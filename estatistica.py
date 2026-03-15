import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import gaussian_kde

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard de Produtividade - Mão de Obra", layout="wide")

# CSS para garantir visibilidade e estilo das caixas (Dark/Light Mode)
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px;
        border-radius: 10px;
    }
    .resposta-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00CC96;
        background-color: rgba(0, 204, 150, 0.1);
        margin: 10px 0px 20px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def carregar_dados():
    url = 'https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx'
    df = pd.read_excel(url, engine='openpyxl')
    # Filtro obrigatório: Mão de Obra
    df_filtrado = df[df['tipo_insumo'] == 'MAO DE OBRA'].copy()
    df_filtrado = df_filtrado.dropna(subset=['ip_d', 'qntd'])
    return df_filtrado

df = carregar_dados()

# --- SIDEBAR (FILTROS E AS 6 PERGUNTAS) ---
st.sidebar.header("⚙️ Painel de Controle")
obras_selecionadas = st.sidebar.multiselect("Selecione as Obras:", 
                                            options=df['codigo_cc'].unique(),
                                            default=df['codigo_cc'].unique()[:3])

df_view = df[df['codigo_cc'].isin(obras_selecionadas)]

st.sidebar.divider()
st.sidebar.header("🔍 Consultas Analíticas")
pergunta_selecionada = st.sidebar.selectbox(
    "Escolha uma pergunta:",
    [
        "Selecione uma pergunta...",
        "1. Qual obra possui a maior média?",
        "2. Qual a moda do menos e do mais produtivo?",
        "3. Onde começa o primeiro quartil (Q1)?",
        "4. Qual a amplitude da obra?",
        "5. Há valores que superam o limite superior (Outliers)?",
        "6. Qual o nível de estabilidade (CV) da obra?"
    ]
)

# --- TÍTULO ---
st.title("📊 Análise de Produtividade: Mão de Obra")

# --- LAYOUT: MÉTRICAS PRINCIPAIS (HORIZONTAL) ---
st.subheader("📌 Indicadores Principais")
c1, c2, c3, c4, c5 = st.columns(5)

m_ip = df_view['ip_d'].mean()
std_ip = df_view['ip_d'].std()

c1.metric("Média (IP)", f"{m_ip:.4f}")
c2.metric("Mediana (IP)", f"{df_view['ip_d'].median():.4f}")
c3.metric("Desvio Padrão", f"{std_ip:.4f}")
c4.metric("Q1 (25%)", f"{df_view['ip_d'].quantile(0.25):.4f}")
c5.metric("Amplitude", f"{(df_view['ip_d'].max() - df_view['ip_d'].min()):.4f}")

st.divider()

# --- ÁREA DE RESPOSTAS DINÂMICAS ---
if pergunta_selecionada != "Selecione uma pergunta...":
    st.subheader("💡 Resposta Analítica")
    st.markdown('<div class="resposta-box">', unsafe_allow_html=True)
    
    if "1." in pergunta_selecionada:
        obra_top = df_view.groupby('codigo_cc')['ip_d'].mean().idxmax()
        st.write(f"**Resultado:** A obra com maior produtividade média é a **{obra_top}**.")
    
    elif "2." in pergunta_selecionada:
        kde = gaussian_kde(df_view['ip_d'])
        x = np.linspace(df_view['ip_d'].min(), df_view['ip_d'].max(), 500)
        moda = x[np.argmax(kde(x))]
        st.write(f"**Resultado:** A moda estatística é **{moda:.4f}**. Representa o pico de frequência da eficiência.")
        
    elif "3." in pergunta_selecionada:
        q1 = df_view['ip_d'].quantile(0.25)
        st.write(f"**Resultado:** O primeiro quartil começa em **{q1:.4f}**. Indica que 25% dos dados estão abaixo deste valor.")
            
    elif "4." in pergunta_selecionada:
        amp = df_view['ip_d'].max() - df_view['ip_d'].min()
        st.write(f"**Resultado:** A amplitude total é de **{amp:.4f}**.")

    elif "5." in pergunta_selecionada:
        q1, q3 = df_view['ip_d'].quantile([0.25, 0.75])
        lim_sup = q3 + 1.5 * (q3 - q1)
        outliers = df_view[df_view['ip_d'] > lim_sup].shape[0]
        st.write(f"**Resultado:** Foram detetados **{outliers}** registros acima do limite superior (**{lim_sup:.4f}**).")

    elif "6." in pergunta_selecionada:
        cv = (std_ip / m_ip) * 100 if m_ip != 0 else 0
        st.write(f"**Resultado:** O CV é de **{cv:.2f}%**. {'Baixa estabilidade' if cv > 30 else 'Processo estável'}.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- LAYOUT: GRÁFICOS ---
theme = "plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white"

col_g1, col_g2 = st.columns(2)
with col_g1:
    fig_hist = px.histogram(df_view, x="ip_d", nbins=30, title="Frequência do IP", color_discrete_sequence=['#636EFA'])
    fig_hist.update_layout(template=theme)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_g2:
    fig_box = px.box(df_view, x="codigo_cc", y="ip_d", title="Boxplot: Quartis e Outliers", color="codigo_cc")
    fig_box.update_layout(template=theme)
    st.plotly_chart(fig_box, use_container_width=True)

st.subheader("🔍 Gráfico de Dispersão: Relação Quantidade vs IP")
fig_scatter = px.scatter(df_view, x="qntd", y="ip_d", color="codigo_cc", size="qntd", hover_data=['descricao'])
fig_scatter.update_layout(template=theme)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# --- SEÇÃO MINIMIZADA (EXPANDERS) ---
with st.expander("📋 Ver Dados Filtrados (Base de Dados Amostral)"):
    st.write("Abaixo estão os dados brutos filtrados por Obra e Mão de Obra:")
    st.dataframe(df_view, use_container_width=True)

with st.expander("🏷️ Classificação de Variáveis (Dicionário do Projeto)"):
    c_class1, c_class2 = st.columns(2)
    with c_class1:
        st.write("**Qualitativa Nominal:** `classe`, `codigo_cc`, `caderno`, `grupo`, `descricao`, `tipo_insumo`.")
        st.write("**Qualitativa Ordinal:** `unid`, `insumo`.")
    with c_class2:
        st.write("**Quantitativa Contínua:** `ip_d`, `qntd`, `data`, `app_inicio`, `app_fim`.")
        st.write("**Quantitativa Discreta:** `elemen`.")