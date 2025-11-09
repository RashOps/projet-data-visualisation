# Imporation des dépendances
import pandas as pd
import streamlit as st

# Configuration de la page principale
st.set_page_config(
    page_title="Accueil",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state = "expanded"
)

# Structuration de la page d'accueil
st.title("Projet Data visualisation")
st.image(image="./images/projet-data.jpg", width=700)

# Description du projet
st.header("Description du projet")
st.markdown(
"""
**2 Étapes**, **2 Jeux de Données**

Analyser deux jeux de données distincts à l'aide des librairies **Seaborn** et **Plotly**, et 
produire des visualisations claires, esthétiques et informatives pour mettre en avant des 
faits marquants.
""")


st.write("")
st.write("")
st.divider()
# Section Seaborn
# Titre de la section
st.subheader("Partie 1 : Analyse Exploratoire avec Seaborn")
st.image(image="./images/partie1-image.jpg", width=700)

# Description de la section
st.markdown(
"""
    **Objectif**

    Utiliser Seaborn pour explorer un dataset simple et mettre en évidence les relations entre 
    plusieurs variables à travers des visualisations statistiques élégantes.

    **Dataset : Netflix Movies and TV Shows**

    Un ensemble de données complet sur les films et séries disponibles sur Netflix, incluant 
    informations sur les pays, années de sortie, genres et durées.

    [Telecharger le dataset utilisé ici](https://www.kaggle.com/datasets/shivamb/netflix-shows)
""")

# Création des colones
col1, col2 = st.columns(2)

# Colone 1
with col1 :
    st.link_button("Section 1 : Analyse Exploratoire", url="/Partie_1_-_Analyse_Exploratoire")

# Colone 2
with col2 :
    st.link_button("Section 2 : Les graphiques avec Seaborn", url="/Partie_1_-_Les_graphiques_Seaborn")



st.write("")
st.write("")
st.divider()
# Section Plotly
# Titre de la section
st.subheader("Partie 2 : Visualisation Interactive avec Plotly")
st.image(image="./images/partie2-image.png", width=700)

# Description de la section
st.markdown(
"""
    **Objectif**

    Créer des visualisations dynamiques et interactives pour explorer un 
    second dataset sous différents angles avec des graphiques manipulables.

    **Dataset : World Happiness Report**

    Données sur le bonheur mondial incluant PIB, santé, liberté, générosité et 
    autres indicateurs de bien-être pour différents pays.

    [Telecharger le dataset utilisé ici](https://www.kaggle.com/datasets/unsdsn/world-happiness)
""")

# Création des colones
col3, col4= st.columns(2)

# Les colonnes
with col3 :
    st.link_button("Section 1 : Harmonisation des datasets", url="/Partie_2_-_Harmonisation_des_datasets")

with col4 :
    st.link_button("Section 2 : Les graphiques intéractifs avec Plotly", url="/Partie_2_-_Visualisation_avec_Plotly")



st.write("")
st.write("")
st.divider()
# Annexes et telechargement des notebooks sur mon github
st.subheader("Annexes")
st.markdown("""
    Télécharger mes notebooks sur mon Github.
""")
st.image(image="./images/github-white.png", width=100)
st.link_button("Lien Github", url="https://github.com/RashOps/projet-data-visualisation", icon="🔗")
