# Importation des dépendances
import pandas as pd
import streamlit as st
from data_loader import load_happiness_all_df

# Configuration de la page principale
st.set_page_config(
    page_title="Harmonisation des datasets World Happiness Report 2015-2019",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state = "expanded"
)

st.sidebar.subheader("Harmonisation des différents datasets (2015 - 2019) ♻️")

# ===========================================================================================================================
st.title("Harmonisation des datasets : World Happiness Report")

# =============================================================================================================================
st.subheader("Analyse de nos datasets")

# Mise en cache et Chargement des datasets
loaded_data = load_happiness_all_df()

if loaded_data is None:
    st.error("Échec du chargement des fichiers de données brutes. Vérifiez le dossier '/data'.")
    st.stop() # Arrête l'exécution de la page si les données sont manquantes

df_2015, df_2016, df_2017, df_2018, df_2019 = loaded_data

# Création des colonnes
col_2015_2017, col_2016_2018 = st.columns(2)
col_2019_1, col_2019_2, col_2019_3 = st.columns(3)

# Affichage de nos dataframes
with col_2015_2017 :
    st.write("Dataframe de l'année 2015")
   
    st.dataframe(df_2015, use_container_width=True)
    st.write("Dataframe de l'année 2017")
    st.dataframe(df_2017, use_container_width=True)

with col_2016_2018 :
    st.write("Dataframe de l'année 2016")
    st.dataframe(df_2016, use_container_width=True)
    st.write("Dataframe de l'année 2018")
    st.dataframe(df_2018, use_container_width=True)

with col_2019_2 :
    st.write("Dataframe de l'année 2019")
    st.dataframe(df_2019, use_container_width=True)


st.markdown("""
    #### Contexte du Jeu de Données

    Les données utilisées dans ce projet proviennent du **World Happiness Report**, une enquête annuelle de référence sur l'état du bonheur mondial.  
    Pour notre analyse, nous disposons de cinq jeux de données distincts, couvrant les années **2015, 2016, 2017, 2018 et 2019**.

    Le cœur de ce rapport est le **Score de Bonheur (Happiness Score)**, une métrique basée sur *l'échelle de Cantril*, qui demande aux citoyens d'évaluer leur vie sur une échelle de 0 (la pire vie possible) à 10 (la meilleure vie possible).  

    Pour expliquer les variations de ce score, le rapport fournit des données sur six facteurs clés :  
    - **PIB par Habitant** (Richesse économique)  
    - **Soutien Social** (Famille, amis)  
    - **Espérance de Vie en Bonne Santé** (Santé)  
    - **Liberté** (Liberté de faire ses choix de vie)  
    - **Générosité**  
    - **Confiance** (Perception de la corruption)  
            
    ---

    #### Le Défi : 5 Fichiers, 5 Schémas Différents

    Notre objectif principal est d'analyser **l'évolution temporelle du bonheur et de ses composantes de 2015 à 2019**.  
    Pour ce faire, il est indispensable de **combiner nos 5 fichiers CSV en un seul et unique jeu de données**.

    Cependant, une simple concaténation est impossible. En inspectant les fichiers, nous constatons qu'ils sont **inhérents et incohérents**. Bien qu'ils traitent du même sujet, leur structure (le *schéma*) change d'une année à l'autre.

    ##### Principales Différences Constatées

    ###### 1. Incohérence des Noms de Colonnes
    Les noms des colonnes pour une même métrique ne sont pas standardisés.

    | Indicateur | 2015 | 2017 | 2019 |
    |-------------|------|------|------|
    | Score | Happiness Score | Happiness.Score | Score |
    | PIB | Economy (GDP per Capita) | Economy..GDP.per.Capita. | GDP per capita |
    | Soutien Social | Family | Family | Social support |
    | Confiance | Trust (Government Corruption) | Trust..Government.Corruption. | Perceptions of corruption |

    ###### 2. Incohérence des Schémas (Colonnes Manquantes ou Supplémentaires)
    - **Region** : présente en 2015 et 2016, absente à partir de 2017.  
    - **Colonnes statistiques** comme *Standard Error*, *Dystopia Residual* (2015-2017), *Lower/Upper Confidence Interval* (2016), ou *Whisker.high/low* (2017) apparaissent de manière non uniforme.

    Ces irrégularités compliquent toute tentative d'analyse comparative.
            
    ---

    #### La Nécessité de l'Harmonisation

    Tenter de combiner ces fichiers *en l'état* résulterait en un **DataFrame inutilisable**, rempli de colonnes dupliquées et de valeurs manquantes (*NaN*).  

    Pour mener à bien notre analyse temporelle, un **processus d'harmonisation rigoureux** est donc un prérequis indispensable.

    ##### Étapes du Processus d'Harmonisation

    1. **Définir un Schéma Unifié** :  
    Sélection d'un *noyau commun* de colonnes pertinentes (Score, PIB, Soutien Social, etc.) et suppression des colonnes statistiques non pertinentes.

    2. **Renommer et Nettoyer** :  
    Chargement de chaque fichier individuellement, puis renommage des colonnes pour qu'elles correspondent parfaitement à notre schéma unifié.

    3. **Enrichir les Données** :  
    - Ajout manuel d'une colonne *Year* à chaque fichier (`df_2015['Year'] = 2015`).  
    - “Rétro-ingénierie” de la colonne *Region* manquante pour 2017-2019 en utilisant les données de 2016 comme table de correspondance.

    4. **Concaténer** :  
    Empilement des 5 DataFrames harmonisés en un seul fichier final :  
    **`world_happiness_2015-2019_combined.csv`**.

    C'est ce jeu de données final et propre qui est utilisé pour toutes les **visualisations interactives** du projet.

""")


