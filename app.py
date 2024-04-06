import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Function to load data from a URL
def load_data(url):
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# URL of the CSV file
csv_url = 'https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv'

# Load data
df = load_data(csv_url)

# Streamlit UI
st.title('Cocktail Finder')

# User inputs
num_ingredients = st.number_input('Number of Ingredients', min_value=1, max_value=20, value=3)
alcohol_base = st.text_input('Type of Alcohol Base').lower()
glassware = st.selectbox('Select Glassware', ['Coupe', 'Martini', 'Tin Cup'])

# Filtering based on the presence of the alcohol base in the 'Ingredients' column
filtered_df = df[df['Ingredients'].str.lower().str.contains(alcohol_base)]

# Filtering for cocktails that match the user-specified number of ingredients
filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == num_ingredients)]

# Filtering based on the 'Glassware' selection
filtered_df = filtered_df[filtered_df['Glassware'] == glassware]

# Display results
if not filtered_df.empty:
    st.write(filtered_df)
else:
    st.write('No cocktails found.')
