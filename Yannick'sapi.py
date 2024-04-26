import streamlit as st
import pandas as pd
import requests
from io import StringIO
import random

# Function to load data from a URL
def load_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            return df
        else:
            st.error("Failed to fetch data: HTTP " + str(response.status_code))
            return pd.DataFrame()  # Return empty DataFrame if not successful
    except Exception as e:
        st.error("An error occurred: " + str(e))
        return pd.DataFrame()  # Return empty DataFrame on error

# URL of the CSV file
csv_url = 'https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv'

# Load data
df = load_data(csv_url)

# Initialize session state for liquor cabinet
if 'my_liquor_cabinet' not in st.session_state:
    st.session_state['my_liquor_cabinet'] = []

# Streamlit UI setup
st.title('Choose your liquor cabinet')

# Multi-select box for choosing liquors
selected_liquors = st.multiselect('Select your liquors:', options=['Whisky', 'Vodka', 'Tequila', 'Gin'])

# Button to save the selection
if st.button('Save Selection'):
    st.session_state['my_liquor_cabinet'] = selected_liquors
    st.success('Your liquor cabinet has been updated!')

# Display the current contents of the liquor cabinet
st.write('Your current liquor cabinet contains:', st.session_state['my_liquor_cabinet'])
