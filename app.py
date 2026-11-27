from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Prova Final Python", layout="wide")
st.title("Gráficos de pizza - Total veículos municípios")

PASTA = Path(__file__).resolve().parent
parametros = ["id_municipio_nome", "tipo_veiculo", "quantidade"]

st.sidebar.header("Controles")
formato = st.sidebar.radio("Arquivo de exemplo", ["CSV", "Excel (.xlsx)"])

try:
    if formato == "CSV":
        df = pd.read_csv(PASTA / "numero_veiculos.csv", encoding="utf-8")
    else:
      
        df = pd.read_excel(PASTA / "numero_veiculos.xlsx", engine="openpyxl")

    obrigatorias = ["ano", "mes", "sigla_uf"] + parametros
    faltando = [coluna for coluna in obrigatorias if coluna not in df.columns]
    if faltando:
        st.error(f"Colunas ausentes no arquivo: {faltando}")
        st.stop()

  
    for coluna in ["ano", "mes", "quantidade"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="raise")

    if df[obrigatorias].isna().any().any():
        st.error("Há células vazias nas colunas usadas. Confira o arquivo.")
        st.stop()

except (OSError, ValueError, ImportError) as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()

# 1. Filtra diretamente pela string "Belo Horizonte" na coluna 'id_municipio_nome'
df_filtrado = df[df["id_municipio_nome"] == "Belo Horizonte"].copy()

# Ordena pelos nomes exatos das colunas
df_filtrado = df_filtrado.sort_values(["id_municipio_nome", "ano", "mes"])
df_tabela = df_filtrado[
    ["id_municipio_nome", "ano", "mes", "tipo_veiculo", "quantidade"]
].copy()

if df_filtrado.empty:
    st.warning("Nenhuma linha encontrada para Belo Horizonte. Confira o arquivo.")
    st.stop()

df_2025 = df_filtrado[
    (df_filtrado["ano"] == 2025) & (df_filtrado["mes"] == 12)
].copy()

dados_pizza = (
    df_2025.groupby("tipo_veiculo", as_index=False)["quantidade"]
    .sum()
    .rename(columns={"tipo_veiculo": "Tipo de Veículo", "quantidade": "Total"})
)

opcao = st.sidebar.radio("Visualização", ["Tabela", "Gráficos"])

if opcao == "Tabela":
    st.header("Tabela filtrada - Belo Horizonte")
    st.write(f"{len(df)} registros de origem; {len(df_tabela)} após o filtro.")
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

    with st.expander("Dados de Dezembro/2025 (Base do Gráfico)"):
        st.dataframe(dados_pizza, use_container_width=True, hide_index=True)

elif opcao == "Gráficos":
    st.header("Distribuição de Veículos - Belo Horizonte (Dez/2025)")

    if dados_pizza.empty:
        st.warning("Não há dados registrados para Belo Horizonte em Dezembro de 2025.")
    else:
        fig_pizza = px.pie(
            dados_pizza,
            names="Tipo de Veículo",
            values="Total",
            title="Proporção por Tipo de Veículo em Belo Horizonte (12/2025)",
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
