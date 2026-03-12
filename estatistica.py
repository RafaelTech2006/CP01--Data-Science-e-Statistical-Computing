import pandas as pd


# URL do arquivo Excel
url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'

# Ler o arquivo Excel diretamente da URL
df = pd.read_excel(url, engine='openpyxl')

# Exibir as primeiras linhas do DataFrame
df.head()

print(df.head)
