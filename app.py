import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Function to load data from a URL into a DataFrame
def load_data(url):
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# Display the welcome message and story
def display_welcome_message():
    st.title("Hello Mixologist")
    st.write("Welcome to the Cocktail Finder!")
    st.write("This website helps you discover new cocktails based on the ingredients you have at home.")
    st.write("Let me tell you a short story:")
    st.write("Once upon a time, nestled in the cozy dorms of the HSG campus, there lived a spirited young student named Emily. Now, Emily wasn't just any ordinary student – she harbored a burning passion for mixology, despite her limited collection of alcohol at home. With only a few bottles of assorted spirits tucked away in her pantry, she dreamed of concocting dazzling cocktails that would dazzle her friends and classmates.")
    st.write("But Emily was faced with a predicament: how could she create masterful cocktails with such a meager selection of ingredients? Undeterred, she embarked on a whimsical journey to unravel the mysteries of mixology, armed with nothing but her enthusiasm and a handful of liquor bottles.")
    st.write("Her first attempt at mixology was nothing short of comical. With a bottle of vodka, a splash of cranberry juice, and a squeeze of lime, she attempted to craft her own version of a classic Cosmopolitan. However, her proportions were far from perfect, resulting in a drink that was more reminiscent of cough syrup than a sophisticated cocktail. Undeterred by her initial failure, Emily soldiered on, determined to refine her skills and create drinks worthy of admiration.")
    st.write("As her journey progressed, Emily's passion for mixology only grew stronger. She spent countless hours scouring the internet for cocktail recipes, experimenting with different combinations of ingredients, and honing her bartending techniques. From simple highballs to elaborate tiki concoctions, Emily fearlessly explored the vast and colorful world of mixology, one drink at a time")
    st.write("But Emily's adventures weren't just confined to her dorm room. She ventured beyond the confines of campus, seeking inspiration from local bars and cocktail lounges. With wide-eyed wonder, she observed seasoned bartenders expertly crafting cocktails, their graceful movements and meticulous attention to detail captivating her imagination.")
    st.write("With each sip of a new cocktail, Emily discovered a world of flavors and sensations she never knew existed. From the tangy bite of a margarita to the smoky richness of an old-fashioned, each drink told a story of its own, inviting her to embark on a journey of exploration and discovery.")
    st.write("And so, armed with newfound knowledge and a boundless sense of curiosity, Emily's journey into the enchanting realm of mixology continued, fueled by her unwavering passion and a thirst for adventure.")
    st.write("As the sun set on another day at HSG, Emily raised her glass to the endless possibilities that lay ahead, knowing that her quest to master the art of mixology was only just beginning. And with a mischievous twinkle in her eye, she whispered to herself, 'Here's to the next cocktail adventure!'")
    st.write("And now, it's your turn to explore and create your own cocktail adventures!")
    st.write("Stay tuned for more updates!")

