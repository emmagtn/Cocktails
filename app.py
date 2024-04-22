import streamlit as st
import pandas as pd
import requests
from io import StringIO
import random
import re

def load_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def display_welcome_message():
    st.title("Hello Mixologist")
    st.write("""
        Welcome to our cocktail exploration tool! Here you can search for cocktails,
        filter by various criteria, or even manage your own virtual liquor cabinet.
        Choose a tab to get started and discover the perfect mix for your next gathering.
    """)

def display_cocktail_search(df):
    st.title("Cocktail Search")
    search_query = st.text_input("Search for a cocktail")
    if search_query:
        results = df[df['Cocktail Name'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            st.subheader("Search Results:")
            for index, row in results.iterrows():
                st.text(f"Cocktail Name: {row['Cocktail Name']}")
                st.text(f"Ingredients: {row['Ingredients']}")
                st.text("")  # Empty line for spacing
        else:
            st.write("No cocktails found with that name.")

def display_cocktail_filter(df):
    st.title("Cocktail Filter")
    # Inputs for filtering
    num_ingredients = st.selectbox("Number of Ingredients", options=['Any'] + list(range(1, 11)))
    glassware_options = ['Any'] + sorted(df['Glassware'].dropna().unique().tolist())
    glassware = st.selectbox("Type of Glassware", options=glassware_options)
    
    # Alcohol selection for filter, adding to the cabinet
    st.write("Select additional alcohols to add to your cabinet:")
    alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                     'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']
    col1, col2 = st.columns(2)
    half = len(alcohol_bases) // 2
    with col1:
        for alcohol in alcohol_bases[:half]:
            if st.checkbox(alcohol, key=f"filter_{alcohol}", value=alcohol in st.session_state.get('my_liquor_cabinet', [])):
                if alcohol not in st.session_state['my_liquor_cabinet']:
                    st.session_state['my_liquor_cabinet'].append(alcohol)
    with col2:
        for alcohol in alcohol_bases[half:]:
            if st.checkbox(alcohol, key=f"filter_{alcohol}", value=alcohol in st.session_state.get('my_liquor_cabinet', [])):
                if alcohol not in st.session_state['my_liquor_cabinet']:
                    st.session_state['my_liquor_cabinet'].append(alcohol)

    # Save and display buttons
    if st.button('Update and Save Cabinet'):
        st.session_state['my_liquor_cabinet'] = [alcohol for alcohol in alcohol_bases if st.session_state.get(f"filter_{alcohol}", False)]
        st.success('Your liquor cabinet has been updated!')

    if st.button('Display Cocktails'):
        # Filtering logic
        filtered_df = df.copy()
        if num_ingredients != 'Any':
            filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == num_ingredients)]
        if glassware != 'Any':
            filtered_df = filtered_df[filtered_df['Glassware'] == glassware]
        
        # Ensure at least one of the selected alcohol bases is in the ingredients
        alcohol_regex = '|'.join([re.escape(alcohol) for alcohol in st.session_state.get('my_liquor_cabinet', [])])
        filtered_df = filtered_df[filtered_df['Ingredients'].str.contains(alcohol_regex, case=False, na=False)]

        # Randomly select up to 5 cocktails to display
        if not filtered_df.empty:
            sample_df = filtered_df.sample(min(len(filtered_df), 5))
            for index, row in sample_df.iterrows():
                st.write(f"Cocktail Name: {row['Cocktail Name']}")
                st.write(f"Ingredients: {row['Ingredients']}")
                st.write(f"Glassware: {row['Glassware']}")
                st.write("")
        else:
            st.write("No cocktails match your filters.")

def manage_liquor_cabinet():
    st.title('Manage Your Liquor Cabinet')
    
    alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                     'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']
    
    col1, col2 = st.columns(2)
    half = len(alcohol_bases) // 2
    with col1:
        for alcohol in alcohol_bases[:half]:
            st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.get('my_liquor_cabinet', []))
    with col2:
        for alcohol in alcohol_bases[half:]:
            st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.get('my_liquor_cabinet', []))

    if st.button('Save Liquor Cabinet'):
        st.session_state['my_liquor_cabinet'] = [alcohol for alcohol in alcohol_bases if st.session_state.get(alcohol, False)]
        st.success('Your liquor cabinet has been updated!')

def main():
    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "Cocktail Search", "Cocktail Filter", "Manage Liquor Cabinet"])
    if selected_tab == "Hello Mixologist":
        display_welcome_message()
    elif selected_tab == "Cocktail Search":
        display_cocktail_search(df)
    elif selected_tab == "Cocktail Filter":
        display_cocktail_filter(df)
    elif selected_tab == "Manage Liquor Cabinet":
        manage_liquor_cabinet()

if __name__ == "__main__":
    main()
