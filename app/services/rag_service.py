import chromadb


cliente = chromadb.PersistentClient(
    path="data/chroma"
)


# =====================================================
# COLEÇÕES
# =====================================================

colecao_tickets = cliente.get_or_create_collection(
    name="tickets_clear_it"
)

colecao_kb = cliente.get_or_create_collection(
    name="kb_clear_it"
)


# =====================================================
# TICKETS
# =====================================================

def adicionar_tickets(
    ids,
    documentos,
    embeddings,
    metadados
):

    colecao_tickets.upsert(
        ids=ids,
        documents=documentos,
        embeddings=embeddings,
        metadatas=metadados
    )


def buscar_tickets(
    embedding_consulta,
    categoria=None,
    quantidade=10
):

    parametros = {
        "query_embeddings": [embedding_consulta],
        "n_results": quantidade
    }

    if categoria:
        parametros["where"] = {
            "categoria": categoria
        }

    return colecao_tickets.query(**parametros)


# =====================================================
# BASE DE CONHECIMENTO
# =====================================================

def adicionar_artigos(
    ids,
    documentos,
    embeddings,
    metadados
):

    colecao_kb.upsert(
        ids=ids,
        documents=documentos,
        embeddings=embeddings,
        metadatas=metadados
    )


def buscar_artigos(
    embedding_consulta,
    categoria=None,
    quantidade=10
):

    parametros = {
        "query_embeddings": [embedding_consulta],
        "n_results": quantidade
    }

    if categoria:
        parametros["where"] = {
            "categoria": categoria
        }

    return colecao_kb.query(**parametros)


# =====================================================
# REFERÊNCIAS
# =====================================================

def extrair_referencias(resultado):

    referencias = []

    documentos = resultado.get("documents")
    metadados = resultado.get("metadatas")

    if not documentos or not metadados:
        return referencias

    if len(documentos) == 0 or len(documentos[0]) == 0:
        return referencias

    for documento, metadata in zip(documentos[0], metadados[0]):

        referencias.append(
            {
                "id": metadata.get("id", ""),
                "categoria": metadata.get("categoria", ""),
                "texto": documento[:120] + "..."
            }
        )

    return referencias


# =====================================================
# CONTEXTO PARA O LLM
# =====================================================

def montar_contexto(resultado, titulo):

    contexto = f"\n===== {titulo} =====\n"

    documentos = resultado.get("documents")

    if not documentos:
        contexto += "Nenhum documento encontrado.\n"
        return contexto

    if len(documentos) == 0 or len(documentos[0]) == 0:
        contexto += "Nenhum documento encontrado.\n"
        return contexto

    for i, documento in enumerate(documentos[0], start=1):

        contexto += f"\nDocumento {i}\n"
        contexto += documento
        contexto += "\n"

    return contexto