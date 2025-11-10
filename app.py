import streamlit as st

# Menu de navigation : Barre latérale

page_accueil = st.Page("./pages/1_🏡_Accueil.py", 
                       title="Accueil", 
                       icon="🏡",
                       default=True)

page_dashboard = st.Page("./pages/6_📝_Dashboard.py", 
                         title="Dashboard", 
                         icon="📝")

page_netflix_cleaning = st.Page("./pages/2_🔎_Partie 1 - Analyse Exploratoire.py", 
                                title="Analyse et Cleaning du dataset Netflix", 
                                icon="🔎")

page_netflix_analysis = st.Page("./pages/3_📈_Partie 1 - Les graphiques Seaborn.py", 
                                title="Visualisation Seaborn du dataset Netflix", 
                                icon="📈")

page_world_happiness_cleaning = st.Page("./pages/4_♻️_Partie 2 - Harmonisation des datasets.py", 
                                        title="Harmonisation des datasets : World Happiness Report (2015-2019)", 
                                        icon="♻️")

page_world_happiness_analysis = st.Page("./pages/5_📊_Partie 2 - Visualisation avec Plotly.py", 
                                        title="Visualisation Plotly du dataset World Happiness Report harmonisé", 
                                        icon="📊")

pg = st.navigation({
    "Accueil": [page_accueil],
    "Dashboard" : [page_dashboard],
    "Partie 1 : Netflix (Seaborn)": [page_netflix_cleaning, page_netflix_analysis],
    "Partie 2 : World Happiness (Plotly)": [page_world_happiness_cleaning, page_world_happiness_analysis]
})

pg.run()
