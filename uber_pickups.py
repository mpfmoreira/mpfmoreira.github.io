import streamlit as st
import pandas as pd
import numpy as np

import time
from selenium import webdriver
def lerSite():
    DATA_URL = "http://www.md-alliance.com.br:9080/pontal/"
    driver = webdriver.Chrome()
    driver.get(DATA_URL)
    driver.implicitly_wait(0.5)

    ousuario = driver.find_element(by=By.NAME, value="usuario")
    asenha = driver.find_element(by=By.ID, value="password")

    ousuario.send_keys("mpfm")
    asenha.send_keys("mpfm")
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
    parte3="&cr=0&bem=0&contrato=0&inicio=2023-03-09&fim=2023-04-07"
    parte4="&credito=true&debito=true&programado=true&previsto=true&efetuado=true&boleto=true"
    DATA_URL = parte1 + parte2 + parte3 + parte4
    driver.get(DATA_URL)
    driver.implicitly_wait(0.5)
    fonte = driver.page_source
    driver.quit()
    return fonte
source = lerSite()
lista = pd.read_html(source,thousands=None)
df = lista[0]
st.write(df)

st.title('Corridas do Uber em Nova Iorque')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Mostre dados originais'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# https://mpfmoreira-mpfmoreira-github-io-uber-pickups-oqz4hs.streamlit.app/
