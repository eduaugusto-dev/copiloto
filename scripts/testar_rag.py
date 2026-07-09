import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.services.embeddings_service import gerar_embedding
from app.services.rag_service import buscar_documentos



consulta = """
Usuário não consegue acessar VPN,
apresenta erro de autenticação.
"""



embedding = gerar_embedding(
    consulta
)



resultado = buscar_documentos(
    embedding,
    quantidade=5
)



print("\nResultados encontrados:\n")


for documento in resultado["documents"][0]:

    print("---------------------")
    print(documento)