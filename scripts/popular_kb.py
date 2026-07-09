import sys
import os
import json


print("Iniciando carga da Base de Conhecimento...")


# Permite importar a pasta app
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.services.embeddings_service import gerar_embedding
from app.services.rag_service import adicionar_artigos



# Arquivo gerado pelo preparar_artigos.py
ARQUIVO = "knowledge_base/artigos_rag.json"



# Ler artigos
with open(
    ARQUIVO,
    "r",
    encoding="utf-8"
) as arquivo:

    artigos = json.load(arquivo)



print(
    f"Quantidade de artigos encontrados: {len(artigos)}"
)



ids = []

documentos = []

embeddings = []

metadados = []



for artigo in artigos:


    print(
        f"Processando artigo {artigo['id']}..."
    )


    texto = artigo["texto"]


    embedding = gerar_embedding(
        texto
    )


    ids.append(
        artigo["id"]
    )


    documentos.append(
        texto
    )


    embeddings.append(
        embedding
    )


    metadados.append(
        artigo["metadata"]
    )



adicionar_artigos(
    ids=ids,
    documentos=documentos,
    embeddings=embeddings,
    metadados=metadados
)



print("\nCarga concluída!")

print(
    f"{len(ids)} artigos adicionados ao ChromaDB."
)