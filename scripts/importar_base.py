import pandas as pd


arquivo_tickets = "knowledge_base/Massa de dados exportada_Maio.xlsx"


tickets = pd.read_excel(
    arquivo_tickets
)


print("\nQuantidade:")
print(len(tickets))


print("\nColunas:")
print(tickets.columns.tolist())


print("\nPrimeiros registros:")
print(
    tickets.head(10).to_string()
)