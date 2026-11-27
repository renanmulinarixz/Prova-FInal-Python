import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

dados = pd.read_csv(Path(__file__).parent / 'numero_veiculos.csv')
cidades = ['Belo Horizonte', 'Betim', 'Contagem']
dados = dados[(dados['ano'] == 2025) & (dados['mes'] == 12) & (dados['id_municipio_nome'].isin(cidades))]
dados = dados[['id_municipio_nome', 'tipo_veiculo', 'quantidade']]
dados = dados.groupby(['id_municipio_nome', 'tipo_veiculo'], as_index=False)['quantidade'].sum()

st.title('Frota de veículos')
opcao = st.sidebar.radio('Visualização', ['Tabela', 'Gráficos'])

if opcao == 'Tabela':
    st.header('Tabela de veículos')
    st.dataframe(dados)
else:
    st.header('Gráficos de veículos')
    for cidade in cidades:
        tabela = dados[(dados['id_municipio_nome'] == cidade) & (dados['quantidade'] > 0)]
        grafico = px.pie(tabela, names='tipo_veiculo', values='quantidade', title=cidade)
        st.plotly_chart(grafico)

    st.header('Gráficos extras')
    st.plotly_chart(px.box(dados, x='id_municipio_nome', y='quantidade', title='Distribuição por município'))
    st.plotly_chart(px.box(dados, x='tipo_veiculo', y='quantidade', title='Distribuição por tipo de veículo'))
    totais = dados.groupby('id_municipio_nome', as_index=False)['quantidade'].sum()
    st.plotly_chart(px.bar(totais, x='id_municipio_nome', y='quantidade', title='Total de veículos por município'))

st.write('Fonte: https://basedosdados.org/')
st.write('Janaína, bom trabalho! Obrigado pela ajuda nos estudos para a prova!')
