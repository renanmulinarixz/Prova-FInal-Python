from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Prova Final Python", layout="wide")
st.title("Gráficos de pizza - Total veículos minicípios")

PASTA = Path(__file__).resolve().parent
municipios = ["Belo Horizonte", "Contagem", "Betim"]
parametros = ["id_municipio_nome", "tipo_veiculo", "quantidade"]
CORES = {"Belo Horizonte": "#FF6B6B", "0Contagem": "#00F5D4", "Betim":"#FF6B6B"}

rotulo_parametros = {
    "id_municipio_nome": "id_municipio_nome",
    "tipo-veiculo": "tipo_veiculo",
    "quantidade": "quantidade"
}
st.sidebar.header("Controles")
formato = st.sidebar.radio("Arquivo de exemplo", ["CSV", "Excel (.xlsx)"])
try:
    if formato == "CSV":
        df = pd.read_csv(PASTA / "numero_veiculos.csv", encoding="utf-8")
        
    else:
        df = pd.read_excel(
            PASTA / "numero_veiculos.csv",
            engine="openpyxl"
        )
       
    obrigatorias = ["ano", "mes", "sigla_uf"] + parametros
    faltando = [coluna for coluna in obrigatorias if coluna not in df.columns]
    if faltando:
        st.error(f"Colunas ausentes no arquivo: {faltando}")
        st.stop()

 
    for coluna in ["ano", "mes"] + parametros:
        df[coluna] = pd.to_numeric(df[coluna], errors="raise")

    if df[obrigatorias].isna().any().any():
        st.error("Há células vazias nas colunas usadas. Confira o arquivo.")
        st.stop()
except (OSError, ValueError, ImportError) as erro:
   
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()


df_filtrado = df[
    (df["id_municipio_nome"].isin(municipios))
].copy()
df_filtrado = df_filtrado.sort_values(["id_municipios", "ano", "mes"])
df_tabela = df_filtrado[["id_municipios", "ano", "mes"]].copy()

if df_filtrado.empty:
    st.warning("Nenhuma linha passou pelo filtro. Confira os nomes e a série.")
    st.stop()


df_2025 = df_filtrado["ano"] == 2025 & df_filtrado["mes"==12] & df_filtrado["id_municipios" == "Belo Horizonte"].copy()

dados_empilhado = df_2025.melt(
    id_vars="id_municipio_nome",
    value_vars=parametros,
    var_name="parametros",
    value_name="Valor",
).rename(columns={"id_municipios_nome": "Cidade"})
dados_empilhado["parametros"] = dados_empilhado["parametros"].replace(
    rotulo_parametros
)
dados_pizza = df_2025[["id_municipio_nome", "ano", "mes"]].rename(columns={"id_municipio_nome": "Cidade"})
dados_radar = dados_empilhado.rename(columns={"Valor": "Nota"})


opcao = st.sidebar.radio("Visualização", ["Tabela", "Gráficos"])

if opcao == "Tabela":
    st.header("Tabela filtrada")
    st.write(f"{len(df)} registros de origem; {len(df_tabela)} após o filtro.")
    st.dataframe(df_tabela, width="stretch", hide_index=True)
    with st.expander("Tabelas respostas"):
        st.dataframe(dados_empilhado, width="stretch", hide_index=True)
        st.dataframe(dados_pizza, width="stretch", hide_index=True)
        st.dataframe(dados_radar, width="stretch", hide_index=True)
