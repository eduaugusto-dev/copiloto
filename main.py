from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.modelos.ticket import Ticket
from app.schemas.resposta import RespostaIA
from app.services.llm_service import analisar_ticket


app = FastAPI(
    title="Tech Tigers Copiloto IA",
    description="API de análise inteligente de tickets de suporte usando RAG + LLM",
    version="1.0.0"
)

# ---------------------------------
# CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # depois você pode restringir ao domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Health Check
# ---------------------------------

@app.get("/")
def status():

    return {
        "status": "online",
        "servico": "Tech Tigers Copiloto IA"
    }


# ---------------------------------
# Análise de Ticket
# ---------------------------------

@app.post("/analisar-ticket")
def analisar(ticket: Ticket):

    try:

        resposta = analisar_ticket(ticket)

        return resposta

    except Exception as e:

        print("ERRO REAL:")
        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
