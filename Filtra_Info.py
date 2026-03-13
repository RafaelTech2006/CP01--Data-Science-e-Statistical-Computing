import pandas as pd
import unicodedata

# 1. Função para normalizar o texto (Remover acentos e Ç)
def remover_acentos_e_cedilha(texto):
    if not isinstance(texto, str):
        return texto  # Se não for texto (ex: número), retorna como está
    
    # Normaliza para a forma NFD (decomposição)
    # Exemplo: 'ç' vira 'c' + 'cedilha combinada'
    nfkd_form = unicodedata.normalize('NFKD', texto)
    
    # Filtra apenas os caracteres que não são "marcas de acentuação" (Mn)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

# 2. Importação do arquivo do GitHub
url = "https://github.com/Dormamos64/excell/raw/refs/heads/main/df_diarios.xlsx"
df = pd.read_excel(url)

# 3. Filtragem de Mão de Obra (Mantendo seu pedido anterior)
df_filtrado = df[df['tipo_insumo'] == 'MAO DE OBRA'].copy()

# 4. Aplicando a limpeza em todas as colunas de texto
# O applymap percorre todas as células do DataFrame
df_limpo = df_filtrado.applymap(remover_acentos_e_cedilha)

# 5. Resultado
print("Dados limpos (sem acentos e sem cedilha):")
print(df_limpo[['insumo', 'descricao']].head())

# Opcional: Salvar o resultado limpo em um novo arquivo
# df_limpo.to_excel("df_diarios_limpo.xlsx", index=False)