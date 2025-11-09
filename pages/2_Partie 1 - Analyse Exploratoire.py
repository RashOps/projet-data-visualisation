# Imporation des dépendances
import pandas as pd
import streamlit as st
import numpy as np

# Configuration de la page principale
st.set_page_config(
    page_title="Partie 1 - Analyse Exporatoire",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state = "expanded"
)

# Titre de la page
st.title("Analayse exploratoire et nettoyage du dataset")

# Visualisation du dataset original
netflix = pd.read_csv('./data/netflix_titles.csv')
st.dataframe(netflix)

# Analyse exploratoire du dataframe
st.subheader("Analyse du dataframe")
st.markdown("""
    La commande "netflix.info()" nous permet deconstater que notre dataframe contient plusieurs valeurs *'null'*
    des données inexploitables dans notre analyses, telles que 'date_added' qui est un *objet* et pas un *datetime*, c'est à dire une date exploitable.
    De plus notre dataframe contient des colonnes comme la description du film 'description', le nom du directeur 'director', le casting des acteurs 'cast', 
    le titre du film 'title', et la colonne 'rating' qui seront peu utile pour notre qu'il faudra eliminer a la fin de notre nettoyage.
""")


st.write("")
st.divider()
# =====================================================================================================================
# Début de l'analyse
st.subheader("Etape 1 : Convertir la date en en une donnée compréhensible par pandas")

st.markdown("""
    La première étape sera de convertir à l'aide du script ci-dessous 'date_added' qui est présentement un ***objet*** et mal formaté, 
    en vrai date, c'est à dire en ***datetime64*** afin de pourvoir l'exploiter correctement.
""")

with st.echo():
    # Imporation des dépendances
    import pandas as pd
    
    # Conversion de 'date_added' (objet) en 'date_added_feature' (datetime)
    netflix['date_added_feature'] = netflix['date_added'].str.strip() # Elimine les espaces blancs en debut et en fin
    netflix['date_added_feature'] = pd.to_datetime(netflix['date_added_feature'], errors='coerce') # Permet de forcer la conversion en réelle dat exploitable

    # creation de la colonne 'year_added' a partir de 'date_added_feature' : Extraction de l'année d'ajout 
    netflix['year_added'] = netflix['date_added_feature'].dt.year

    # creation de la colonne 'month_added' a partir de 'date_added_feature' : Extraction du mois d'ajout 
    netflix['month_added'] = netflix['date_added_feature'].dt.month

    # creation de la colonne 'added_day_of_week' a partir de 'date_added_feature' : Extraction du jour d'ajout 
    netflix['added_day_of_week'] = netflix['date_added_feature'].dt.day

    # Creation de la colonne 'lag_time' : qui est la durée entre l'ajout sur netflix et la sortie
    netflix['lag_time'] = netflix['year_added'] - netflix['release_year']

    st.dataframe(netflix.head())

st.markdown("""
    En effectuant ce bloc de script on optient 5 nouvelles colonnes utilisables et comprenables par pandas : \n
    - '**date_added_feature**' : La date correctement formaté et compréhensible par pandas \n
    - '**year_added**' : L'année d'ajout sur la plateforme Netflix \n
    - '**month_added**' : Le mois d'ajout sur la plateforme Netflix  \n
    - '**day_added**' : Le jour d'ajout sur la plateforme Netflix   \n
    - '**lag_time**' : Le délai entre la sortie du film et son ajout sur Netflix \n
""")

st.write("""
    Ces nouvelles colonnes obtenues, nous serons utiles à la réalisation de graphiques et d'analyse,
    que la colonne de base qui était mal formatée et inexploitable.
""")

# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Etape 2 : Séparer la durée des films de celles des séries pour les rendre compréhensibles et exploitables")

st.markdown("""
    Cette seconde étape va consister à la durée des films de celles des séries qui se presentent sous forme d'***objet***, 
    puis les formater correctment, avant de les convertir en valeurs numériques (***float***) afin de les exploiter.
""")

