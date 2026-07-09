print("Iniciando carga no ChromaDB...")


import sys
import os
import json


# Permite que o script encontre a pasta app/
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.services.embeddings_service import gerar_embedding
from app.services.rag_service import adicionar_documentos



# Caminho do arquivo com os documentos preparados
ARQUIVO_DOCUMENTOS = (
    "knowledge_base/documentos_rag.json"
)



def carregar_documentos():

    with open(
        ARQUIVO_DOCUMENTOS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)



def preparar_embeddings(documentos):

    ids = []
    textos = []
    embeddings = []
    metadados = []


    for documento in documentos:

        print(
            "Processando:",
            documento["id"]
        )


        ids.append(
            documento["id"]
        )


        textos.append(
            documento["texto"]
        )


        embeddings.append(
            gerar_embedding(
                documento["texto"]
            )
        )


        metadados.append(
            documento["metadata"]
        )


    return (
        ids,
        textos,
        embeddings,
        metadados
    )



def main():


    documentos = carregar_documentos()


    print(
        f"Documentos encontrados: {len(documentos)}"
    )


    (
        ids,
        textos,
        embeddings,
        metadados
    ) = preparar_embeddings(documentos)



    adicionar_documentos(
        ids,
        textos,
        embeddings,
        metadados
    )


    print(
        f"{len(ids)} documentos adicionados ao ChromaDB"
    )



if __name__ == "__main__":

    main()