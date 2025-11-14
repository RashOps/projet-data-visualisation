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

# Imporation des dépendances
import pandas as pd
import streamlit as st
import numpy as np

# Configuration de la page principale
st.set_page_config(
    page_title="Analyse et Cleaning du dataset Netflix",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state = "expanded"
)

st.sidebar.subheader("Analyse Exporatoire & Cleaning 🔎")

# Titre de la page
st.title("Analayse exploratoire et nettoyage du dataset")

# Visualisation du dataset original
# Chargmenet du dataframe
from data_loader import load_netflix_data_cleaning
netflix = load_netflix_data_cleaning()
st.dataframe(netflix)

# Analyse exploratoire du dataframe
st.subheader("Analyse du dataframe")
st.markdown("""
    La commande `netflix.info()` nous permet de constater que notre dataframe contient plusieurs valeurs **null** (ou `NaN`), ainsi que des données inexploitables en l'état pour notre analyse.

    Par exemple, la colonne `date_added` est de type `object` (texte) et non `datetime`, c'est-à-dire un format de date non exploitable directement.

    De plus, notre dataframe contient des colonnes comme `description` (la description du film), `director` (le réalisateur), `cast` (le casting des acteurs), `title` (le titre) et `rating`. Celles-ci seront peu utiles pour notre analyse et il faudra effectuer une sélection à la fin de notre nettoyage.
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

with st.expander("Découvrir le code") : 
    with st.echo():
        # Imporation des dépendances
        import pandas as pd
        
        # Conversion de 'date_added' (objet) en 'date_added_feature' (datetime)
        netflix['date_added_feature'] = netflix['date_added'].str.strip() # Suppression des espaces blancs en debut et en fin
        netflix['date_added_feature'] = pd.to_datetime(netflix['date_added_feature'], errors='coerce')

        # création de la colonne 'year_added' à partir de 'date_added_feature' : Extraction de l'année d'ajout 
        netflix['year_added'] = netflix['date_added_feature'].dt.year

        # création de la colonne 'month_added' à partir de 'date_added_feature' : Extraction du mois d'ajout 
        netflix['month_added'] = netflix['date_added_feature'].dt.month

        # création de la colonne 'added_day_of_week' à partir de 'date_added_feature' : Extraction du jour d'ajout 
        netflix['added_day_of_week'] = netflix['date_added_feature'].dt.day

        # Création de la colonne 'lag_time' : qui est la durée entre l'ajout sur netflix et la sortie
        netflix['lag_time'] = netflix['year_added'] - netflix['release_year']

st.dataframe(netflix.head())

st.markdown("""
    En effectuant ce bloc de script, on **obtient** 5 nouvelles colonnes utilisables et compréhensibles par Pandas :

    * `date_added_feature` : La date correctement formatée et compréhensible par Pandas.
    * `year_added` : L'année d'ajout sur la plateforme Netflix.
    * `month_added` : Le mois d'ajout sur la plateforme Netflix.
    * `day_added` : Le jour d'ajout sur la plateforme Netflix.
    * `lag_time` : Le délai entre la sortie du film et son ajout sur Netflix.
            
    Ces nouvelles colonnes nous seront utiles pour la réalisation de graphiques et d'analyses, contrairement à la colonne de base qui était mal formatée et inexploitable.
""")

# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 2 : Séparer la durée des films de celles des séries pour les rendre compréhensibles et exploitables")

st.markdown("""
    Cette seconde étape consistera à **séparer** la durée des films de celles des séries, qui se présentent actuellement sous forme d'**`object`** (texte). 
    Nous allons ensuite les formater correctement, avant de les convertir en valeurs numériques (`float`) afin de les exploiter.
""")

with st.expander("Découvrir le code") : 
    with st.echo() :
        # Initialisation des colonnes à remplir
        netflix['duration_min'] = np.nan # permet de créer une colonne pour la durée des film
        netflix['duration_seasons'] = np.nan # permet de créer une colonne pour le nombre de saison des séries

        # Création des masques servant a departager les films et series
        mask_films = ((netflix['type']=='Movie') & (netflix['duration'].notna())) # Masque pour les films
        mask_series = ((netflix['type']=='TV Show') & (netflix['duration'].notna())) # Masque pour les séries

        # Application des masques et séparation des films et series
        # Durée des films
        netflix.loc[mask_films, 'duration_min'] = netflix.loc[mask_films, 'duration'] # Application du masque film sur la colonne et extraction de la duree des film
        netflix['duration_min'] = netflix['duration_min'].str.replace(' min', '').astype(float) # Conversion de la duree qui en 'str' en 'float'

        # Durée des séries
        netflix.loc[mask_series, 'duration_seasons'] = netflix.loc[mask_series, 'duration'] # Application du masque series sur la colonne et extraction de la duree des series
        netflix['duration_seasons'] = netflix['duration_seasons'].str.replace(' Seasons', '').str.replace(' Season', '').astype(float) # Conversion de la duree qui en 'str' en 'float'

st.dataframe(netflix.head())

st.markdown("""
    À l'aide du script précédent, on obtient deux nouvelles colonnes utilisables et compréhensibles par Pandas :

    * `duration_min` : qui correspond **uniquement** à la durée des films (en minutes).
    * `duration_seasons` : qui fait référence **uniquement** au nombre de saisons pour les séries.
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 3 : Extraire le pays de production et le genre principal de chaque film et série")

st.markdown("""
    Cette étape consistera à extraire le genre principal et le pays de production de chaque film et série, 
    en partant du principe que le premier élément de chaque cellule est l'élément principal. 
""")

with st.expander("Découvrez le code") :  
    with st.echo() :
        # Pour les pays 
        netflix['main_country'] = netflix['country'].str.split(',').str[0]

        # Pour les catégories
        netflix['main_genre'] = netflix['listed_in'].str.split(',').str[0]

st.dataframe(netflix.head())

st.markdown("""
    Ce script précédent nous permet d'obtenir **deux** nouvelles colonnes utilisables et compréhensibles par Pandas :

    * `main_country` : qui correspond au pays de production du film ou de la série.
    * `main_genre` : qui fait référence au genre de la série ou du film.
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Étape 4 : Sélectionner les colonnes exploitables et télécharger un nouveau dataset nettoyé")

st.markdown("""
    À cette étape, notre nettoyage est terminé. Il ne nous reste plus qu'à sélectionner les colonnes qui nous seront utiles et à les sauvegarder dans un nouveau dataset.
""")

with st.expander("Découvrir le code") : 
    with st.echo() :
        # Ma liste de colonnes final
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
            'added_day_of_week', 
            'lag_time', 
            'duration_min', 
            'duration_seasons'
        ]

        # Nouveau dataframe :
        netflix_cleaned = netflix[columns_final].copy()

st.dataframe(netflix_cleaned.head())

st.write("""
    Ainsi, notre travail de data cleaning prend fin.
    Vu la configuration de notre nouveau dataframe, une suppression simple des valeurs nulles nous ferait perdre une grande quantité d'informations, ce qui **biaiserait** nos futures analyses.

    Téléchargez le nouveau dataframe ci-dessous 👇.
""")


# =====================================================================================================================
# Telecharger notre dataframe en csv
csv_data = netflix_cleaned.to_csv(index=False) 

# Le bouton de téléchargement
st.download_button(
    label="Télécharger le nouveau dataframe nettoyé en CSV",
    data=csv_data,
    file_name="netflix_cleaned.csv",
    mime="text/csv",
)

# Passer à la partie création des graphiques aprés l'analyse 
st.write("")
st.write("Passer à la visualisation des graphes avec Seaborn en cliquant sur le bouton ci-dessous.")
st.link_button("Cliquez-ici ", url="/Partie_1_-_Les_graphiques_Seaborn")