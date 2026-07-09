# API CONTRACT
# Copiloto IA de Suporte - Tech Tigers


# 1. CONTEXTO DO PROJETO


## Nome do Sistema

Copiloto IA de Suporte Clear IT


## Objetivo

Criar uma plataforma inteligente para auxiliar analistas de suporte na análise e resolução de tickets.

O sistema recebe um ticket técnico, consulta informações internas utilizando RAG (Retrieval Augmented Generation), analisa o contexto utilizando um modelo de linguagem e retorna um diagnóstico estruturado.


O sistema NÃO substitui o analista.

Ele funciona como um copiloto fornecendo:

- causa provável;
- criticidade;
- ações recomendadas;
- sugestão de resposta;
- nível de confiança;
- evidências utilizadas.


---

# 2. ARQUITETURA DO SISTEMA


O backend já está implementado em FastAPI.


Fluxo:


Usuário

↓

Frontend Web

↓

API FastAPI

↓

Serviço de análise de ticket

↓

Geração de embedding

↓

Busca Vetorial ChromaDB

↓

Base de Conhecimento

+

Tickets Históricos

↓

Construção de contexto RAG

↓

LLM Groq Llama 3.3

↓

Resposta JSON estruturada

↓

Frontend apresenta diagnóstico



---

# 3. TECNOLOGIAS EXISTENTES


Backend:

- Python
- FastAPI
- Pydantic


IA:

- Groq API
- Llama 3.3 70B


RAG:

- ChromaDB
- Embeddings


Dados:

- Base de Conhecimento Clear IT
- Massa histórica de tickets


Frontend esperado:

- React
- TypeScript
- Tailwind CSS


---

# 4. ENDPOINTS DISPONÍVEIS


## Health Check


Método:

GET


Endpoint:

/health


Objetivo:

Verificar se a API está online.



Resposta:


```json
{
 "status":"online"
}
```
# 5. ENDPOINT PRINCIPAL

## POST /analisar-ticket

Descrição:

Recebe um ticket de suporte, consulta a Base de Conhecimento e Tickets Históricos através do RAG e retorna um diagnóstico gerado por IA.

Tempo médio esperado de resposta:

5 a 15 segundos (dependendo da consulta ao modelo de IA).

Content-Type:

application/json

# 6. REQUEST

## Endpoint

POST /analisar-ticket

Content-Type:

application/json

### Exemplo de Requisição

```json
{
  "id": 1001,
  "descricao": "Usuário não consegue conectar na VPN corporativa. Ao tentar acessar apresenta erro de autenticação e não consegue iniciar a conexão.",
  "categoria": "Rede",
  "prioridade": "Alta",
  "status": "Aberto",
  "logs": "Authentication failed. User credentials rejected.",
  "criado_em": "2026-07-09",
  "prazo_final": "2026-07-10"
}
```

Descrição:

Este endpoint recebe um ticket de suporte e inicia o processo completo de análise por Inteligência Artificial.

Ao receber o ticket, o backend:

1. Gera um embedding da descrição e dos logs.
2. Consulta a Base de Conhecimento utilizando RAG.
3. Consulta os Tickets Históricos semelhantes.
4. Monta um contexto enriquecido.
5. Envia o contexto ao modelo Llama 3.3 hospedado na Groq.
6. Processa a resposta do modelo.
7. Calcula a confiança do diagnóstico.
8. Retorna um JSON estruturado para o frontend.

# 7. CAMPOS DO REQUEST

| Campo | Tipo | Obrigatório | Descrição |
|--------|------|-------------|-----------|
| id | Integer | Sim | Identificador do ticket. |
| descricao | String | Sim | Descrição completa do problema. |
| categoria | String | Sim | Categoria técnica do incidente. |
| prioridade | String | Sim | Prioridade do ticket. |
| status | String | Sim | Status atual do ticket. |
| logs | String | Sim | Logs técnicos relacionados ao incidente. |
| criado_em | Date | Sim | Data de abertura do ticket. |
| prazo_final | Date | Sim | Data limite prevista pelo SLA. |

# 8. RESPONSE
## Endpoint

POST /analisar-ticket

Exemplo de Resposta
{
  "causa_provavel": "Erro de autenticação devido a credenciais de usuário rejeitadas.",
  "confianca": 0.90,
  "criticidade": "Alta",
  "acoes_recomendadas": [
    "Verificar as credenciais do usuário.",
    "Validar permissões de acesso à VPN.",
    "Consultar a Base de Conhecimento para revisar a configuração da VPN."
  ],
  "necessita_escalonamento": false,
  "rascunho_resposta": "Prezado usuário, identificamos uma possível falha de autenticação durante a conexão com a VPN. Estamos verificando as credenciais e as permissões de acesso. Caso o problema persista, entraremos em contato para realizar novas verificações.",
  "artigos_utilizados": [
    {
      "id": "33000052297",
      "categoria": "KBs Internos",
      "texto": "Criação de VPN-IPSEC - FORTIGATE..."
    }
  ],
  "tickets_semelhantes": [
    {
      "id": "1266",
      "categoria": "Windows",
      "texto": "Criação de acesso VPN..."
    }
  ]
}
Descrição

A API sempre retorna um JSON estruturado contendo o diagnóstico gerado pela IA, o nível de confiança calculado pelo backend e todas as evidências utilizadas durante o processo RAG.

