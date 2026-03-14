import pandas as pd
import streamlit as st
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as pl

#IMPORTAÇÃO E RECONHECIMENTO DA BASE
@st.cache_data
def carregar_dados():
    url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'
    return pd.read_excel(url, engine='openpyxl')

df = carregar_dados()

url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'
df = pd.read_excel(url, engine='openpyxl')

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
# elemen -> identificador da obra. 

# QUANTITATIVA CONTÍNUA:
# app_inicio ->período de registro. Informa o dia, mês, ano e horário de início do registro.
# app_fim -> período de registro. Informa o dia, mês, ano e horário do fim do registro.
# qntd -> quantidade produzida.
# qs -> quantidade produzida.
# data -> período de registro. Informa o dia, mês, ano e horário de início do registro.
# qntd_acum -> quantiade acumlada
# qs_acum -> quantidade acumulada
# ip_d -> identificação da obra
# ip_acum -> identificação da obra

#FILTRAGEM DADOS
mao_de_obra = df[df['tipo_insumo'] == 'MAO DE OBRA'] 
print(mao_de_obra.head())
st.warning("O filtro da 'MÃO DE OBRA' torna a comparação de produtividade mais coerente pois evita o encontro entre dois insumos diferentes, priorizando a ação do trabalhador, assim, possibilitando a análise de sua produtividade com mais eficiência.")

#LEITURA EXPLORATÓRIA E FORMULAÇÃO DE PERGUNTAS
# Qual obra possui a maior média?
# Qual a moda do menos e do mais produtivo?
# onde começa o primeiro quartil?
# Qual a amplitude da obra?
# Ha valores qeu superam ou são inferiores ao limite superior/inferior?  
# Qual o seu limite superior e inferior financeiro para a obra?



#Remover valores NaN ou infinitos na coluna 'ip_d'
df_mao_de_obra = mao_de_obra[np.isfinite(mao_de_obra['ip_d'])]

#Calcular Média e Mediana
media_ip = df_mao_de_obra['ip_d'].mean()
mediana_ip = df_mao_de_obra['ip_d'].median()

#Calcular a Moda Contínua utilizando KDE 
kde = gaussian_kde(df_mao_de_obra['ip_d'], bw_method='scott')
x_values = np.linspace(df_mao_de_obra['ip_d'].min(), df_mao_de_obra['ip_d'].max(), 1000)
kde_values = kde(x_values)
moda_ip_continua = x_values[np.argmax(kde_values)]

#Mesma coisa mas agora para 'qntd'

df_mao_de_obra = mao_de_obra[np.isfinite(mao_de_obra['ip_d'])]

#Calcular Média e Mediana
media_qntd = df_mao_de_obra['qntd'].mean()
mediana_qntd = df_mao_de_obra['qntd'].median()

#Calcular a Moda Contínua utilizando KDE 
kde = gaussian_kde(df_mao_de_obra['qntd'], bw_method='scott')
x_values = np.linspace(df_mao_de_obra['qntd'].min(), df_mao_de_obra['qntd'].max(), 1000)
kde_values = kde(x_values)
moda_qntd_continua = x_values[np.argmax(kde_values)]


# Print tabela filtrada 
st.write("Dados de Mão de Obra:", df_mao_de_obra.head())

# Exibindo os resultados de forma organizada "ip"
st.subheader("Estatísticas de Produtividade (IP)")

col1, col2, col3 = st.columns(3)

col1.metric("Média", f"{media_ip:.4f}")
col2.metric("Mediana", f"{mediana_ip:.4f}")
col3.metric("Moda (KDE)", f"{moda_ip_continua:.4f}")

# Exibindo os resultados de forma organizada "qntd"
st.subheader("Estatísticas de Volume (Quantidade)")
c4, c5, c6 = st.columns(3)
c4.metric("Média Qntd", f"{media_qntd:.2f}")
c5.metric("Mediana Qntd", f"{mediana_qntd:.2f}")
c6.metric("Moda Qntd (KDE)", f"{moda_qntd_continua:.2f}")

#medidas de dispersão

# Lista das variáveis que realmente importam para dispersão
variaveis_importantes = ['ip_d', 'qntd']

for var in variaveis_importantes:
    # Limpeza rápida para a variável atual
    dados_limpos = df_mao_de_obra[np.isfinite(df_mao_de_obra[var])].copy()
    
    # Cálculos
    media = dados_limpos[var].mean()
    desvio = dados_limpos[var].std()
    cv = (desvio / media) * 100 if media != 0 else 0
    amplitude = dados_limpos[var].max() - dados_limpos[var].min()
    variancia = dados_limpos[var].var()
    
    # Título da seção no Streamlit
    st.subheader(f"Análise de: {var.upper()}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Amplitude", f"{amplitude:.3f}")
    c2.metric("Desvio-Padrão", f"{desvio:.3f}")
    c3.metric("Variância", f"{variancia:.3f}")
    c4.metric("Coef. Variação", f"{cv:.2f}%")
    
