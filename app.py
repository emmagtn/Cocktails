import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Function to load data from a URL
def load_data(url):
    # Assuming the CSV is accessible at a URL
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# URL of the CSV file (Update with the actual URL)
csv_url = 'https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv'

# Load data
df = load_data(csv_url)

# Streamlit UI
st.title('Cocktail Finder')




st.header("Helklllo")

st. button("hello")

st. button("Yannick")

st. button("yoyostreak")

st.button("Click here Willy")
st.markdown("Hi there")

