import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import re

# Define alcohol_bases globally
alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                 'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']

def load_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")
        return pd.DataFrame()

def display_welcome_message():
    st.title('Welcome to the Cocktail Connoisseur App')

    st.markdown('''
    Dive into the art of cocktail making and expand your mixology horizons with the Cocktail Connoisseur App! 
    Whether you're looking to dazzle your friends with your newfound skills or simply enjoy exploring new flavors, 
    this app is your ultimate guide.

    **By using this app, you can:**
    - Broaden your drinking repertoire.
    - Refine your palate.
    - Impress friends with your mixology prowess.

    **Our Story:**
    Seven business students, eager to move beyond basic gin and tonics and screwdrivers, created this app. 
    Their goal? To explore the sophisticated world of cocktails and share their passion with like-minded enthusiasts.

    **How Does This App Work?**
    - **Search Function**: Look up any cocktail by name. If it’s in our extensive database, you'll find detailed information about it.
    - **Filter Function**: Find cocktails based on specific criteria such as ingredient count, preferred alcohol base, 
    available liquor in your cabinet, and desired glassware.
    - **Manage Liquor Cabinet**: This feature lets you monitor and manage the contents of your liquor cabinet effortlessly.
    - **My Favorites**: Keep track of your favorite cocktails and see statistics on your preferences, including a 
    detailed pie chart showing your favorite alcohol bases.

    Embark on your mixology journey with us and start exploring the rich world of cocktails today!
    ''')


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
                like_key = f"like_{row['Cocktail Name']}_{index}"  # Append index to make the key unique
                if st.button("Like", key=like_key):
                    if row['Cocktail Name'] not in st.session_state.favorites:
                        st.session_state.favorites.append(row['Cocktail Name'])
                st.text("")  # Empty line for spacing
        else:
            st.write("No cocktails found with that name.")

def display_cocktail_filter(df):
    st.title("Cocktail Filter")
    num_ingredients = st.selectbox("Number of Ingredients", options=['Any'] + list(range(1, 11)))
    glassware_options = ['Any'] + sorted(df['Glassware'].dropna().unique().tolist())
    glassware = st.selectbox("Type of Glassware", options=glassware_options)
    
    st.write("Select additional alcohols to add to your cabinet:")
    cols = st.columns(4)
    quarter = len(alcohol_bases) // 4
    for i in range(4):
        with cols[i]:
            for alcohol in alcohol_bases[i * quarter: (i + 1) * quarter + (0 if i < 3 else len(alcohol_bases) % 4)]:
                if st.checkbox(alcohol, key=f"filter_{alcohol}", value=alcohol in st.session_state.my_liquor_cabinet):
                    if alcohol not in st.session_state.my_liquor_cabinet:
                        st.session_state.my_liquor_cabinet.append(alcohol)

    display_cocktails = st.button('Display Cocktails')
    if display_cocktails or st.session_state.get('display_cocktails', False):
        st.session_state['display_cocktails'] = True
        
        filtered_df = df.copy()
        if num_ingredients != 'Any':
            filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == int(num_ingredients))]
        if glassware != 'Any':
            filtered_df = filtered_df[filtered_df['Glassware'] == glassware]
        
        alcohol_regex = '|'.join([re.escape(alcohol) for alcohol in st.session_state.my_liquor_cabinet])
        filtered_df = filtered_df[filtered_df['Ingredients'].str.contains(alcohol_regex, case=False, na=False)]

        if not filtered_df.empty:
            st.subheader("Search Results:")
            for index, row in filtered_df.iterrows():
                st.text(f"Cocktail Name: {row['Cocktail Name']}")
                st.text(f"Ingredients: {row['Ingredients']}")
                like_key = f"like_{row['Cocktail Name']}_{index}"
                if st.button("Like", key=like_key):
                    if row['Cocktail Name'] not in st.session_state.favorites:
                        st.session_state.favorites.append(row['Cocktail Name'])
                st.text("")  # Empty line for spacing
        else:
            st.write("No cocktails match your filters.")

def manage_liquor_cabinet():
    st.title('Manage Your Liquor Cabinet')
    cols = st.columns(4)
    per_column = len(alcohol_bases) // 4
    remainder = len(alcohol_bases) % 4
    for i, col in enumerate(cols):
        with col:
            start_index = i * per_column
            end_index = start_index + per_column + (1 if i < remainder else 0)
            for alcohol in alcohol_bases[start_index:end_index]:
                st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.my_liquor_cabinet)
    if st.button('Save Liquor Cabinet'):
        st.session_state.my_liquor_cabinet = [alcohol for alcohol in alcohol_bases if st.session_state.get(alcohol, False)]
        st.success('Your liquor cabinet has been updated!')

def display_favorites(df):
    st.title("My Favorites")
    if 'favorites' in st.session_state and st.session_state.favorites:
        st.subheader("Liked Cocktails:")
        for favorite in st.session_state.favorites:
            st.write(favorite)

        total_cocktails = len(df)
        liked_cocktails = len(st.session_state.favorites)
        labels = ['Liked Cocktails', 'Total Cocktails']
        sizes = [liked_cocktails, total_cocktails - liked_cocktails]
        explode = (0.1, 0)
        colors = ['#ffcc99', '#66b3ff']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)

        base_count = {base: 0 for base in alcohol_bases}
        for cocktail in st.session_state.favorites:
            ingredients = df.loc[df['Cocktail Name'] == cocktail, 'Ingredients'].values[0]
            for base in alcohol_bases:
                if base.lower() in ingredients.lower():
                    base_count[base] += 1

        bases = [base for base in base_count if base_count[base] > 0]
        counts = [base_count[base] for base in bases]
        fig2, ax2 = plt.subplots()
        ax2.pie(counts, labels=bases, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.markdown("### You are made of:")  # Using markdown to style the header similarly
        st.pyplot(fig2)

        if st.button('Reset Likes'):
            st.session_state.favorites = []
            st.success('Your liked cocktails have been reset!')
    else:
        st.write("You haven't liked any cocktails yet.")

def main():
    # Initialize session state if it hasn't been initialized already
    if 'my_liquor_cabinet' not in st.session_state:
        st.session_state['my_liquor_cabinet'] = []
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "Cocktail Search", "Cocktail Filter", "Manage Liquor Cabinet", "My Favorites"])

    if selected_tab == "Hello Mixologist":
        display_welcome_message()
    elif selected_tab == "Cocktail Search":
        display_cocktail_search(df)
    elif selected_tab == "Cocktail Filter":
        display_cocktail_filter(df)
    elif selected_tab == "Manage Liquor Cabinet":
        manage_liquor_cabinet()
    elif selected_tab == "My Favorites":
        display_favorites(df)

if __name__ == "__main__":
    main()
