from pydantic import BaseModel
from typing import List, Dict, Any


class RespostaIA(BaseModel):

    causa_provavel: str

    confianca: float

    criticidade: str

    acoes_recomendadas: List[str]

    necessita_escalonamento: bool

    rascunho_resposta: str

    artigos_utilizados: List[Dict[str, Any]]

    tickets_semelhantes: List[Dict[str, Any]]