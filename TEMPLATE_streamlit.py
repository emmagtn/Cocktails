# Hi guys, this is meant to be a general template for streamlit to facilitate our workflow.
# it is meant to be a source for some basic formatting we can all use (like buttons, etc.)
# make sure to have streamlit and pandas installed down in terminal (pip install streamlit & pip install pandas)
# how to see it on streamlit: insert down in terminal: streamlit run TEMPLATE_streamlit.py 


# First for any file we import streamlit
import streamlit as st


# Write a title and some text to the app's page.
st.title('Streamlit Cheat Sheet for Our Project')
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
