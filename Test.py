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

# Streamlit UI setup
st.title('Choose your liquor cabinet')

# Multi-select box for choosing liquors
selected_liquors = st.multiselect('Select your liquors:', options=['Whisky', 'Vodka', 'Tequila', 'Gin'])

# Function to filter cocktails based on selected liquors
def filter_cocktails(dataframe, liquors):
    if liquors:
        mask = dataframe['Ingredients'].str.contains('|'.join([liquor for liquor in liquors]), case=False, na=False)
        filtered_df = dataframe[mask]
        return filtered_df
    return pd.DataFrame()

# Apply filter
filtered_df = filter_cocktails(df, selected_liquors)

# Select only the necessary columns
columns_to_display = ['Cocktail Name', 'Ingredients', 'Garnish', 'Notes']
filtered_df = filtered_df[columns_to_display]

# Randomly select 10 cocktails if there are enough
if not filtered_df.empty:
    if len(filtered_df) > 10:
        sampled_df = filtered_df.sample(n=10)
        st.table(sampled_df)
    else:
        st.table(filtered_df)
else:
    st.write("No cocktails found with the selected liquors.")
