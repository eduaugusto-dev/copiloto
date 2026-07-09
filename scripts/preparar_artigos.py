import pandas as pd
import json
import os


print("Preparando Base de Conhecimento...")


# Caminho da planilha
ARQUIVO_BASE = "knowledge_base/Base de conhecimento exportada.xlsx"


# Carregar Excel
df = pd.read_excel(
    ARQUIVO_BASE
)

# Remove artigos duplicados pelo ID
df = df.drop_duplicates(
    subset=["ID"]
)


print(f"Artigos únicos encontrados: {len(df)}")

# Lista dos documentos
artigos = []


# Percorrer cada linha da planilha
for _, linha in df.iterrows():

    # Texto que será usado no embedding
    texto = f"""
Título:
{linha['Título']}

Categoria:
{linha['Categoria']}

Tipo:
{linha['Tipo']}

Status:
{linha['Status']}

Pasta:
{linha['Pasta']}

Autor:
{linha['Autor']}

ID:
{linha['ID']}
"""


    # Metadados para consulta futura
    metadata = {

        "id": f"kb_{linha['ID']}",

        "categoria": str(linha["Categoria"]),

        "tipo": str(linha["Tipo"]),

        "status": str(linha["Status"]),

        "pasta": str(linha["Pasta"]),

        "autor": str(linha["Autor"])
    }


    # Documento final
    artigo = {

        "id": f"kb_{linha['ID']}",

        "texto": texto,

        "metadata": metadata
    }


    artigos.append(artigo)



print(
    f"Documentos preparados: {len(artigos)}"
)


# Garantir que a pasta existe
os.makedirs(
    "knowledge_base",
    exist_ok=True
)


# Salvar JSON
ARQUIVO_SAIDA = "knowledge_base/artigos_rag.json"


with open(
    ARQUIVO_SAIDA,
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        artigos,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


print(
    f"Arquivo criado: {ARQUIVO_SAIDA}"
)