def display_liquor_cabinet():
    st.title("My Liquor Cabinet")
    st.write("Welcome to your Liquor Cabinet!")
    st.write("Here, you can list the assortment of alcohol you have.")

    # List of alcohol bases
    alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 
                     'Vermouth', 'Liqueurs', 'Absinthe', 'Aquavit', 'Sake', 
                     'Sherry', 'Port', 'Cachaça', 'Pisco', 'Mezcal', 
                     'Aguardiente', 'Soju', 'Baijiu', 'Grappa']

    # Initialize selected_alcohols in session state if not already present
    if 'selected_alcohols' not in st.session_state:
        st.session_state['selected_alcohols'] = []

    # Create a row of 5 columns for alcohol checkboxes
    num_columns = 5
    columns = st.columns(num_columns)
    updated_selected_alcohols = st.session_state['selected_alcohols'].copy()
    
    for i, alcohol in enumerate(alcohol_bases):
        col_index = i % num_columns
        if columns[col_index].checkbox(alcohol, key=alcohol, value=alcohol in st.session_state['selected_alcohols']):
            if alcohol not in updated_selected_alcohols:
                updated_selected_alcohols.append(alcohol)
        elif alcohol in updated_selected_alcohols:
            updated_selected_alcohols.remove(alcohol)
    
    # Update session state after iteration
    st.session_state['selected_alcohols'] = updated_selected_alcohols

    # Display the selected alcohol bases
    st.write("which glasses do u have at home:")
    for selected_alcohol in st.session_state['selected_alcohols']:
        st.write(f"- {selected_alcohol}")

    # ***Define glass_types here, before using it for rows calculation***
    glass_types = [
        'Punch Bowl', 'Collins', 'Coupe', 'Tin Cup', 'Martini', 'Rocks Glass', 
        'Nick & Nora', 'Flip Glass', 'Tiki glass', 'Demitasse Glass', 
        'Footed Rocks Glass', 'Etched Rocks Glass', 'Canadian Glencairn Glass', 
        'Vintage Glass', 'Double Old Fashioned Glass', 'Crystal Rocks', 'Shot Glass', 
        'V-Shaped Rocks Glass', 'Hurricane Glass', 'Tiki Cat Glass', 
        'Bamboo Highball Glass', 'Tumbler', 'Egg Coupe', 'Port Glass', 
        'Smoked Glass', 'Highball Glass', 'Stemmed Cordial Glass', 'Cocktail Glass', 
        'Wine Glass', 'Old Fashioned Glass', 'Mug', 'Large Balloon Glass', 'Bucket',
        'Pilsner Glass', 'Goblet', 'Royal Coupette', 'Copita Glass', 'Shorty Beer',
        'Double Rocks Glass', 'Glass Mug', 'Stemless Wine Glass', 'Lowball Glass', 
        'Irish Coffee Mug', 'Julep Cup', 'Fizz Glass', 'Lager', 'Small tumbler', 'Snifter',
        'Champagne Flute', 'Copper Mug', 'Coffee Mug', 'Large Antique Vintage Shaker', 'Beer Glass'
    ]

    if 'selected_glasses' not in st.session_state:
        st.session_state['selected_glasses'] = []

    num_columns = 4
    rows = (len(glass_types) + num_columns - 1) // num_columns
    for i in range(rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            idx = i * num_columns + j
            if idx < len(glass_types):
                glass = glass_types[idx]
                if cols[j].checkbox(glass, key=glass, value=glass in st.session_state['selected_glasses']):
                    if glass not in st.session_state['selected_glasses']:
                        st.session_state['selected_glasses'].append(glass)
                elif glass in st.session_state['selected_glasses']:
                    st.session_state['selected_glasses'].remove(glass)

# Explore cocktails based on selections
def cocktail_explorer(df):
    st.title("Cocktail Explorer")
    st.write("Welcome to the Cocktail Explorer!")
    st.write("Here, you can explore various cocktails based on your preferences.")
    st.write("Use the search function to filter cocktails by ingredients, glassware, and more.")
    st.write("You can also rate cocktails and save your favorites for future reference.")

    # Cocktail Finder Code Starts Here
    # User input for maximum number of ingredients
    max_ingredients = st.number_input('Maximum Ingredients', min_value=1, max_value=20, value=5, help="Select the maximum number of ingredients you want in the cocktails.")

    # List of all possible alcohol bases
    alcohol_base_options = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaça', 'Pisco', 'Mezcal', 'Aguardiente', 'Soju', 'Baijiu', 'Grappa']

    # Filter out alcohol bases that result in no cocktails
    valid_alcohol_bases = []
    for alcohol in alcohol_base_options:
        filtered_df = df[df['Ingredients'].str.lower().str.contains(alcohol.lower())]
        if not filtered_df.empty:
            valid_alcohol_bases.append(alcohol)

    # Dropdown for selecting alcohol base
    alcohol_base = st.selectbox('Select Alcohol Base', valid_alcohol_bases).lower()

    # Get unique glassware options
    glassware_options = df['Glassware'].unique()

    # Prepend 'Any' option to glassware options
    glassware_options = ['Any'] + list(glassware_options)

    # Select box for glassware
    glassware = st.selectbox('Select Glassware', glassware_options)

    # Filtered DataFrame initially includes all cocktails
    filtered_df = df.copy()

    # Filter for cocktails with up to the given maximum number of ingredients
    filtered_df['num_ingredients'] = filtered_df['Ingredients'].apply(lambda x: len(x.split(',')))
    filtered_df = filtered_df[filtered_df['num_ingredients'] <= max_ingredients]

     # If 'Any' glassware is selected, do not apply glassware filter
    if glassware != 'Any':
        filtered_df = filtered_df[filtered_df['Glassware'] == glassware]

    # Display results
    if not filtered_df.empty:
        st.write(filtered_df.drop(columns=['num_ingredients']))  # Drop the temporary 'num_ingredients' column before display
    else:
        st.write('No cocktails found.')

# Display favorites
def display_favorites(df):
    st.title("Favourites")
    st.write("Welcome to your Favourites!")
    st.write("Here, you can view and manage your favorite cocktails.")
    st.write("Explore the cocktails you've rated highly and revisit them anytime.")
    # TODO: Add code to display and manage favorite cocktails


def main():
    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "My Liquor Cabinet", "Cocktail Explorer", "Favourites"])
    
    if selected_tab == "Hello Mixologist":
        display_welcome_message()
    elif selected_tab == "My Liquor Cabinet":
        display_liquor_cabinet()
    elif selected_tab == "Cocktail Explorer":
        cocktail_explorer(df)
    elif selected_tab == "Favourites":
        display_favorites(df)

if __name__ == "__main__":
    main()
