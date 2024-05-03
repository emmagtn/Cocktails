# Zugriff auf Datenbanken durch deren Import
import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import re


# Definieren von alcohol_bases global als Liste. Unsere API wurde manuell analysiert, um festzustellen, welche Alkoholbasen erwähnt wurden.
alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                 'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal']

# Aktivieren der Funktionen aus unseren Importen
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

# Tab 1: Willkommen-Seite, Bilder und Text.
def display_welcome_message():
    st.title('Welcome to the Cocktail Connoisseur App')

    # Bild wird angezeigt einer Cocktail-Bar welches von folgender URL stammt. Untenstehend wird der Text der Startseite angezeigt.
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
    ''') # Oben: Lange und persönliche Einführung in unser Projekt. Plus Beschreibung, wie man auf unserer Website navigiert.

# Tab 2: My Liquor Cabinet. 
# Der folgende Code verweist zurück auf unsere Alkohol-Liste in Zeile 11-12 'alcohol bases'
def manage_liquor_cabinet():
    st.title('Manage Your Liquor Cabinet')
    cols = st.columns(4)
    per_column = len(alcohol_bases) // 4 #Zeile 64 und 65 sind für ästhetische Zwecke, unsere Buttons werden im 4x4 Format angeordnet.
    remainder = len(alcohol_bases) % 4
    for i, col in enumerate(cols):
        with col:
            start_index = i * per_column
            end_index = start_index + per_column + (1 if i < remainder else 0)
            for alcohol in alcohol_bases[start_index:end_index]:
                st.checkbox(alcohol, key=alcohol, value=alcohol in st.session_state.my_liquor_cabinet)
    if st.button('Save Liquor Cabinet'): # Diese Schaltfläche speichert die Auswahl der Alkohole im Schrank. Es ermöglicht uns, diese Informationen später für andere Seiten zu finden.
        st.session_state.my_liquor_cabinet = [alcohol for alcohol in alcohol_bases if st.session_state.get(alcohol, False)]
        st.success('Your liquor cabinet has been updated!')

# Tab 3: Cocktail Suche
# Ermöglicht dem Benutzer die Suche nach einem Cocktail durch Zugriff auf unsere API über ein Suchabfragetab.
def display_cocktail_search(df):
    st.title("Cocktail Search")
    search_query = st.text_input("Search for a cocktail")
    if search_query:
        results = df[df['Cocktail Name'].str.contains(search_query, case=False, na=False)]
        if not results.empty:
            st.subheader("Search Results:")
            for index, row in results.iterrows(): # Diese Funktion gibt unsere Daten aus
                with st.expander(f"{row['Cocktail Name']}"): #Der Expander ermöglicht es uns, die Auswahl bei Klick zu erweitern (beim Klick auf den Cocktailtitel erhält man das gesamte Rezept).
                    # Aufteilung der Zutaten in Strings.
                    ingredients_list = row['Ingredients'].split(',')
                    # Anzeige der Zutaten in Bulletpoint-Format.
                    st.write("**Ingredients:**")
                    for ingredient in ingredients_list:
                        st.write(f"- {ingredient.strip()}")  # .strip() entfernt überschüssiger Whitespace, für ein saubereres Erscheinungsbild.
                    st.write(f"**Preparation:** {row['Preparation']}")          
                    st.write(f"**Garnish:** {row['Garnish']}")
                    st.write(f"**Glassware:** {row['Glassware']}")
                    st.write(f"**Bartender:** {row['Bartender']}")
                    st.write(f"**Location:** {row['Location']}")

# Der folgende Code erlaubt dem Nutzer einen Cocktail seiner / ihrer Wahl in die Favoriten zu speichern.
                    like_key = f"like_{row['Cocktail Name']}_{index}"
                    if st.button("Like", key=like_key):
                        if row['Cocktail Name'] not in st.session_state.get('favorites', []):
                            st.session_state.favorites = st.session_state.get('favorites', []) + [row['Cocktail Name']] # speichert unser Like im Favoriten-Tab
                    st.write("")  # Formatierung: Leere Zeile.
        else:
            st.write("No cocktails found with that name.") # Falls unsere Suchanfrage nicht zu einem Cocktail in unserem API passt.

# Tab 4: Cocktail Filter
# Der Code für diesen Tab ist im Wesentlichen analog zu dem des 'Alcohol Cabinets', da sie miteinander interagieren.
# Die Zeilen 111-115 zeigen, wie unsere Benutzeroberfläche funktioniert und aufgebaut ist. Personalisierung des Inputs durch den Benutzer - Auswahlmöglichkeitetn gegeben durch die Daten in unserer API.
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

# Diese Schaltfläche ermöglicht es dem Benutzer, die Cocktails anzuzeigen. Es kann jedoch nicht deaktiviert werden, wenn es einmal geklickt wurde.
# Der einzige Fix für dieses Problem besteht derzeit darin, die gesamte Auswahl/die gesamte App zu aktualisieren.
    display_cocktails = st.button('Display Cocktails')
    if display_cocktails or st.session_state.get('display_cocktails', False):
        st.session_state['display_cocktails'] = True
        
        # Der Filter ermöglicht es uns, die Cocktails anzuzeigen. Wir erstellen eine Kopie, um die Originaldaten nicht zu ändern.
        filtered_df = df.copy()
        # Filtern der Zeilen, bei denen die Anzahl der Zutaten (durch Kommas getrennt in der Spalte 'Ingredients') 
        # der angegebenen Zutatenanzahl entspricht. Gleiches gilt für Gläser.
        if num_ingredients != 'Any':
            filtered_df = filtered_df[filtered_df['Ingredients'].apply(lambda x: len(x.split(',')) == int(num_ingredients))]
        if glassware != 'Any':
            filtered_df = filtered_df[filtered_df['Glassware'] == glassware]
        
        # Hier erstellen wir einen Regex-Filter, um die im Schrank ausgewählten Alkohole abzugleichen.
        alcohol_regex = '|'.join([re.escape(alcohol) for alcohol in st.session_state.my_liquor_cabinet])
        filtered_df = filtered_df[filtered_df['Ingredients'].str.contains(alcohol_regex, case=False, na=False)]

        if not filtered_df.empty:
            st.subheader("Search Results:")
    
        # Hier verwenden wir den Expander von Streamlit, um Cocktaildetails übersichtlich zu gruppieren.
        # Gleich wie der Code, der verwendet wird, um die Zutaten im Suchregister anzuzeigen.
            for index, row in filtered_df.iterrows():
                with st.expander(f"{row['Cocktail Name']}"):
                    # die Zutanten werden in Strings aufgetrennt
                    ingredients_list = row['Ingredients'].split(',')
                    # Die Zutaten werden in einer Bulletpoint-Liste angezeigt
                    st.write("**Ingredients:**")
                    for ingredient in ingredients_list:
                        st.write(f"- {ingredient.strip()}")  # .strip() entfernt überschüssiger Whitespace
                    st.write(f"**Preparation:** {row['Preparation']}")          
                    st.write(f"**Garnish:** {row['Garnish']}")
                    st.write(f"**Glassware:** {row['Glassware']}")
                    st.write(f"**Bartender:** {row['Bartender']}")
                    st.write(f"**Location:** {row['Location']}")

                    like_key = f"like_{row['Cocktail Name']}_{index}"
                    if st.button("Like", key=like_key):
                        if row['Cocktail Name'] not in st.session_state.get('favorites', []):
                            st.session_state.favorites = st.session_state.get('favorites', []) + [row['Cocktail Name']]
                    st.write("")  # Eine leere Zeile für eine saubere Struktur
        else:
             st.warning("No cocktails match your filters.")

# Tab 5: My Favorites 
# Folgender Code wurde mithilfe ChatGPT geschrieben: Die Prompt lassen wir auf Englisch für eine akkurate und transparente Zitierung. 
    #Prompt:
        #Adapt code that the like checkmark box is below every cocktail title when search and if the like check mark is presse it saves the cocktail 
        #to the favorites list which would then print the favorites list on the last tab, this should be adapted  for both the tabs search cocktail 
        #and filter cocktail: [input entire code]
def display_favorites(df):
    st.title("My Favorites")
    if 'favorites' in st.session_state and st.session_state.favorites:
        st.subheader("Liked Cocktails:")
        for favorite in st.session_state.favorites:
            st.write(favorite)

        # Folgend sind die benötigten Daten für unsere Visualisierung als Kreisdiagramm
        total_cocktails = len(df)
        liked_cocktails = len(st.session_state.favorites)
        labels = ['Liked Cocktails', 'Total Cocktails']
        sizes = [liked_cocktails, total_cocktails - liked_cocktails]
        explode = (0.1, 0)
        colors = ['#ffcc99', '#66b3ff'] # Farben-Codes erhalten durch Nutzen eines Streamlit-Cheat Sheets

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')
        st.pyplot(fig1)

        # Erstellung unseres zweiten Kreisdiagramms --> Woraus 'besteht' unser Benutzer?
        # Code geschrieben mit Hilfe von ChatGPT4: Die Prompt lassen wir auf Englisch für eine akkurate und transparente Zitierung.
            #Prompt: 
                #edit the code so that when a cocktail title is like then their will be a search for each selected titles row of the dataset for all the alchol basis represented in this alchol_ bases definition: 
                #alcohol_bases = ['Vodka', 'Rum', 'Gin', 'Tequila', 'Whiskey', 'Brandy', 'Vermouth', 'Liqueurs', 
                #'Absinthe', 'Aquavit', 'Sake', 'Sherry', 'Port', 'Cachaca', 'Pisco', 'Mezcal'] then count the amount each alchol base comes up and display a graph chart , keep the rest of the code as is and show the editing in snippets , edit this following code :
                #display_favorites(df): [(...) c.f. Code Lines 179-184]
      
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
        st.markdown("### You are made of:")  # Nutzen des Markdowns für Formatierung des Titels.
        st.pyplot(fig2)

        # Wird verwendet, um unsere Likes zurückzusetzen. Muss zweimal angeklickt werden, um die Auswahl der App vollständig zurückzusetzen.
        if st.button('Reset Likes'):
            st.session_state.favorites = []
            st.success('Your liked cocktails have been reset!')
    else:
        st.write("You haven't liked any cocktails yet.")

# Definition des Mains: Verbindung der verschiedenen Code-Stücke miteinander
def main():
    if 'my_liquor_cabinet' not in st.session_state:
        st.session_state['my_liquor_cabinet'] = []
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

# Laden unseres APIs
    df = load_data('https://github.com/OzanGenc/CocktailAnalysis/raw/main/cocktails.csv')
# Erschaffen von einer Sidebar mit Tabs des Apps.
    selected_tab = st.sidebar.radio("Select Tab", ["Hello Mixologist", "Manage Liquor Cabinet", "Cocktail Search", "Cocktail Filter", "My Favorites"])

# Tab Funktionalität:
    if selected_tab == "Hello Mixologist": # Darstellung des Tab-Titels
        display_welcome_message() # Tab-Klick ausführen
    elif selected_tab == "Manage Liquor Cabinet":
        manage_liquor_cabinet()
    elif selected_tab == "Cocktail Search":
        display_cocktail_search(df)
    elif selected_tab == "Cocktail Filter":
        display_cocktail_filter(df)
    elif selected_tab == "My Favorites":
        display_favorites(df)

# Ausführung des Mains
if __name__ == "__main__":
    main()
