import pandas as pd

#IMPORTAÇÃO E RECONHECIMENTO DA BASE

url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'
df = pd.read_excel(url, engine='openpyxl')
print(df.head())

#TIPO DE VARIÁVEL / EXPLICAÇÃO DE CADA COLUNA 

# QUALITATIVA NOMINAL: 
# classe -> descrição da atividade. Diz o que é feito, sem dizer a função.
# caderno -> frente. Divide-se entre infraestrutura e edificio.
# grupo -> descrição da atividade. Diz o que é feito, sem dizer a função.        
# codigo_cc -> identificação da obra. É uma sequência de numeros e caracteres padronizados, que possuem a função de identificar na obra
# descricao -> etapa da obra. São objetivos a serem cumpridos
# codins -> identificação da obra. Sequência de números, que possuem a função de identificar na obra
# unidins -> unidades de medida usadas na obra
# tipo_insumo -> tipo insumo. São identificados por mão de obra e equipamento
# id_ccoi_elemento -> identificação da obra. Sequência de números, que possuem a função de identificar na obra
# id_appropriation_composition ->  identificação da obra. Sequência de números, que possuem a função de identificar na obra


# QUALITATIVA ORDINAL:
# unid -> unidade de medida usadas na obra
# insumo -> tipo de insumo. Cita a mão de obra e equipamento presentes na obra

# QUANTITATIVA DISCRETA:
# elemen -> identificador da obra

# QUANTITATIVA CONTÍNUA:
# app_inicio ->período de registro. Informa o dia, mês, ano e horário de início do registro.
# app_fim -> período de registro. Informa o dia, mês, ano e horário do fim do registro.
# qntd -> quantidade produzida.
# qs -> quantidade produzida.
# data -> período de registro
# qntd_ac -> quantiade de insumo
# qs_acum -> indicadores de produtividade
# ip_d -> indicador de produtividade
# ip_acum -> indicador de produtividade