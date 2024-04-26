import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import re

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
    st.title("Welcome to the Cocktail Connoisseur App!")
    st.markdown("""
        Welcome to the **Cocktail Connoisseur App**, your gateway to mastering the art of cocktail making. 
        By using this app, you'll not only broaden your drinking horizons and refine your palate but also dazzle your friends with your newfound mixology skills.
        
        This app was crafted by three university students eager to expand their horizons beyond the routine gin and tonics and screwdrivers. 
        Through developing this app, they broke free from the mundane, embracing a world of vibrant and diverse cocktails.
        
        ## How Does This App Work?
        - **Search Function**: Allows you to look up a cocktail by name. If it exists in our extensive database, you can view detailed information.
        - **Filter Function**: Enables you to find cocktails based on specific criteria such as the number of ingredients, preferred alcohol base, and desired glassware.
        
        Dive in and start exploring the rich world of cocktails with us!
    """)

def display_cocktail_search(df):
    st.title("Cocktail Search")
    search_query = st.text_input("Search for a cocktail")
    if search_query:
        results = df[df['Cocktail Name'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            st.subheader("Search Results:")
            for index, row in results.iterrows():
                display_cocktail_info(row)
        else:
            st.write("No cocktails found with that name.")

def display_cocktail_filter(df):
    st.title("Cocktail Filter")
    num_ingredients = st.selectbox("Number of Ingredients", options=['Any'] + list(range(1, 11)))
    glassware_options = ['Any'] + sorted(df['Glassware'].dropna().unique().tolist())
    glassware = st.selectbox("Type of Glassware", options=glassware_options)
    
    st.write("Select additional alcohols to add to your cabinet:")
    alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                     'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']
    cols = st.columns(4)
    quarter = len(alcohol_bases) // 4
    for i in range(4):
        with cols[i]:
            for alcohol in alcohol_bases[i * quarter: (i + 1) * quarter + (0 if i < 3 else len(alcohol_bases) % 4)]:
                if st.checkbox(alcohol, key=f"filter_{alcohol}", value=alcohol in st.session_state.get('my_liquor_cabinet', [])):
                    if alcohol not in st.session_state['my_liquor_cabinet']:
                        st.session_state['my_liquor_cabinet'].append(alcohol)

    if st.button('Update and Save Cabinet'):
        st.session_state['my_liquor_cabinet'] = [alcohol for alcohol in alcohol_bases if st.session_state.get(f"filter_{alcohol}", False)]
        st.success('Your liquor cabinet has been updated!')

    if st.button('Display Cocktails'):
        filtered_df = df.copy()
        if num_ingredients != 'Any':
            filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == int(num_ingredients))]
        if glassware != 'Any':
            filtered_df = filtered_df[filtered_df['Glassware'] == glassware]
        
        alcohol_regex = '|'.join([re.escape(alcohol) for alcohol in st.session_state.get('my_liquor_cabinet', [])])
        filtered_df = filtered_df[filtered_df['Ingredients'].str.contains(alcohol_regex, case=False, na=False)]

        if not filtered_df.empty:
            for index, row in filtered_df.iterrows():
                display_cocktail_info(row)
        else:
            st.write("No cocktails match your filters.")

def manage_liquor_cabinet():
    st.title('Manage Your Liquor Cabinet')
    alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                     'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']
    cols = st.columns(4)
    per_column = len(alcohol_bases) // 4
    remainder = len(alcohol_bases) % 4
    for i, col in enumerate(cols):
        with col:
            start_index = i * per_column
            end_index = start_index + per_column + (1 if i < remainder else 0)
            for alcohol in alcohol_bases[start_index:end_index]:
                st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.get('my_liquor_cabinet', []))
    if st.button('Save Liquor Cabinet'):
        st.session_state['my_liquor_cabinet'] = [alcohol for alcohol in alcohol_bases if st.session_state.get(alcohol, False)]
        st.success('Your liquor cabinet has been updated!')

def display_favorites(df):
    st.title("My Favorites")
    if 'favorites' in st.session_state and st.session_state['favorites']:
        for cocktail in st.session_state['favorites']:
            st.write(cocktail)

        total_cocktails = len(df)
        liked_cocktails = len(st.session_state['favorites'])
        labels = ['Liked Cocktails', 'Total Cocktails']
        sizes = [liked_cocktails, total_cocktails - liked_cocktails]
        explode = (0.1, 0)
        colors = ['#ffcc99', '#66b3ff']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)

        # Alcohol base distribution pie chart
        base_count = {base: 0 for base in alcohol_bases}
        for base in alcohol_bases:
            for cocktail in st.session_state['favorites']:
                if base in df.loc[df['Cocktail Name'] == cocktail, 'Ingredients'].values[0]:
                    base_count[base] += 1

        bases = [base for base in base_count if base_count[base] > 0]
        counts = [base_count[base] for base in bases]
        fig2, ax2 = plt.subplots()
        ax2.pie(counts, labels=bases, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig2)

        if st.button('Refresh'):
            st.session_state['favorites'] = []

    else:
        st.write("You haven't liked any cocktails yet.")

def display_cocktail_info(row):
    st.write(f"Cocktail Name: {row['Cocktail Name']}")
    st.write(f"Ingredients: {row['Ingredients']}")
    like_key = f"like_{row['Cocktail Name']}"
    if st.button("Like", key=like_key):
        if row['Cocktail Name'] not in st.session_state.get('favorites', []):
            st.session_state.setdefault('favorites', []).append(row['Cocktail Name'])
    st.write("")  # Empty line for spacing

def main():
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
