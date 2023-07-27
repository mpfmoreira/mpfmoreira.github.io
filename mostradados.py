import streamlit as st
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from datetime import timedelta

def lerSite(inicio,fim,user,mot):
    DATA_URL = "http://www.md-alliance.com.br:9080/pontal/"
    driver = webdriver.Chrome()
    driver.get(DATA_URL)
    driver.implicitly_wait(0.5)

    ousuario = driver.find_element(by=By.NAME, value="usuario")
    asenha = driver.find_element(by=By.ID, value="password")

    ousuario.send_keys(user)
    asenha.send_keys(mot)
    d1 = driver.find_element(by=By.CLASS_NAME, value="panel-footer")
    d2 = d1.find_element(by=By.CLASS_NAME, value="pull-right")
    lista = d2.find_elements(by=By.TAG_NAME, value="input")
    submit_input = lista[0]
    time.sleep(2)

    x = submit_input.click()

    driver.switch_to.new_window('tab')
    time.sleep(5)
    parte1="http://www.md-alliance.com.br:9080/pontal/extratotable.php?conta=5"
    parte2="&empresa=0"
    parte3="&cr=0&bem=0&contrato=0&inicio="+inicio+"&fim="+fim
    parte4="&credito=true&debito=true&programado=true&previsto=true&efetuado=true&boleto=true"
    DATA_URL = parte1 + parte2 + parte3 + parte4
    driver.get(DATA_URL)
    driver.implicitly_wait(0.5)
    fonte = driver.page_source
    driver.quit()
    return fonte

def highlight_data(val):
    color = 'lightgrey'
    return f'background-color: {color}'

st.title('Mostra dados')

with st.expander("credenciais"):
    with st.form("dadosacesso"):
        umalinha = st.columns([2,2])
        usuario = umalinha[0].text_input("Email", placeholder="usuário: ")
        senha = umalinha[1].text_input("Senha", placeholder="senha", type="password")
        login_button = st.form_submit_button("OK")

with st.form("Intervalo"):


    outralinha = st.columns([2,2,1])
    outralinha[0].write("Periodo no formato aaaa/mm/dd")
    d = outralinha[1].date_input(
        "",[datetime.date(2023, 6, 30),datetime.date(2023, 7, 6)],label_visibility="collapsed")
    submitted = outralinha[2].form_submit_button("Bora lá?","vai?")

if submitted:
    if 5 > 4 :
        source = lerSite(d[0].strftime("%Y-%m-%d"),d[1].strftime("%Y-%m-%d"),usuario,senha)
        lista = pd.read_html(source,thousands=None)
    else:
### na lista estão todas as planilhas do arquivo. Neste caso, é só uma
        lista = pd.read_html('/Users/mpedro/myproject/teste5.html',thousands=None)


    df = lista[0]
#    st.write(df)
###  troca pontos e vírgulas. Acrescenta cabeçalho que está em branco
    df["Valor"] = df["Valor"].str.replace(".","",regex=False)
    df["Valor"] = df["Valor"].str.replace(",",".",regex=True)
    df["Valor"] = df["Valor"].astype(float)
    df["Valor"] = df["Valor"].replace(np.nan,0,regex=True)
    df.columns.values[5:8] = 'aa','bb','cc'
    df.rename(columns={'aa':"a",'bb':"b",'cc':"c"},inplace=True)

    dx=pd.to_datetime('30/12/1899',format="%d/%m/%Y")
    df["Data"] = (pd.to_datetime(df["Data"], format="%d/%m/%Y") - dx) / timedelta(days=1)

###  df2 é a nova planilha que queremos construir
    df2 = df.loc[:,["Data","PC","Histórico","CR","Valor","Favorecido","Recebedor","a","b","c","Status"]]

###  acerta df2 com: CR Downtown; ajeita o plano de contas para poder ordenar; preenche datas boletos
    x = df2["PC"]
    z = df2["CR"].isnull()
    semdata = df2["Data"].isnull()
    for i in range(1,x.size):
        if semdata[i]:
            df2.at[i,"Data"] = df2.at[(i-1),"Data"]

        if z[i]:
            df2.at[i,"CR"] = "Downtown"
        y=str(x[i]).split(".")
        if len(y[0])==1:
            y[0]="0"+y[0]
        if len(y[1])==1:
            y[1]="0"+y[1]
        if len(y[2])==1:
            y[2]="0"+y[2]
        df2.at[i,"PC"] = ".".join(y)
        temp = df2.at[i,"Histórico"]

        if temp[0:15] == "Boleto Desconto":
            temp = temp[7:100]
            df2.at[i,"Histórico"] = temp

        if temp[0:8] == "Desconto":
            f = temp.rfind("R$")
            Svalor = temp[(f+3):100].replace(".","").replace(",",".")
            df2.at[i,"Valor"] = -float(Svalor)
            df2.at[i,"PC"] = "01.01.02"
            df2.at[i,"a"] = "Entradas Operacionais"
            df2.at[i,"b"] = "Aluguel"
            df2.at[i,"c"] = "Desconto de aluguel mensal"
            dia = df2.at[i,"Data"]
            df2.loc[(i-0.5)] = [dia,'..','Boleto','','','','','','','','']
### ordena df2
    df2 = df2.sort_index().reset_index(drop=True)
    df2["Data"] = df2["Data"].astype(int) + 693594
### somei 693594 para converter a data de excel para pandas
    df2["Data"] = pd.to_datetime(df2["Data"].apply(datetime.datetime.fromordinal),format='%d/%m/%y').dt.strftime('%d/%m/%y')
    st.dataframe(df2.style.applymap(highlight_data,subset=['Data']))




# https://mpfmoreira-meuuber.streamlit.app/
