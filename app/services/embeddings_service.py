from sentence_transformers import SentenceTransformer


modelo = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def gerar_embedding(texto: str):

    vector = modelo.encode(
        texto
    )

    return vector.tolist()