with st.echo() :
    # Initialisation des colonnes a remplir
    netflix['duration_min'] = np.nan # permet de creer un colonne pour la duree des film
    netflix['duration_seasons'] = np.nan # permet de creer une colonne pour le nombre de saison des series

    # Création des masques servant a departager les films et series
    mask_films = ((netflix['type']=='Movie') & (netflix['duration'].notna())) # Masque pour les films
    mask_series = ((netflix['type']=='TV Show') & (netflix['duration'].notna())) # Masque pour les series

    # Application des masques et séparation des films et series
    # .loc[masque_films, 'colonne_à_remplir'] = ...
    # Durée des films
    netflix.loc[mask_films, 'duration_min'] = netflix.loc[mask_films, 'duration'] # Application du masque film sur la colonne et extraction de la duree des film
    netflix['duration_min'] = netflix['duration_min'].str.replace(' min', '').astype(float) # Conversion de la duree qui en 'str' en 'float'

    # Durée des séries
    netflix.loc[mask_series, 'duration_seasons'] = netflix.loc[mask_series, 'duration'] # Application du masque series sur la colonne et extraction de la duree des series
    netflix['duration_seasons'] = netflix['duration_seasons'].str.replace(' Seasons', '').str.replace(' Season', '').astype(float) # Conversion de la duree qui en 'str' en 'float'

    st.dataframe(netflix.head())

st.markdown("""
    à l'aide du script précedent on obtient 2 nouvelles colonnes utilisables et comprenables par pandas : \n
    - '**duration_min**' : qui correspond **uniquement** à la durée des films \n
    - '**duration_seasons**' : qui fait reference **uniquement** à la durée des séries \n
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Etape 3 : Extraire le pays de production et le genre principal de chaque film et séries")

st.markdown("""
    Cette étape consistera à extraire le genre principal et le pays de production de chaque films et séries,
    en partant du principe que le premier élément de chaque case est l'élément principal. 
""")

with st.echo() :
    # Extraction de la categorie principal et pays de chaque film et series

    # En partant du principe que le premier pays listé est le pays principal
    # Pareil pour la catégorie, en partant du principe que la première catégorie de la liste est la catégorie principal


    # Pour les pays
    # .str.split(',') : Coupe la chaîne à chaque virgule (renvoie une liste)
    # .str[0]         : Sélectionne le premier élément de cette liste
    netflix['main_country'] = netflix['country'].str.split(',').str[0]

    # Pour les catégories
    netflix['main_genre'] = netflix['listed_in'].str.split(',').str[0]

    st.dataframe(netflix.head())

st.markdown("""
    Ce script précedent nous permet d'obtenir 2 nouvelles colonnes utilisables et comprenables par pandas : \n
    - '**main_country**' : qui correspond au pays de production du films ou de la séries \n
    - '**main_genre**' : qui fait reference au genre de la série ou du film \n
""")


# =====================================================================================================================
st.write("")
st.divider()
st.subheader("Etape 4 : Sélectionner les colonnes exploitables et telecharger un nouveau dataset nettoyé")

st.markdown("""
    A cette étape, notre nettoyage est terminé. Il ne nous reste plus qu'a selectionné les colonnes qui nous serons utiles,
    Et les sauvegarder comme une nouveux dataset.
""")

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
    Ainsi notre travail de data cleaning prend, et vu la configuaration de notre nouveau dataframe,
    supprimer les valeurs nulles, nous ferait perdre une grande quantité de données qui biaiseront nos données.
         
    Telecharger le nouveau dataframe ci-dessous👇.
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
st.write("Passez à la visualisation des graphes avec Seaborn en cliquant sur le bouton ci-dessous.")
st.link_button("Cliquez-ici ", url="/Partie_1_-_Les_graphiques_Seaborn")