# ==================================================================================================================
st.divider()
st.write("")
st.write("")
st.subheader("Harmonisation des dataframes")

with st.expander("Découvrir le code"):
    
    with st.echo():
        # Régularisation des dataframes
        # 1. Définition des dictionnaires de renommage pour chaque année
        COLS_2015 = {
            'Country': 'Country', 'Region': 'Region', 'Happiness Rank': 'Rank', 'Happiness Score': 'Score',
            'Economy (GDP per Capita)': 'GDP_per_Capita', 'Family': 'Social_Support',
            'Health (Life Expectancy)': 'Health_Life_Expectancy', 'Freedom': 'Freedom',
            'Trust (Government Corruption)': 'Trust_Government_Corruption', 'Generosity': 'Generosity'
        }
        COLS_2016 = {
            'Country': 'Country', 'Region': 'Region', 'Happiness Rank': 'Rank', 'Happiness Score': 'Score',
            'Economy (GDP per Capita)': 'GDP_per_Capita', 'Family': 'Social_Support',
            'Health (Life Expectancy)': 'Health_Life_Expectancy', 'Freedom': 'Freedom',
            'Trust (Government Corruption)': 'Trust_Government_Corruption', 'Generosity': 'Generosity'
        }
        COLS_2017 = {
            'Country': 'Country', 'Happiness.Rank': 'Rank', 'Happiness.Score': 'Score',
            'Economy..GDP.per.Capita.': 'GDP_per_Capita', 'Family': 'Social_Support',
            'Health..Life.Expectancy.': 'Health_Life_Expectancy', 'Freedom': 'Freedom',
            'Trust..Government.Corruption.': 'Trust_Government_Corruption', 'Generosity': 'Generosity'
        }
        COLS_2018 = {
            'Country or region': 'Country', 'Overall rank': 'Rank', 'Score': 'Score',
            'GDP per capita': 'GDP_per_Capita', 'Social support': 'Social_Support',
            'Healthy life expectancy': 'Health_Life_Expectancy', 'Freedom to make life choices': 'Freedom',
            'Perceptions of corruption': 'Trust_Government_Corruption', 'Generosity': 'Generosity'
        }
        COLS_2019 = COLS_2018 # 2019 est identique à 2018

        # 2. Création d'une liste vide pour stocker nos DataFrames nettoyés
        dfs_to_concat = []

        try:
            # --- 2015 ---
            df_2015 = df_2015[list(COLS_2015.keys())].rename(columns=COLS_2015)
            df_2015['Year'] = 2015
            dfs_to_concat.append(df_2015)
            st.write("Fichier 2015 traité.")
            
            # --- 2016 ---
            df_2016 = df_2016[list(COLS_2016.keys())].rename(columns=COLS_2016)
            df_2016['Year'] = 2016
            dfs_to_concat.append(df_2016)
            st.write("Fichier 2016 traité.")
            
            # Création de la table de correspondance pour les Régions
            region_map = df_2016[['Country', 'Region']].drop_duplicates().set_index('Country')['Region']
            
            # --- 2017 ---
            df_2017 = df_2017[list(COLS_2017.keys())].rename(columns=COLS_2017)
            df_2017['Year'] = 2017
            df_2017['Region'] = df_2017['Country'].map(region_map)
            dfs_to_concat.append(df_2017)
            st.write("Fichier 2017 traité (régions ajoutées).")
            
            # --- 2018 ---
            df_2018 = df_2018[list(COLS_2018.keys())].rename(columns=COLS_2018)
            df_2018['Year'] = 2018
            df_2018['Region'] = df_2018['Country'].map(region_map)
            dfs_to_concat.append(df_2018)
            st.write("Fichier 2018 traité (régions ajoutées).")

            # --- 2019 ---
            df_2019 = df_2019[list(COLS_2019.keys())].rename(columns=COLS_2019)
            df_2019['Year'] = 2019
            df_2019['Region'] = df_2019['Country'].map(region_map)
            dfs_to_concat.append(df_2019)
            st.write("Fichier 2019 traité (régions ajoutées).")
            
            # 3. Concaténation
            df_final = pd.concat(dfs_to_concat, ignore_index=True)
            st.success("--- Concaténation terminée ! ---")
            
            # 4. Vérification et Sauvegarde
            st.write(f"Dimensions du DataFrame final : {df_final.shape}")
            
            output_filename = "world_happiness_2015-2019_combined.csv"
            st.write(f"DataFrame final prêt (non sauvegardé ici, mais disponible en téléchargement).")
            
            # Affichage du résultat (df_final) à l'intérieur de l'expander
            st.subheader("Aperçu du DataFrame Final Harmonisé")
            st.dataframe(df_final.head())

        except KeyError as e:
            st.error(f"ERREUR : Une colonne attendue n'a pas été trouvée. Vérifiez les dictionnaires de renommage.")
            st.error(e)
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {e}")


