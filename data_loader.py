# data_loader.py
import pandas as pd
import streamlit as st

# ===================================================================================
# Netflix section 1
@st.cache_data 
def load_netflix_data_cleaning():
    try : 
        netflix = pd.read_csv('./data/netflix_titles.csv') 
        return netflix
    except FileNotFoundError :
        st.error("ERREUR : Le fichier 'netflix_titles.csv' est manquant dans le dossier '/data'.")
        return None


# Netflix section 2
@st.cache_data 
def load_netflix_data_analysis():
    try : 
        df = pd.read_csv('./data/netflix_cleaned.csv')
        return df
    except FileNotFoundError :
        st.error("ERREUR : Le fichier 'netflix_cleaned.csv' est manquant dans le dossier '/data'.")
        return None

# ===================================================================================
# World Happiness section 1
@st.cache_data
def load_happiness_data_cleaning():
    df_2015 = pd.read_csv('./data/2015.csv')
    df_2016 = pd.read_csv('./data/2016.csv')
    df_2017 = pd.read_csv('./data/2017.csv')
    df_2018 = pd.read_csv('./data/2018.csv')
    df_2019 = pd.read_csv('./data/2019.csv')

    # Régularisation des dataframes
    # 1. Définition des dictionnaires de renommage pour chaque année

    COLS_2015 = {
        'Country': 'Country',
        'Region': 'Region',
        'Happiness Rank': 'Rank',
        'Happiness Score': 'Score',
        'Economy (GDP per Capita)': 'GDP_per_Capita',
        'Family': 'Social_Support',
        'Health (Life Expectancy)': 'Health_Life_Expectancy',
        'Freedom': 'Freedom',
        'Trust (Government Corruption)': 'Trust_Government_Corruption',
        'Generosity': 'Generosity'
    }

    COLS_2016 = {
        'Country': 'Country',
        'Region': 'Region',
        'Happiness Rank': 'Rank',
        'Happiness Score': 'Score',
        'Economy (GDP per Capita)': 'GDP_per_Capita',
        'Family': 'Social_Support',
        'Health (Life Expectancy)': 'Health_Life_Expectancy',
        'Freedom': 'Freedom',
        'Trust (Government Corruption)': 'Trust_Government_Corruption',
        'Generosity': 'Generosity'
    }

    # Note : 2017 n'a pas de 'Region'
    COLS_2017 = {
        'Country': 'Country',
        'Happiness.Rank': 'Rank',
        'Happiness.Score': 'Score',
        'Economy..GDP.per.Capita.': 'GDP_per_Capita',
        'Family': 'Social_Support',
        'Health..Life.Expectancy.': 'Health_Life_Expectancy',
        'Freedom': 'Freedom',
        'Trust..Government.Corruption.': 'Trust_Government_Corruption',
        'Generosity': 'Generosity'
    }

    # Note : 2018/2019 n'ont pas de 'Region' et les noms diffèrent
    COLS_2018 = {
        'Country or region': 'Country',
        'Overall rank': 'Rank',
        'Score': 'Score',
        'GDP per capita': 'GDP_per_Capita',
        'Social support': 'Social_Support',
        'Healthy life expectancy': 'Health_Life_Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust_Government_Corruption',
        'Generosity': 'Generosity'
    }

    # 2019 est identique à 2018
    COLS_2019 = {
        'Country or region': 'Country',
        'Overall rank': 'Rank',
        'Score': 'Score',
        'GDP per capita': 'GDP_per_Capita',
        'Social support': 'Social_Support',
        'Healthy life expectancy': 'Health_Life_Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust_Government_Corruption',
        'Generosity': 'Generosity'
    }

    # 2. Création d'une liste vide pour stocker nos DataFrames nettoyés
    dfs_to_concat = []

    try:
        # --- 2015 ---
        # On ne garde que les colonnes qui nous intéressent et on les renomme
        df_2015 = df_2015[list(COLS_2015.keys())].rename(columns=COLS_2015)
        df_2015['Year'] = 2015 # Ajout de la colonne 'Year'
        dfs_to_concat.append(df_2015)
        print("Fichier 2015 traité.")
        
        # --- 2016 ---
        df_2016 = df_2016[list(COLS_2016.keys())].rename(columns=COLS_2016)
        df_2016['Year'] = 2016
        dfs_to_concat.append(df_2016)
        print("Fichier 2016 traité.")
        
        # Création de la table de correspondance pour les Régions 
        # La colonne 'Region' disparaît après 2017. Nous la sauvegardons pour la ré-appliquer aux autres années.
        region_map = df_2016[['Country', 'Region']].drop_duplicates().set_index('Country')['Region']
        
        # --- 2017 ---
        df_2017 = df_2017[list(COLS_2017.keys())].rename(columns=COLS_2017)
        df_2017['Year'] = 2017
        df_2017['Region'] = df_2017['Country'].map(region_map) # On applique la map
        dfs_to_concat.append(df_2017)
        print("Fichier 2017 traité (régions ajoutées).")
        
        # --- 2018 ---
        df_2018 = df_2018[list(COLS_2018.keys())].rename(columns=COLS_2018)
        df_2018['Year'] = 2018
        df_2018['Region'] = df_2018['Country'].map(region_map) # On applique la map
        dfs_to_concat.append(df_2018)
        print("Fichier 2018 traité (régions ajoutées).")

        # --- 2019 ---
        df_2019 = df_2019[list(COLS_2019.keys())].rename(columns=COLS_2019)
        df_2019['Year'] = 2019
        df_2019['Region'] = df_2019['Country'].map(region_map) # On applique la map
        dfs_to_concat.append(df_2019)
        print("Fichier 2019 traité (régions ajoutées).")
        
        # 3. Concaténation 
        # C'est l'étape finale. On empile tous les DataFrames de la liste.
        df_final = pd.concat(dfs_to_concat, ignore_index=True)
        
        print("\n--- Concaténation terminée ! ---")
        
        # 4. Vérification et Sauvegarde
        print(f"Dimensions du DataFrame final : {df_final.shape}")
        print("\nInfos sur le DataFrame final :")
        df_final.info()
        
        print("\nAperçu (5 dernières lignes) :")
        print(df_final.tail())
        
        output_filename = "world_happiness_2015-2019_combined.csv"
        # Pour ne pas telechrager le fichier en executant le code ----
        # df_final_csv = df_final.to_csv(output_filename, index=False) 
        print(f"\nDataFrame final sauvegardé sous : {output_filename}")
        
    except FileNotFoundError as e:
        print(f"ERREUR : Fichier manquant. Assurez-vous que tous les CSV (2015-2019) sont présents.")
        print(e)
    except KeyError as e:
        print(f"ERREUR : Une colonne attendue n'a pas été trouvée. Vérifiez les dictionnaires de renommage.")
        print(e)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
    return df_final

# Mise en cache de tous les datasets world happiness report 2015 - 2019
@st.cache_data
def load_happiness_all_df():
    try :
        df_2015 = pd.read_csv('./data/2015.csv')
        df_2016 = pd.read_csv('./data/2016.csv')
        df_2017 = pd.read_csv('./data/2017.csv')
        df_2018 = pd.read_csv('./data/2018.csv')
        df_2019 = pd.read_csv('./data/2019.csv')
        return df_2015, df_2016, df_2017, df_2018, df_2019
    except FileNotFoundError :
        st.error("ERREUR : Le fichier 'world_happiness_2015-2019_combined.csv' est manquant dans le dossier '/data'.")
        return None

# World Happiness section 2
@st.cache_data
def load_happiness_data_analysis():
    try : 
        world_happiness_report = pd.read_csv("./data/world_happiness_2015-2019_combined.csv")
        return world_happiness_report
    except FileNotFoundError :
        st.error("ERREUR : Le fichier 'world_happiness_2015-2019_combined.csv' est manquant dans le dossier '/data'.")
        return None