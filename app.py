import streamlit as st
import numpy as np
import pandas as pd
import pickle
import base64

st.title('Painel do Covid por cidade')
st.header('Dados captados da base de dados brasileira disponível em: https://covid.saude.gov.br/')

test = pd.read_csv('./HIST_PAINEL_COVIDBR_02dez2020.csv', sep=";",error_bad_lines=False)

#municipios = df[['municipio','codmun']].groupby('municipio', as_index=True

with open('./dict.p', 'rb') as fp:
    mun = pickle.load(fp)

choice = st.selectbox(
     "Escolha seu município",
    mun['codmun'].keys())


st.write(' Sua cidade escolhida foi: ', mun['codmun'][choice])


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download csv file</a>'
    return href

if st.checkbox('Gerar data frame'):

    index  = [
        'regiao','municipio',
         'codmun','data','semanaEpi',
         'populacaoTCU2019','casosAcumulado',
         'casosNovos','obitosAcumulado',
         'obitosNovos']

    cit = test[index].where(test['codmun']  == mun['codmun'][choice])
    cit.dropna(subset=['codmun'], inplace=True)
    st.write(cit)

    if (st.checkbox('Obitos novos por casos novos')):
        obitos = cit[['casosNovos','obitosNovos']]
        st.line_chart(obitos)

    semana  = cit.groupby('semanaEpi', as_index=True)[['casosNovos','obitosNovos']].mean()
    st.write('Média de casos novos  e óbitos novos por semana epidemiológica')
    st.line_chart(semana[['casosNovos','obitosNovos']])
    semana  = cit.groupby('semanaEpi', as_index=True)[['casosNovos','obitosNovos']].sum()
    st.write('Maior número de infectados por semana ', semana['casosNovos'].max())
    st.write('Maior número de óbitos por semana ', semana['obitosNovos'].max())
    st.write('Rank das semanas com maior numero de infecção')
    st.write(semana.nlargest(10,'casosNovos'))
    st.write('Rank das semanas com menor número de infecção')
    st.write(semana.nsmallest(10,'casosNovos'))
    st.write('Total de mortes ' + str(semana['obitosNovos'].sum()))
    st.line_chart(semana['obitosNovos'])
    st.write('Total de casos ' + str(semana['casosNovos'].sum()))
    st.line_chart(semana['casosNovos'])
    if (st.checkbox('Salvar Data Frame')):
        st.markdown(get_table_download_link(cit), unsafe_allow_html=True)