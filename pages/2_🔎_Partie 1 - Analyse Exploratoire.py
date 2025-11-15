"""
Page "Processus" : Analyse Exploratoire et Nettoyage (Netflix).

Ce script correspond à la page "2_🔎_Partie 1 - Analyse Exploratoire"
de l'application. Son objectif est de documenter le processus
d'analyse exploratoire (EDA) et de nettoyage des données brutes,
conformément au cahier des charges de la Partie 1.

Il contient : 
1.  Le chargement du dataset original (`netflix_titles.csv`).
2.  L'analyse descriptive des problèmes (valeurs nulles, types
    de données incorrects, colonnes inutiles).
3.  Le code de nettoyage et de Feature Engineering (ex: `lag_time`,
    `main_country`), expliqué avec `st.echo`.
4.  La présentation du DataFrame final (`netflix_cleaned.csv`)
    et un bouton pour le télécharger.

Cette page est le "making-of" qui prépare les données pour la page
de visualisation suivante : "3_📈_Visualisation Seaborn".
"""

# Importation des dépendances
import pandas as pd
import streamlit as st
import numpy as np
from data_loader import load_netflix_data_cleaning 

# Configuration de la page principale
st.set_page_config(
    page_title="Analyse et Cleaning du dataset Netflix",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state = "expanded"
)

# Faute d'orthographe
st.sidebar.subheader("Analyse Exploratoire & Cleaning 🔎")

# Titre de la page
st.title("Analyse exploratoire et nettoyage du dataset")

# Visualisation du dataset original
st.subheader("Chargement du DataFrame Brut")

# Gestion d'erreur critique 
netflix = load_netflix_data_cleaning()

if netflix is None:
    st.error("Échec du chargement du fichier 'netflix_titles.csv'. Vérifiez le dossier '/data'.")
    st.stop() 

st.dataframe(netflix, use_container_width=True)

# Analyse exploratoire du dataframe
st.subheader("Analyse du dataframe")
st.markdown("""
    La commande `netflix.info()` nous permet de constater que notre dataframe contient plusieurs valeurs **null** (ou `NaN`), ainsi que des données inexploitables en l'état pour notre analyse.

    Par exemple, la colonne `date_added` est de type `object` (texte) et non `datetime`, c'est-à-dire un format de date non exploitable directement.

    De plus, notre dataframe contient des colonnes comme `description`, `director`, `cast`, et `rating`. Celles-ci seront peu utiles pour notre analyse et **ne seront pas incluses** dans notre sélection de colonnes finale.
""")


st.write("")
st.divider()
# =====================================================================================================================
# Début de l'analyse
st.subheader("Étape 1 : Convertir la date en un format compréhensible par Pandas")

st.markdown("""
    La première étape sera de convertir `date_added` à l'aide du script ci-dessous. Actuellement de type `object` (texte) et mal formatée, 
    nous allons la transformer en un format de date exploitable, c'est-à-dire en `datetime64`.
""")

with st.expander("Découvrir le code"):
    with st.echo():
        # Conversion de 'date_added' (objet) en 'date_added_feature' (datetime)
        # .str.strip() supprime les espaces blancs en début et en fin
        netflix['date_added_feature'] = netflix['date_added'].str.strip()
        netflix['date_added_feature'] = pd.to_datetime(netflix['date_added_feature'], errors='coerce')

        # création de la colonne 'year_added' : Extraction de l'année
        netflix['year_added'] = netflix['date_added_feature'].dt.year

        # création de la colonne 'month_added' : Extraction du mois
        netflix['month_added'] = netflix['date_added_feature'].dt.month

        # création de la colonne 'added_day_of_week' : Extraction du jour d'ajout
        netflix['added_day_of_month'] = netflix['date_added_feature'].dt.day

        # Création de la colonne 'lag_time' : durée entre l'ajout et la sortie
        netflix['lag_time'] = netflix['year_added'] - netflix['release_year']

st.dataframe(netflix.head(), use_container_width=True)

st.markdown("""
    En effectuant ce bloc de script, on **obtient** 5 nouvelles colonnes exploitables :

    * `date_added_feature` : La date correctement formatée.
    * `year_added` : L'année d'ajout sur Netflix.
    * `month_added` : Le mois d'ajout sur Netflix.
    * `added_day_of_month` : Le jour du mois de l'ajout (ex: 25).
    * `lag_time` : Le délai (en années) entre la sortie du film et son ajout.
""")

# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 2 : Séparer la durée des films de celles des séries")

st.markdown("""
    Cette seconde étape consistera à **séparer** la durée des films (ex: "90 min") de celles des séries (ex: "2 Seasons"), qui sont mélangées dans la colonne `duration`.
    Nous allons les formater et les convertir en valeurs numériques (`float`).
""")

with st.expander("Découvrir le code"):
    with st.echo():
        # Initialisation des colonnes à remplir
        netflix['duration_min'] = np.nan # Colonne pour la durée des films
        netflix['duration_seasons'] = np.nan # Colonne pour le nombre de saisons

        # Création des masques pour séparer Films et Séries
        mask_films = (netflix['type'] == 'Movie') & (netflix['duration'].notna())
        mask_series = (netflix['type'] == 'TV Show') & (netflix['duration'].notna())

        # Application des masques et séparation
        # Durée des films
        netflix.loc[mask_films, 'duration_min'] = netflix.loc[mask_films, 'duration'].str.replace(' min', '').astype(float)

        # Durée des séries
        netflix.loc[mask_series, 'duration_seasons'] = netflix.loc[mask_series, 'duration'].str.replace(' Seasons', '').str.replace(' Season', '').astype(float)

st.dataframe(netflix.head(), use_container_width=True)

st.markdown("""
    À l'aide du script précédent, on obtient two nouvelles colonnes numériques :
    * `duration_min` : Contient la durée **uniquement** pour les films.
    * `duration_seasons` : Contient le nombre de saisons **uniquement** pour les séries.
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 3 : Extraire le pays et le genre principaux")

st.markdown("""
    Les colonnes `country` et `listed_in` peuvent contenir plusieurs valeurs (ex: "United States, France, Canada").
    Pour simplifier l'analyse, nous partons du principe que le **premier élément** de la liste est l'élément principal.
""")

with st.expander("Découvrir le code"):
    with st.echo():
        # Pour les pays 
        netflix['main_country'] = netflix['country'].str.split(',').str[0]

        # Pour les catégories
        netflix['main_genre'] = netflix['listed_in'].str.split(',').str[0]

st.dataframe(netflix.head(), use_container_width=True)

st.markdown("""
    Ce script nous permet d'obtenir **deux** nouvelles colonnes exploitables :
    * `main_country` : Le pays de production principal.
    * `main_genre` : Le genre principal.
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 4 : Sélectionner les colonnes et créer le DataFrame nettoyé")

st.markdown("""
    Notre nettoyage est terminé. Il ne nous reste plus qu'à sélectionner les colonnes qui nous seront utiles pour l'analyse et à créer notre dataset final.
""")

with st.expander("Découvrir le code"):
    with st.echo():
        # Ma liste de colonnes finales
        columns_final = [
            'show_id', 
            'type', 
            'title', 
            'main_country', 
            'main_genre', 
            'release_year', 
            'date_added_feature',
            'year_added', 
            'month_added', 
            'added_day_of_month', 
            'lag_time', 
            'duration_min', 
            'duration_seasons'
        ]

        # Nouveau dataframe :
        netflix_cleaned = netflix[columns_final].copy()

st.dataframe(netflix_cleaned.head(), use_container_width=True)

st.write("""
    Ainsi, notre travail de data cleaning prend fin.
    Vu la configuration de notre nouveau dataframe, une suppression simple des valeurs nulles nous ferait perdre une grande quantité d'informations, ce qui **biaiserait** nos futures analyses.

    **Téléchargez** le nouveau dataframe ci-dessous 👇.
""")


# =====================================================================================================================
# Telecharger notre dataframe en csv
# Optimisation (Mise en cache du 'to_csv')
@st.cache_data
def convert_df_to_csv(df):
    """Convertit un DataFrame en CSV (encodé en UTF-8) en mémoire."""
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(netflix_cleaned)

# Le bouton de téléchargement
st.download_button(
    label="Télécharger le DataFrame nettoyé (netflix_cleaned.csv)",
    data=csv_data,
    file_name="netflix_cleaned.csv",
    mime="text/csv",
    use_container_width=True
)

# Passer à la partie création des graphiques aprés l'analyse 
st.write("")
st.write("Passez à la visualisation des graphiques avec Seaborn en cliquant sur le bouton ci-dessous.")

st.link_button(
    "Passer à la Visualisation 📈", 
    url="/Partie_1_-_Les_graphiques_Seaborn",
    use_container_width=True
)