import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.title('Painel do Covid por cidade')
st.header('Dados captados da base de dados brasileira disponível em: https://covid.saude.gov.br/')

test = pd.read_csv('./HIST_PAINEL_COVIDBR_02dez2020.csv', sep=";",error_bad_lines=False)


with open('./dict.p', 'rb') as fp:
    mun = pickle.load(fp)

choice = st.selectbox(
     "Escolha seu município",
    mun['codmun'].keys())


st.write(' Sua cidade escolhida foi: ', mun['codmun'][choice])

if st.checkbox('Gerar data frame'):

    index  = [
        'regiao','municipio',
         'codmun','data','semanaEpi',
         'populacaoTCU2019','casosAcumulado',
         'casosNovos','obitosAcumulado',
         'obitosNovos','Recuperadosnovos',
         'emAcompanhamentoNovos']

    cit = test[index].where(test['codmun']  == mun['codmun'][choice])
    cit.dropna(subset=['codmun'], inplace=True)
    st.write(cit)

    if (st.checkbox('Obitos novos por casos novos')):
        obitos = cit[['casosNovos','obitosNovos']]
        st.line_chart(obitos)

    semana  = cit.groupby('semanaEpi', as_index=False)[['casosNovos','obitosNovos']].mean()
    st.write('Média de casos novos  e obitos novos por semana epidemiológica')
    st.line_chart(semana[['casosNovos','obitosNovos']])
    semana  = cit.groupby('semanaEpi', as_index=False)[['casosNovos','obitosNovos']].sum()
    st.write('Total de mortes ' + str(semana['obitosNovos'].sum()))
    st.line_chart(semana['obitosNovos'])
    st.write('Total de casos ' + str(semana['casosNovos'].sum()))
    st.line_chart(semana['casosNovos'])
