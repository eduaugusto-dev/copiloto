import os
import json

from dotenv import load_dotenv
from groq import Groq

from app.modelos.ticket import Ticket

from app.services.embeddings_service import gerar_embedding

from app.services.rag_service import (
    buscar_artigos,
    buscar_tickets,
    montar_contexto,
    extrair_referencias
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================================
# BUSCA CONTEXTO RAG
# ==========================================================

def buscar_contexto_rag(ticket: Ticket):

    texto_busca = f"""
Categoria:
{ticket.categoria}

Descrição:
{ticket.descricao}

Logs:
{ticket.logs}
"""

    embedding = gerar_embedding(texto_busca)

    artigos = buscar_artigos(
        embedding_consulta=embedding,
        quantidade=10
    )

   
    tickets = buscar_tickets(
        embedding_consulta=embedding,
        quantidade=10
    )

    print("\n========== DEBUG ARTIGOS RAG ==========")

    for i, doc in enumerate(artigos["documents"][0]):

        print("\nDocumento:", i + 1)

        print("ID:", artigos["ids"][0][i])

        print("Distância:",
              artigos["distances"][0][i])

        print("Categoria:",
              artigos["metadatas"][0][i].get("categoria"))

        print("Trecho:",
              doc[:200])


    print("\n========== DEBUG TICKETS RAG ==========")

    for i, doc in enumerate(tickets["documents"][0]):

        print("\nTicket:", i + 1)

        print("ID:", tickets["ids"][0][i])

        print("Distância:",
              tickets["distances"][0][i])

        print("Categoria:",
              tickets["metadatas"][0][i].get("categoria"))

        print("Trecho:",
              doc[:200])


    contexto = (
        montar_contexto(
            artigos,
            "BASE DE CONHECIMENTO"
        )
        +
        "\n"
        +
        montar_contexto(
            tickets,
            "TICKETS HISTÓRICOS"
        )
    )


    return (
        contexto,
        extrair_referencias(artigos),
        extrair_referencias(tickets)
    )



# ==========================================================
# CÁLCULO DA CONFIANÇA
# ==========================================================

def calcular_confianca(
    ticket: Ticket,
    artigos_utilizados,
    tickets_utilizados
):

    score = 0.0

    descricao = ticket.descricao.lower()
    logs = ticket.logs.lower()
    categoria = ticket.categoria.lower()


    # ---------------------------------
    # 1. Evidência RAG - Base conhecimento
    # Peso: 40%
    # ---------------------------------

    if artigos_utilizados:

        quantidade_artigos = len(artigos_utilizados)

        if quantidade_artigos >= 3:
            score += 0.40

        elif quantidade_artigos == 2:
            score += 0.35

        elif quantidade_artigos == 1:
            score += 0.30


    # ---------------------------------
    # 2. Evidência RAG - Tickets históricos
    # Peso: 30%
    # ---------------------------------

    if tickets_utilizados:

        quantidade_tickets = len(tickets_utilizados)

        if quantidade_tickets >= 3:
            score += 0.30

        elif quantidade_tickets == 2:
            score += 0.25

        elif quantidade_tickets == 1:
            score += 0.20


    # ---------------------------------
    # 3. Indicadores técnicos
    # Peso: 15%
    # ---------------------------------

    erros = [
        "error",
        "failed",
        "authentication",
        "timeout",
        "connection",
        "offline",
        "exception",
        "denied",
        "refused"
    ]


    encontrados = sum(
        1 for erro in erros
        if erro in logs
    )


    if encontrados >= 3:
        score += 0.15

    elif encontrados == 2:
        score += 0.10

    elif encontrados == 1:
        score += 0.05


    # ---------------------------------
    # 4. Qualidade do ticket
    # Peso: 10%
    # ---------------------------------

    if len(descricao) > 200:
        score += 0.10

    elif len(descricao) > 100:
        score += 0.05


    # ---------------------------------
    # 5. Categoria conhecida
    # Peso: 5%
    # ---------------------------------

    categorias = [
        "rede",
        "banco de dados",
        "infraestrutura",
        "windows",
        "linux",
        "backup",
        "api",
        "email"
    ]


    if categoria in categorias:
        score += 0.05


    return round(min(score, 0.98), 2)

# ==========================================================
# ANÁLISE DO TICKET
# ==========================================================

def analisar_ticket(ticket: Ticket):

    # ---------------------------------
    # Recuperação de contexto (RAG)
    # ---------------------------------

    contexto_rag, artigos_utilizados, tickets_utilizados = buscar_contexto_rag(ticket)

    print("\n========== CONTEXTO RAG ==========")
    print(contexto_rag)
    print("==================================\n")

    # ---------------------------------
    # Prompt enviado ao LLM
    # ---------------------------------

    prompt = f"""
Você é um Analista Sênior de Infraestrutura da Clear IT.

Você possui acesso à Base de Conhecimento da empresa e aos Tickets Históricos.

Utilize essas informações como referência antes de responder.

=========================
BASE DE CONHECIMENTO E TICKETS
=========================

{contexto_rag}

=========================
TICKET RECEBIDO
=========================

ID:
{ticket.id}

Descrição:
{ticket.descricao}

Categoria:
{ticket.categoria}

Prioridade:
{ticket.prioridade}

Status:
{ticket.status}

Logs:
{ticket.logs}

=========================

Sua missão é:

1. Identificar a causa provável do incidente.

2. Classificar a criticidade.

3. Sugerir ações de resolução.

4. Informar se o ticket deve ser escalonado.

5. Elaborar um rascunho de resposta para o usuário.

Regras importantes:

- Utilize prioritariamente os artigos da Base de Conhecimento.
- Considere os tickets históricos semelhantes.
- Não invente procedimentos.
- Caso não exista informação suficiente, deixe isso claro.
- NÃO informe a confiança da resposta.
- Responda SOMENTE um JSON válido.

Formato obrigatório:

{{
    "causa_provavel": "",
    "criticidade": "",
    "acoes_recomendadas": [],
    "necessita_escalonamento": false,
    "rascunho_resposta": ""
}}
"""

    # ---------------------------------
    # Chamada ao LLM
    # ---------------------------------

    resposta = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um especialista em suporte técnico corporativo, "
                    "infraestrutura, redes, servidores, banco de dados, VPN, "
                    "Windows, Linux e boas práticas de ITSM."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    if not resposta.choices:
        raise Exception("A API não retornou nenhuma resposta.")

    conteudo = resposta.choices[0].message.content

    conteudo = conteudo.replace("```json", "")
    conteudo = conteudo.replace("```", "")
    conteudo = conteudo.strip()

    print("\n========== RESPOSTA DO LLM ==========")
    print(conteudo)
    print("=====================================\n")

        # ---------------------------------
    # Processamento da resposta
    # ---------------------------------


    try:

        diagnostico = json.loads(conteudo)

        # Confiança calculada pelo sistema
        diagnostico["confianca"] = calcular_confianca(
    ticket,
    artigos_utilizados,
    tickets_utilizados
)

        # Referências utilizadas pelo RAG
        diagnostico["artigos_utilizados"] = artigos_utilizados

        diagnostico["tickets_semelhantes"] = tickets_utilizados

        return diagnostico


    except json.JSONDecodeError:

        raise Exception(
            "A resposta gerada pela IA não possui um JSON válido."
        )


    except KeyError as e:

        raise Exception(
            f"Campo obrigatório ausente na resposta da IA: {str(e)}"
        )


    except Exception as e:

        raise Exception(
            f"Erro ao processar diagnóstico do ticket: {str(e)}"
        )