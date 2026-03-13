import pandas as pd


# URL do arquivo Excel
url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'

# Ler o arquivo Excel diretamente da URL
df = pd.read_excel(url, engine='openpyxl')

# TIPO DE VARIÁVEL DE COLUNAS PERTINENTES 
# QUALITATIVA NOMINAL: 
# classe -> nomeia as funções
# caderno -> infraestrutura e edificio 
# grupo -> organiza as funções em grupos        
# codigo_cc -> identificador
# descricao -> tarefas
# codin -> identificador 
# unidin -> unidade de medida   
# tipo_insumo -> cclassifica entre mão de obra e equipamento
# id_ccoi_elemento -> identificador
# id_appropriation_composition -> identificador


# QUALITATIVA ORDINAL:
# unid -> unidad de medida
# insumo -> reccursos utilizados

# QUANTITATIVA DISCRETA:
# elemen -> identificador

# QUANTITATIVA CONTÍNUA:
# app_inicio -> data/hora de início
# app_fim -> data/hora de término
# qntd -> quantidade
# qs -> quantidade 
# data -> data/hora 
# qntd_ac -> quantiade de insumo
# qs_acu -> 
# ip_d -> 
# ip_acu ->
  

# Exibir as primeiras linhas do DataFrame
print(df.head())




