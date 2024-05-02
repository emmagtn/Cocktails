#accessing databases by importing them 
import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import re


# Defining alcohol_bases globally as a list. Our API was analyzed manually to determine which alocohols bases were mentioned.
alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                 'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']

#activating functions from our imports
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

#Opening tab (Tab 1): Welcome to the App. Images and text. 
def display_welcome_message():
    st.title('Welcome to the Cocktail Connoisseur App')

    # Displaying an image of a cocktail bar with the provided URL
    image_url = 'https://media.guestofaguest.com/t_article_content/gofg-media/2020/02/1/53239/83688932_1183344105191648_3383560581132931295_n_(3).jpg'
    st.image(image_url, caption='Elegant Cocktail Bar')

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
    ''') #long and personal introduction to our project. Plus description of how to navigate through our website

#Tab 2: My Liquor Cabinet. 
#The following code calls back to our alcohol list on line 11-12 'alcohol bases'
def manage_liquor_cabinet():
    st.title('Manage Your Liquor Cabinet')
    cols = st.columns(4)
    per_column = len(alcohol_bases) // 4 #Line 64 and 65 are for aesthetic purposes; It arranges our clickable buttons in a 4x4 manner
    remainder = len(alcohol_bases) % 4
    for i, col in enumerate(cols):
        with col:
            start_index = i * per_column
            end_index = start_index + per_column + (1 if i < remainder else 0)
            for alcohol in alcohol_bases[start_index:end_index]:
                st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.my_liquor_cabinet)
    if st.button('Save Liquor Cabinet'): #this button saves the selection of alcohols in the cabinet. It allows us to find this information later on for other pages.
        st.session_state.my_liquor_cabinet = [alcohol for alcohol in alcohol_bases if st.session_state.get(alcohol, False)]
        st.success('Your liquor cabinet has been updated!')

#Tab 3: Cocktail Search
#Allows the user to search for any cocktail by accessing our API through a search query tab
def display_cocktail_search(df):
    st.title("Cocktail Search")
    search_query = st.text_input("Search for a cocktail")
    if search_query:
        results = df[df['Cocktail Name'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            st.subheader("Search Results:")
            for index, row in results.iterrows(): #this function outputs our data
                with st.expander(f"{row['Cocktail Name']}"): #the expander allows us to expand the selection upon click (when clicking the cocktail title, you will get the whole recipe)
                    #split ingredients in string
                    ingredients_list = row['Ingredients'].split(',')
                    # Displaying ingredients in a bulleted list
                    st.write("**Ingredients:**")
                    for ingredient in ingredients_list:
                        st.write(f"- {ingredient.strip()}")  # .strip() removes any leading/trailing whitespace, to make our list cleaner
                    st.write(f"**Preparation:** {row['Preparation']}")          
                    st.write(f"**Garnish:** {row['Garnish']}")
                    st.write(f"**Glassware:** {row['Glassware']}")
                    st.write(f"**Bartender:** {row['Bartender']}")
                    st.write(f"**Location:** {row['Location']}")

#The following is how a user saves a cocktail to their favorites
                    like_key = f"like_{row['Cocktail Name']}_{index}"
                    if st.button("Like", key=like_key):
                        if row['Cocktail Name'] not in st.session_state.get('favorites', []):
                            st.session_state.favorites = st.session_state.get('favorites', []) + [row['Cocktail Name']] #sends our 'like' to the favorites tab
                    st.write("")  # Empty line for spacing
        else:
            st.write("No cocktails found with that name.") #if search query does not correspond to any cocktail from our API

#Tab 4: Cocktail Filter
#the code for this tab is essentially analogous to the one of the liquor cabinet, as they interact with one another
#Lines 111-115 showcase how our interface works and is built, provide maximal selection for the user given the data provided in our API
def display_cocktail_filter(df):
    st.title("Cocktail Filter")
    num_ingredients = st.selectbox("Maximum Number of Ingredients", options=['Any'] + list(range(1, 11)))
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

#This button allows the user to display the cocktails. However, once clicked, it cannot undisplay the results
#The only fix to this issue at the moment is to refresh the entire selection / whole app
    display_cocktails = st.button('Display Cocktails')
    if display_cocktails or st.session_state.get('display_cocktails', False):
        st.session_state['display_cocktails'] = True
        
        #The filter allows us to showcase the cocktails. We create a copy to avoid modifying the original data.
        filtered_df = df.copy()
         # Filter rows where the number of ingredients (comma-separated in the 'Ingredients' column)
        # matches the specified number of ingredients. The same is performed for glassware.
        if num_ingredients != 'Any':
            filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == int(num_ingredients))]
        if glassware != 'Any':
            filtered_df = filtered_df[filtered_df['Glassware'] == glassware]
        
        #here we create a regex filter to match alcohols selected in the cabinet.
        alcohol_regex = '|'.join([re.escape(alcohol) for alcohol in st.session_state.my_liquor_cabinet])
        filtered_df = filtered_df[filtered_df['Ingredients'].str.contains(alcohol_regex, case=False, na=False)]

        if not filtered_df.empty:
            st.subheader("Search Results:")
    
        # Use Streamlit's expander to group cocktail details neatly.
        #same as the code used to display the ingredients in the search tab.
            for index, row in filtered_df.iterrows():
                with st.expander(f"{row['Cocktail Name']}"):
                    #split ingrediants in string
                    ingredients_list = row['Ingredients'].split(',')
                    # Displaying ingredients in a bulleted list
                    st.write("**Ingredients:**")
                    for ingredient in ingredients_list:
                        st.write(f"- {ingredient.strip()}")  # .strip() removes any leading/trailing whitespace
                    st.write(f"**Preparation:** {row['Preparation']}")          
                    st.write(f"**Garnish:** {row['Garnish']}")
                    st.write(f"**Glassware:** {row['Glassware']}")
                    st.write(f"**Bartender:** {row['Bartender']}")
                    st.write(f"**Location:** {row['Location']}")

                    like_key = f"like_{row['Cocktail Name']}_{index}"
                    if st.button("Like", key=like_key):
                        if row['Cocktail Name'] not in st.session_state.get('favorites', []):
                            st.session_state.favorites = st.session_state.get('favorites', []) + [row['Cocktail Name']]
                    st.write("")  # Empty line for spacing
        else:
             st.warning("No cocktails match your filters.")

#Tab 5: My Favorites 
#Code written with the help of ChatGPT4. Prompt:
def display_favorites(df):
    st.title("My Favorites")
    if 'favorites' in st.session_state and st.session_state.favorites:
        st.subheader("Liked Cocktails:")
        for favorite in st.session_state.favorites:
            st.write(favorite)

        #This is the data used to create our pie chart.
        total_cocktails = len(df)
        liked_cocktails = len(st.session_state.favorites)
        labels = ['Liked Cocktails', 'Total Cocktails']
        sizes = [liked_cocktails, total_cocktails - liked_cocktails]
        explode = (0.1, 0)
        colors = ['#ffcc99', '#66b3ff'] #color codes selected by accessing streamlit cheatsheet.

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)

        #Creation of our second pie chart --> Which Alcohols our user is made of. 
        #Code written with the help of ChatGPT4. Prompt:
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

        #Used to reset our likes. Must be clicked twice to work and do a full reset of the selection on the app.
        if st.button('Reset Likes'):
            st.session_state.favorites = []
            st.success('Your liked cocktails have been reset!')
    else:
        st.write("You haven't liked any cocktails yet.")

#Definition of Main: linking the different pirces of the code together
def main():
    if 'my_liquor_cabinet' not in st.session_state:
        st.session_state['my_liquor_cabinet'] = []
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

#Loading our API
    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
#Creating a sidebar with tabs
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "Manage Liquor Cabinet", "Cocktail Search", "Cocktail Filter", "My Favorites"])

#Tab functionality
    if selected_tab == "Hello Mixologist": #displaying tab title
        display_welcome_message() #running the tab
    elif selected_tab == "Manage Liquor Cabinet":
        manage_liquor_cabinet()
    elif selected_tab == "Cocktail Search":
        display_cocktail_search(df)
    elif selected_tab == "Cocktail Filter":
        display_cocktail_filter(df)
    elif selected_tab == "My Favorites":
        display_favorites(df)

#Running main
if __name__ == "__main__":
    main()
