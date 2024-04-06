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

# User inputs
num_ingredients = st.number_input('Number of Ingredients', min_value=1, max_value=10, value=3)
alcohol_base = st.text_input('Type of Alcohol Base').lower()
tool = st.selectbox('Uses a Strainer or Shaker', ['Strainer', 'Shaker', 'Either']).lower()

# Filter based on inputs
# Adjusting for 'ingredients' as the column for the type of alcohol base
filtered_df = df[df['ingredients'].str.lower().str.contains(alcohol_base)]

if tool != 'either':
    filtered_df = filtered_df[filtered_df['Tool'].str.lower() == tool]

filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == num_ingredients)]

# Display results
if not filtered_df.empty:
    st.write(filtered_df)
else:
    st.write('No cocktails found.')