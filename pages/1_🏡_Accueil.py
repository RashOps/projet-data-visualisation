"""
Page d'Accueil et Sommaire de l'Application (1_🏡_Accueil.py).

Ce script est la page d'atterrissage (landing page) principale
de l'application.

Son rôle est de :
1.  **Décrire** le projet : présenter le cahier des charges,
    les datasets (Netflix, World Happiness) et les objectifs.
2.  **Guider** l'utilisateur : agir comme un sommaire visuel
    en centralisant les liens vers les deux composantes principales
    du projet :
    * Le **Produit Fini** (le Dashboard interactif).
    * Le **Processus Académique** (les pages de "making-of" :
        Nettoyage et Visualisation statique).
"""

# Imporation des dépendances
import streamlit as st

# Configuration de la page principale
st.set_page_config(
    page_title="Accueil | Projet Data-Viz",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.subheader("Accueil 🏡")

# --- SECTION HAUT (Titre et Description) ---
st.title("Projet de Data Visualisation")
st.image(image="./images/projet-data.jpg", use_container_width=True)

st.header("Description du projet")
st.markdown(
"""
**2 Étapes**, **2 Jeux de Données**

Analyser deux jeux de données distincts à l'aide des librairies **Seaborn** et **Plotly**, et 
produire des visualisations claires, esthétiques et informatives pour mettre en avant des 
faits marquants.
"""
)

st.divider()

# --- SECTION 1 : Le Produit Fini (Le plus important) ---
st.header("🚀 Le Produit Fini : Dashboard Interactif")
st.markdown(
"""
C'est la pièce maîtresse du projet. Un dashboard intéractif complet qui combine les deux datasets en un seul outil d'exploration.

* **Sidebar Dynamique :** Les filtres s'adaptent au dataset que vous choisissez.
* **KPIs en Temps Réel :** Les chiffres clés se mettent à jour avec vos sélections.
* **Graphiques Interactifs :** Comparez les données à la volée.
"""
)

# Mettre le bouton en évidence
cols_dash = st.columns([1, 2, 1]) # Crée 3 colonnes, [milieu] est 2x plus large
with cols_dash[1]:
    st.link_button(
        "Accéder au Dashboard Interactif 📝", 
        url="/Dashboard", # L'URL vient du titre de st.Page dans app.py
        use_container_width=True # Fait un gros bouton
    )

st.divider()

# --- SECTION 2 : L'Analyse Détaillée (Le "Making-of") ---
st.header("📚 L'Analyse Détaillée (Le 'Making-of')")
st.markdown(
"""
Conformément au cahier des charges, cette section présente l'analyse **étape par étape**,
en montrant le processus de **nettoyage** et de **visualisation** pour chaque dataset.
"""
)

# Utiliser des onglets (st.tabs) est plus propre
tab1, tab2 = st.tabs(["Partie 1 : Netflix (Seaborn)", "Partie 2 : World Happiness (Plotly)"])

with tab1:
    st.subheader("Partie 1 : Netflix (Seaborn)")
    st.image("./images/partie1-image.jpg", use_container_width=True)
    st.markdown("""
    **Objectif :** Utiliser Seaborn pour une analyse statistique.
    
    * **Étape 1 :** Voir le processus de nettoyage du dataset.
    * **Étape 2 :** Voir le rapport de visualisation statique (graphiques et analyses).
    
    [Dataset utilisé disponible ici](https://www.kaggle.com/datasets/shivamb/netflix-shows)
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        st.link_button(
            "Analyse & Cleaning 🔎", 
            url="/Partie_1_-_Analyse_Exploratoire", 
            use_container_width=True
        )
    with c2:
        st.link_button(
            "Visualisation Seaborn 📈", 
            url="/Partie_1_-_Les_graphiques_Seaborn", 
            use_container_width=True
        )

with tab2:
    st.subheader("Partie 2 : World Happiness (Plotly)")
    st.image("./images/partie2-image.png", use_container_width=True)
    st.markdown("""
    **Objectif :** Utiliser Plotly pour une analyse interactive.
    
    * **Étape 1 :** Voir le processus d'harmonisation des 5 datasets.
    * **Étape 2 :** Voir le rapport de visualisation interactif (graphiques et analyses).
    
    [Dataset utilisé disponible ici](https://www.kaggle.com/datasets/unsdsn/world-happiness)
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        st.link_button(
            "Harmonisation des datasets ♻️", 
            url="/Partie_2_-_Harmonisation_des_datasets", 
            use_container_width=True
        )
    with c2:
        st.link_button(
            "Visualisation Plotly 📊", 
            url="/Partie_2_-_Visualisation_avec_Plotly", 
            use_container_width=True
        )


st.write("")
st.write("")
st.divider()
# Annexes et telechargement des notebooks sur mon github
st.subheader("Annexes")
st.markdown("""
    Télécharger les notebooks utilisés sur mon Github.
""")
st.image(image="./images/github-white.png", width=100)
st.link_button("Lien Github", url="https://github.com/RashOps/projet-data-visualisation", icon="🔗")