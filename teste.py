import pandas as pd

# O link precisa ser o "Direct Link" (que baixa o arquivo sozinho no navegador)
url_direta = 'https://fiapcom.sharepoint.com/.../Doc2.xlsx?download=1'

try:
    df = pd.read_excel(url_direta, engine='openpyxl')
    print("Sucesso! Dados carregados:")
    print(df.head())
except Exception as e:
    print(f"Erro ao acessar: {e}")
    print("Dica: Verifique se o link não exige login ou se é um link de visualização.")