# 9. DESCRIÇÃO DOS CAMPOS DA RESPONSE
Campo	Tipo	Descrição
causa_provavel	String	Diagnóstico principal identificado pela IA.
confianca	Float	Valor entre 0 e 1 representando a confiança do diagnóstico. O frontend deve exibir como porcentagem.
criticidade	String	Baixa, Média, Alta ou Crítica.
acoes_recomendadas	Array<String>	Lista de ações sugeridas pela IA.
necessita_escalonamento	Boolean	Indica se o ticket deve ser escalonado.
rascunho_resposta	String	Sugestão de resposta ao usuário final.
artigos_utilizados	Array<Object>	Artigos recuperados pela Base de Conhecimento.
tickets_semelhantes	Array<Object>	Tickets históricos utilizados como referência.
Regras
O frontend nunca recalcula a confiança.
Toda a lógica permanece no backend.
O frontend apenas apresenta os dados retornados.

# 10. FLUXO DE EXECUÇÃO
1.O analista abre um ticket.
2. O frontend envia o ticket para a API.
3. A API gera um embedding.
4. O ChromaDB realiza a busca vetorial.
5. São recuperados artigos da Base de Conhecimento.
6. São recuperados tickets históricos semelhantes.
7. O backend monta o contexto RAG.
8. O contexto é enviado para o Llama 3.3 (Groq).
9. O modelo gera um diagnóstico estruturado.
10. O backend calcula a confiança.
11. O backend adiciona as referências utilizadas.
12. A resposta JSON é enviada ao frontend.
13. O frontend apresenta o diagnóstico ao analista.

# 11. TELAS DA APLICAÇÃO
## Dashboard

Exibir indicadores gerais:

Quantidade de tickets analisados
Tickets pendentes
Tickets críticos
Média de confiança das análises
Últimas análises realizadas
Lista de Tickets

Tabela contendo:

ID
Categoria
Prioridade
Status
Data de abertura
Botão "Analisar"

Filtros:

Categoria
Prioridade
Status
Pesquisa textual
Tela de Análise

Layout dividido em duas colunas.

Coluna esquerda

Informações do ticket:

ID
Categoria
Prioridade
Status
Descrição
Logs
Coluna direita

Resultado da IA:

Causa provável
Criticidade
Confiança
Escalonamento
Ações recomendadas
Rascunho de resposta
Evidências do RAG

Seção contendo duas tabelas.

Base de Conhecimento

Mostrar:

ID
Categoria
Trecho utilizado
Tickets Semelhantes

Mostrar:

ID
Categoria
Resumo
Histórico

Lista de análises realizadas.

Cada item deve permitir reabrir a análise.

# 12. COMPONENTES DA INTERFACE

Utilizar componentes modernos.

Componentes esperados:

Sidebar
Navbar superior
Cards
Tabelas
Badges
Alertas
Botões
Inputs
Área de texto
Loading
Skeleton Loading
Progress Bar
Modal
Toast de sucesso
Toast de erro

# 13. REGRAS DE NEGÓCIO
O frontend nunca executa lógica de IA.
Toda análise ocorre no backend.
Toda busca vetorial ocorre no backend.
Toda consulta ao LLM ocorre no backend.
O frontend apenas consome a API.
O frontend deve suportar futuras autenticações sem alteração estrutural.

# 14. TRATAMENTO DE ERROS
HTTP 200

Análise realizada com sucesso.

HTTP 422

Campos obrigatórios ausentes.

Exibir mensagem amigável.

HTTP 500

Erro interno.

Exibir mensagem:

"Não foi possível concluir a análise do ticket."

Permitir nova tentativa.

Timeout

Caso a IA demore.

Mostrar indicador:

"A IA está analisando o ticket..."

# 15. IDENTIDADE VISUAL

O sistema deve possuir aparência corporativa.

Inspirado em:

Jira Service Management
ServiceNow
Freshservice
Zendesk
Azure Portal

Paleta:

Azul
Branco
Cinza
Verde para sucesso
Vermelho para criticidade
Amarelo para atenção

Utilizar Tailwind CSS.

# 16. EXPERIÊNCIA DO USUÁRIO

A interface deve ser:

Moderna
Responsiva
Minimalista
Rápida
Intuitiva

O fluxo deve exigir o menor número possível de cliques.

Durante chamadas à API:

Mostrar animação de carregamento.
Bloquear múltiplos envios simultâneos.
Exibir progresso da análise.

# 17. OBJETIVO DO FRONTEND

O frontend deverá consumir a API FastAPI já existente.

Não criar dados mockados.

Não simular respostas.

Toda informação apresentada deverá ser proveniente da API.

O frontend deverá ser desenvolvido em:

React
TypeScript
Tailwind CSS

A aplicação deverá estar preparada para futuras funcionalidades, como:

Autenticação
Histórico persistente
Dashboard analítico
Exportação de relatórios
Integração com sistemas ITSM
Upload de anexos
Notificações em tempo real

# 18. ESTRUTURA DAS PÁGINAS

O frontend deverá possuir as seguintes páginas:

- Dashboard
- Lista de Tickets
- Detalhes do Ticket
- Análise da IA
- Histórico de Análises
- Página 404

# 19. COMPONENTES REUTILIZÁVEIS

Os seguintes componentes deverão ser reutilizáveis:

- Sidebar
- Header
- Card
- Badge
- ProgressBar
- Loading
- Modal
- ConfirmDialog
- TicketCard
- TicketTable
- IAResultCard
- KnowledgeCard
- SimilarTicketCard
- SearchInput
- Filters
- Pagination

# 20. OBJETIVO DO LOVABLE

O frontend deverá ser construído consumindo diretamente a API FastAPI existente.

Não utilizar dados mockados.

Não criar endpoints fictícios.

Toda comunicação deverá ocorrer através da API documentada neste arquivo.

A interface deverá ser moderna, responsiva e inspirada em ferramentas corporativas de ITSM.

O sistema deverá estar preparado para futura autenticação, dashboards analíticos e integração com sistemas externos.

Todo o código deverá seguir boas práticas de React, TypeScript e Tailwind CSS, priorizando componentes reutilizáveis e organização da estrutura do projeto.