# Hi guys, this is meant to be a general template for streamlit to facilitate our workflow.
# it is meant to be a source for some basic formatting we can all use (like buttons, etc.)
# make sure to have streamlit and pandas installed down in terminal (pip install streamlit & pip install pandas)
# how to see it on streamlit: insert down in terminal: streamlit run TEMPLATE_streamlit.py 


# First for any file we import streamlit
import streamlit as st

# Following now there will be some elements that are specifically useful for our app. 
# DOWN BELOW we have more general resources that are more general functions that we might want to use.


# Title and subheader for the welcome page
st.title('Cocktails on the Go!')
st.subheader('Fancy an inspiration for Sprittwoch? Discover new cocktails you can mix from your own liquor cabinet.')

# Table of Contents
st.markdown("""
## Table of Contents
1. [My Liquor Cabinet](#my-liquor-cabinet)
2. [Cocktail Suggestions](#cocktail-suggestions)
3. [Wishlist](#wishlist)
4. [My Favorites](#my-favorites)
""")

# How to: Navigation to different sections
# This can be achieved by Streamlit's anchors or buttons that will scroll to different parts of the page.
# maybe we still need to figure that one out...

# NEXT: My liquor cabinet page

st.header('My Liquor Cabinet')  # Chapter title
# Creating a list of liquor bases -> maybe NOT the way we need to go, since we need to use the API
liquor_bases = ['Gin', 'Whiskey', 'Vodka', 'Rum', 'Tequila']

# Allowing users to select their available liquors
selected_bases = st.multiselect('Select the liquor you have:', liquor_bases)

# Button to save selected liquors
if st.button('Save My Cabinet'):
    # Save the data to the backend/session state
    st.session_state['selected_bases'] = selected_bases
    st.success('Your liquor cabinet has been updated.')

# Button to find drinks from the cabinet
if st.button('Find Drinks'):
    # Perform search query using selected_bases
    # Assume we have a function `find_drinks` that takes the selected bases and returns a list of drink recipes
    drink_suggestions = find_drinks(selected_bases)
    # Save drink suggestions to session state
    st.session_state['drink_suggestions'] = drink_suggestions


# NEXT: Result of our liquor selection

st.header('Cocktail Suggestions')

# Display drink suggestions from session state if available
if 'drink_suggestions' in st.session_state:
    for drink in st.session_state['drink_suggestions'][:5]:  # Only show 5 suggestions
        st.write(drink)  # Display each drink suggestion
        # Include a button to favorite each drink
        if st.button(f'Favorite {drink}', key=drink):
            # Logic to add the drink to favorites
            pass

    # Button to refresh drink suggestions
    if st.button('Refresh Suggestions'):
        # Logic to refresh the drink suggestions
        pass



# NEXT: Wishlist page

st.header('Wishlist')

# Similar logic to 'My Liquor Cabinet' page
# ...

# You can reuse most of the code from 'My Liquor Cabinet' and adjust the variables/function calls as needed.


# NEXT: our favorites page

st.header('My Favorite Recipes')
# Assuming you have a list of favorite recipes stored in 'favorites'
favorites = ['Margarita', 'Martini']  # Placeholder for favorites list

# Displaying favorites in alphabetical order
for recipe in sorted(favorites):
    st.write(recipe)
    if st.button(f'Delete {recipe} from Favorites'):
        # Add code to remove the recipe from favorites
        pass

if st.button('Erase all favorites'):
    # Add code to erase all favorites
    pass

# Displaying a pie chart of common alcohol bases in the favorite recipes
import matplotlib.pyplot as plt

# Sample data for the pie chart
alcohol_counts = {'Gin': 4, 'Whiskey': 2, 'Vodka': 3}  # This would come from analyzing the 'favorites' list
fig, ax = plt.subplots()
ax.pie(alcohol_counts.values(), labels=alcohol_counts.keys(), autopct='%1.1f%%')
st.pyplot(fig)

if st.button('Reset chart'):
    # Add code to reset the pie chart based on updated favorites
    pass

# The above code includes buttons for interaction and a pie chart for data visualization.



# BELOW: General resources

# Write a title and some text to the app's page.
st.title('Below: General Streamlit Cheat Sheet for Our Project')
st.write("This is generic text. Here's our first attempt at using data to create a table:")

# Writing text and data
# Use `st.write` to print data or messages on the app
st.write("Hello, you drunken sailor!")

# How to display data
# How to create a simple dataframe (here we need the pandas, make sure to have pip install pandas in the terminal)
import pandas as pd
data = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

# Use `st.dataframe` to display the dataframe
st.dataframe(data)

# Display charts
# Use `st.line_chart` to create a line chart of a dataframe
st.line_chart(data)

# Plotting maps (if you have lat/long data)
# Use `st.map` to display a map with points on it
map_data = pd.DataFrame({
    'lat': [34.0522, 37.7749],
    'lon': [-118.2437, -122.4194]
})

st.map(map_data)

# Use checkboxes for options
if st.checkbox('Show dataframe'):
    data = pd.DataFrame({
      'first column': [1, 2, 3, 4],
      'second column': [10, 20, 30, 40]
    })
    st.write(data)

# Use a selectbox for options
option = st.selectbox(
    'Which number do you like best?',
     data['first column'])

'You selected:', option

# Add sliders and buttons
age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

if st.button('Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

# Layouts & Containers - Use columns to layout widgets side by side
col1, col2 = st.columns(2)
with col1:
    st.header('A cat')
    st.image('https://static.streamlit.io/examples/cat.jpg') # this inserts a picture

with col2:
    st.header('A dog')
    st.image('https://static.streamlit.io/examples/dog.jpg')

# Caching - speed up your app by caching data
@st.cache
def expensive_computation():
    # ... some expensive computation ...
    return result

# Session state - persist state across reruns -> this is to add counts up, it's aggregated in the increment function
if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)

# Sidebar - add widgets to a sidebar -> maybe these can be used as tabs
st.sidebar.write("Here are some cool widgets:")

# Display interactive widgets in the sidebar
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Execute the file with streamlit run [filename]
# in our case: streamlit run TEMPLATE_streamlit.py

