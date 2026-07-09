from pydantic import BaseModel
from datetime import datetime
class Ticket(BaseModel):
    id: int
    descricao: str
    status: str
    categoria: str
    prioridade: str
    logs: str
    criado_em: datetime
    prazo_final: datetime
