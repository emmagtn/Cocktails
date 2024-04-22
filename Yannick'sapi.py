import streamlit as st
import pandas as pd
import re
import requests
from io import StringIO

# Function to load data from a URL into a DataFrame
def load_data(url):
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# Tab 1 the intro page
def display_welcome_message():
    st.title("Hello Mixologist")
    # Placeholder for additional story or welcome message

#  Tab 2 Search by title
def display_cocktail_search(df):
    st.title("Cocktail Search")
    search_query = st.text_input("Search for a cocktail")
    if search_query:
        # Perform a case-insensitive search within the 'Cocktail Name' column
        results = df[df['Cocktail Name'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            for index, row in results.iterrows():
                if st.button(f"View Details for {row['Cocktail Name']}"):
                    display_cocktail_details(row['Cocktail Name'], df)
        else:
            st.write("No cocktails found with that name.")

#### sub part 2 the structure of the search tab 2

# Subtitles: best served with (garnish, glassware) / more info (bartneder, location)
# Add sentences where the data is put in directly
# show: title, ingredients, garnish, preparation, glasssware, bartender, location

def display_cocktail_details(cocktail_name, df):
    if filtered_df.empty:
        st.write('No cocktails found.')
    else:
    cocktail_details = df[df['Cocktail Name'].str.lower() == cocktail_name.lower()].iloc[0]
    st.header(cocktail_details['Cocktail Name'])
    st.subheader('Ingredients')
    st.write(cocktail_details['Ingredients'])
    st.subheader('Preparation')
    st.write(cocktail_details['Preparation'])

    # Displaying additional information only if available

    if 'Garnish' in cocktail_details and 'Glassware' in cocktail_details:
        st.subheader('Best servded with')
        st.write(cocktail_details['Garnish'])
        st.write(cocktail_details['Glassware'])

    if 'Bartender' in cocktail_details and 'Location' in cocktail_details:
    st.subheader('Additional Info')
        st.write(cocktail_details['Bartender'])
        st.write(cocktail_details['Location'])
    
# Tab 3 cocktail filter
def cocktail_filter(df):
    st.title("Cocktail Filter")
    st.title("Cocktail Explorer")
    st.write("Welcome to the Cocktail Explorer!")
    st.write("Here, you can explore various cocktails based on your preferences.")
    st.write("Use the search function to filter cocktails by ingredients, glassware, and more.")

### Cocktail Finder Code Starts Here

# Definitions of filtered variables
    
    # Alcohol
    # List of all possible alcohol bases, defined by us, not from the df
        alcohol_bases = ['Any', ' Vodka ', ' Rum ', ' Gin ', ' Tequila ', ' Whiskey ', ' Brandy ', ' Vermouth ', ' Liqueurs ', 'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']
    
    # Glassware
    # Get all possible glassware options
        glassware_options = df['Glassware'].unique()

    # Add the option 'Any' to glassware options
        glassware_options = ['Any'] + list(glassware_options)

    # Vibe
    # the cocktail ingredients matching a words on one of these lists, would categorize the cocktail's vibe as that of the list

        vibes = {
                'fruity': [
                            'lemon', 'lime', 'orange', 'berry', 'pineapple', 'mango', 'peach', 'apple',
                            'grape', 'banana', 'passion fruit', 'fruit liqueur', 'cherry', 'pomegranate',
                            'apricot', 'melon', 'kiwi', 'pear', 'fig', 'fruit juice', 'fruit', 'juice'
                            ],
                'tropical': [
                            'coconut', 'pineapple juice', 'mango juice', 'passion fruit juice', 'papaya',
                            'guava', 'lychee', 'rum', 'tiki bitters', 'banana liqueur', 'Malibu', 'cachaça',
                            'tamarind', 'dragon fruit', 'star fruit', 'kumquat', 'coconut milk', 'coconut cream',
                            'falernum', 'orgeat'
                            ],
                'sweet': [
                            'syrup', 'sugar', 'honey', 'liqueur', 'grenadine', 'agave nectar', 'sweet vermouth',
                            'cointreau', 'maraschino', 'soda', 'cola', 'vanilla'
                            ],
                'spicy': [
                            'pepper', 'cayenne', 'jalapeno', 'jalapeño', 'ginger', 'cinnamon', 'horseradish',
                            'spicy', 'spice', 'hot sauce', 'tabasco', 'chili', 'wasabi', 'sriracha'
                             ],
                'Any'
                }

    # funtion to later find the vibe in ingredients of df
    def ingredient_in_phrase(phrase, ingredients_list):
        phrase = phrase.lower()  # Normalize to lowercase
        patterns = [re.escape(ingredient) for ingredient in ingredients_list]  # Create regex patterns
        return any(re.search(pattern, phrase) for pattern in patterns)

# User input
    
    #Nr of ingredients
    # User input for maximum number of ingredients
    max_ingredients = st.number_input('Maximum Ingredients', min_value=1, max_value=13, value=5, help="Select the maximum number of ingredients you want in the cocktails.")

    # Dropdown for selecting alcohol base
    alcohol_base = st.selectbox('Select Alcohol Base', alcohol_bases).lower()

    # Select box for glassware
    glassware = st.selectbox('Select Glassware', glassware_options)
    
    # Select box for vibes
    vibe = st.selectbox('Select the Vibe of your drink', vibes)

# Final Filtered dataframe

    # Filter for cocktails with up to the given maximum number of ingredients
    filtered_df = df[df['Ingredients'].apply(lambda x: len(x.split(','))) <= max_ingredients]

    # If 'Any' alcohol is selected, do not apply alcohol filter
    if alcohol_base != 'Any':
        for alcohol in alcohol_bases:
        filtered_df = df[df['Ingredients'].str.lower().str.contains(alcohol.lower())]

     # If 'Any' glassware is selected, do not apply glassware filter
    if glassware != 'Any':
        filtered_df = filtered_df[filtered_df['Glassware'] == glassware]

    # If 'Any' vibe is selected, do not apply vibe filter
        if alcohol_base != 'Any':
            for vibe in vibes:
            filtered_df = df[df['Ingredients'].apply(lambda x: ingredient_in_phrase(x, vibe))]


# the summary of all the previous tabs and compilement function
def main():
    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "Cocktail Search", "Cocktail Filter"])
    
    if selected_tab == "Hello Mixologist":
        display_welcome_message()
    elif selected_tab == "Cocktail Search":
        display_cocktail_search(df)
    elif selected_tab == "Cocktail Filter":
        cocktail_filter(df)
        
# the excution of programm
if _name_ == "main":
    main()