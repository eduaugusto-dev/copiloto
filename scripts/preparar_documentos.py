import pandas as pd
import json
import os


arquivo_tickets = (
    "knowledge_base/Massa de dados exportada_Maio.xlsx"
)


arquivo_saida = (
    "knowledge_base/documentos_rag.json"
)



# Ler tickets

tickets = pd.read_excel(
    arquivo_tickets
)


print(
    f"Tickets carregados: {len(tickets)}"
)



documentos = []



for index, ticket in tickets.iterrows():


    documento = f"""
Ticket histórico: {ticket['ID do ticket']}

Tipo:
{ticket['Tipo']}

Categoria:
{ticket['Categoria']}

Subcategoria:
{ticket['Subcategoria']}

Prioridade:
{ticket['Prioridade']}


Assunto:
{ticket['Assunto']}


Descrição do problema:
{ticket['Descrição']}


Interações do analista:
{ticket['Interações do analista']}


Resolução aplicada:
{ticket['Nota de resolução']}


Status:
{ticket['Status da Resolução']}


Tags:
{ticket['Tags']}
"""


    documentos.append(
        {
            "id": str(ticket["ID do ticket"]),
            "texto": documento,
            "metadata": {
                "tipo": "ticket_historico",
                "categoria": str(ticket["Categoria"]),
                "subcategoria": str(ticket["Subcategoria"])
            }
        }
    )



# Salvar resultado

with open(
    arquivo_saida,
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        documentos,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


print(
    f"Documentos criados: {len(documentos)}"
)

print(
    f"Arquivo salvo em: {arquivo_saida}"
)