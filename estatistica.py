import pandas as pd


# URL do arquivo Excel
url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'

# Ler o arquivo Excel diretamente da URL
df = pd.read_excel(url, engine='openpyxl')

# Exibir as primeiras linhas do DataFrame
df.head()

print(df.head)

'''qualitativa nominal = coisas q n da para colocar em ordem, ierarquia ex. genero, cidade, cor.
-grupo
-descrição
-insumo
-nome_obra
-id_ccoi_elemento
-id_appropriation_compostition
-ip_d
-ip_acum


qualitativa ordinal = é oq da para ordenar sem ser numero ex. patentes , classificação.
-codigo_cc 
-unid



quantitativa discreta = quando c consegue contar sendo valores inteiros e finitos ex. numeros 1,2,3...
-elemento


quantitativa contínua = quando n da para contar ex. peso exato altura exata etc tempo, temperatura ....
-app_inicio
-app_fim
-qntd
'''