st.markdown("""
    #### Récapitulatif de l'Harmonisation des Données (2015-2019)
    L'objectif était de combiner 5 fichiers CSV distincts (un pour chaque année de 2015 à 2019) en un seul jeu de données cohésif. Une simple concaténation était impossible car les noms de colonnes (le "schéma") différaient d'une année à l'autre. Le processus suivant a été appliqué pour harmoniser et empiler les données sans perte de lignes.

    ##### Opération 1 : Définition d'un Schéma Unifié ("Colonnes Clés")
    Justification : Pour analyser l'évolution d'une métrique (comme le PIB) dans le temps, elle doit exister dans une seule et même colonne. Nous avons donc défini un "noyau commun" de colonnes pertinentes présentes, sous une forme ou une autre, dans tous les fichiers.

    Colonnes Conservées (Schéma Final) :
    Country (Pays)  
    * Region (Région géographique)  
    * Rank (Le classement)  
    * Score (Le score de bonheur)  
    * GDP_per_Capita (PIB par habitant)  
    * Social_Support (Soutien social/familial)  
    * Health_Life_Expectancy (Espérance de vie en bonne santé)  
    * Freedom (Liberté de faire des choix)  
    * Trust_Government_Corruption (Confiance envers le gouvernement / perception de la corruption)  
    * Generosity (Générosité)  

    ---        

    ##### Opération 2 : Sélection et Renommage (Harmonisation)
    Justification : Chaque fichier a été chargé individuellement, et ses colonnes ont été renommées pour correspondre à notre schéma unifié. Les colonnes non pertinentes ont été intentionnellement supprimées.

    Exemples de Renommage :

    GDP_per_Capita (nouveau nom) provenait de :  
    * Economy (GDP per Capita) (en 2015, 2016)  
    * Economy..GDP.per.Capita. (en 2017)  
    * GDP per capita (en 2018, 2019)  

    Social_Support (nouveau nom) provenait de :  
    * Family (en 2015, 2016, 2017)  
    * Social support (en 2018, 2019)  

    Colonnes Principales Supprimées (et Années) :  
    * Standard Error (2015)  
    * Dystopia Residual (2015, 2016, 2017)  
    * Lower Confidence Interval, Upper Confidence Interval (2016)  
    * Whisker.high, Whisker.low (2017)  

    Justification de la Suppression : Ces colonnes étaient des métadonnées statistiques (comme les marges d'erreur) qui n'étaient pas présentes de manière cohérente dans tous les fichiers. Les conserver aurait créé un DataFrame final avec de nombreuses colonnes vides (NaN), polluant l'analyse temporelle. Nous avons privilégié le "noyau commun" de métriques.

    ---        

    ##### Opération 3 : Création de la Colonne Year
    Justification : Pour effectuer une analyse temporelle (comme px.line()), nous avions besoin d'une colonne indiquant l'année de chaque observation.

    Action : Une colonne Year a été ajoutée à chaque DataFrame avant la fusion (ex: df_2015['Year'] = 2015, df_2016['Year'] = 2016, etc.).

    ---        

    ##### Opération 4 : Rétro-ingénierie de la Colonne Region
    Justification : La colonne Region est cruciale pour le regroupement et la coloration des graphiques (ex: color='Region'). Cependant, elle n'était explicitement présente que dans les fichiers de 2015 et 2016.

    Action :

    Une table de correspondance ("mapping") Pays -> Région a été extraite du fichier de 2016 (qui était complet).  
    Cette table a été utilisée pour "remplir" la colonne Region manquante dans les fichiers de 2017, 2018 et 2019, en se basant sur la colonne Country.  

    Note : Ce processus a réussi à récupérer la majorité des régions (764 sur 782), les 18 NaN restants correspondant à des pays qui n'avaient pas de correspondance dans les données de 2016.

    ---        

    ##### Opération 5 : Concaténation Verticale
    Justification : Assembler les 5 DataFrames (maintenant propres et harmonisés) en un seul grand DataFrame.  
    Action : La fonction pd.concat() a été utilisée pour "empiler" verticalement les DataFrames.  
    Résultat : Un DataFrame unique de 782 lignes (158 + 157 + 155 + 156 + 156) et 11 colonnes (les 10 du schéma + Year), ne conservant que les NaN qui existaient dans les données sources ou qui n'ont pas pu être mappés (pour Region). 
    
    **Aucune ligne n'a été perdue.**
            
    ---
            
    ##### Conclusion
    On obtient un dataframe avec toutes les colonnes importantes et exploitables.
""")


# Création de colonnes
st.write("")
st.markdown("""Téléchargez le nouveau dataframe et passez à la visualisation avec Plotly""")
col_next1, col_next2 = st.columns(2)

# Telechargement du fichier harmonisé
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(df_final) 


with col_next1 :
    st.download_button(
        label="Téléchargez le nouveau DataFrame en CSV",
        data=csv_data, 
        file_name="world_happiness_2015-2019_combined.csv",
        mime="text/csv",
        icon="🗒️",
        use_container_width=True
    )

with col_next2 :
    st.link_button(
        "Les graphiques interactifs avec Plotly", 
        url="/Partie_2_-_Visualisation_avec_Plotly", 
        icon="➡️",
        use_container_width=True
    )