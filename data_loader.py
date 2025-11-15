"""
Module de Chargement et de Mise en Cache des Données (Data Loading).

Ce module centralise toutes les fonctions de lecture des fichiers CSV
pour l'application. Il agit comme la "source unique de vérité" pour
l'accès aux données.

Fonctionnalités Clés :
- Utilise `@st.cache_data` pour mettre en cache les DataFrames en mémoire,
  garantissant des performances optimales et un re-chargement instantané
  lors de la navigation entre les pages.
- Gère les erreurs `FileNotFoundError` pour que l'application ne
  plante pas si un fichier de données est manquant.

Contient les chargeurs pour :
- Données Netflix (brutes et nettoyées)
- Données World Happiness Report (fichiers annuels bruts et version harmonisée)
"""

import pandas as pd
import streamlit as st
import sys

# ===================================================================================
# Netflix section 1
@st.cache_data 
def load_netflix_data_cleaning():
    """
    Charge et met en cache le dataset **brut** de Netflix (`netflix_titles.csv`).

    Cette fonction est spécifiquement utilisée par la page
    "2_🔎_Partie 1 - Analyse Exploratoire" pour montrer
    le processus de nettoyage à partir des données originales.

    Gère les erreurs `FileNotFoundError` si le fichier est manquant.

    Returns:
        pd.DataFrame | None : Le DataFrame brut, ou None si le chargement échoue.
    """

    file_path = './data/netflix_titles.csv'
    try : 
        netflix = pd.read_csv(file_path) 
        return netflix
    except FileNotFoundError :
        st.error(f"ERREUR CRITIQUE: Le fichier {file_path} est manquant.")
        st.error("L'application ne peut pas charger la partie Netflix.")
        return None
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue en chargeant {file_path}: {e}")
        return None

# Netflix section 2
@st.cache_data 
def load_netflix_data_analysis():
    """
    Charge et met en cache le dataset **nettoyé** de Netflix (`netflix_cleaned.csv`).

    Cette fonction est le chargeur principal pour toutes les pages qui
    nécessitent les données Netflix prêtes à l'analyse, notamment :
    - La page "3_📈_Visualisation Seaborn".
    - Le Dashboard interactif ("6_📝_Dashboard").

    Gère les erreurs `FileNotFoundError` si le fichier est manquant.

    Returns:
        pd.DataFrame | None: Le DataFrame **nettoyé**, ou None si le chargement échoue.

    """

    file_path = './data/netflix_cleaned.csv'
    try : 
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError :
        st.error(f"ERREUR CRITIQUE: Le fichier {file_path} est manquant.")
        st.error("L'application ne peut pas charger le fichier 'netflix_cleaned.csv'.")
        return None
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue en chargeant {file_path}: {e}")
        return None

# ===================================================================================
# Mise en cache de tous les datasets world happiness report 2015 - 2019
@st.cache_data
def load_happiness_all_df():
    """
    Charge et met en cache les 5 datasets **bruts** (2015-2019) du World Happiness Report.

    Cette fonction est spécifiquement utilisée par la page
    "4_♻️_Partie 2 - Harmonisation des datasets" pour lui fournir
    les 5 DataFrames originaux nécessaires au processus d'ETL (harmonisation).

    Gère les erreurs `FileNotFoundError` si un des fichiers est manquant.

    Returns:
        tuple | None:
            - Un tuple de 5 DataFrames (df_2015, ..., df_2019) si le chargement réussit.
            - None si un fichier est manquant ou si une erreur survient.
    """
        
    try :
        df_2015 = pd.read_csv('./data/2015.csv')
        df_2016 = pd.read_csv('./data/2016.csv')
        df_2017 = pd.read_csv('./data/2017.csv')
        df_2018 = pd.read_csv('./data/2018.csv')
        df_2019 = pd.read_csv('./data/2019.csv')
        return df_2015, df_2016, df_2017, df_2018, df_2019
    except FileNotFoundError :
        st.error("ERREUR : Un ou plusieurs fichiers CSV (2015-2019) sont manquants dans le dossier '/data'.")
        st.error("L'application ne peut pas charger la partie World Happiness Report")
        return None
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue en chargeant les fichiers : {e}")
        return None

# World Happiness section 2
@st.cache_data
def load_happiness_data_analysis():
    """
    Charge et met en cache le dataset **harmonisé** du World Happiness Report.

    Cette fonction charge le fichier CSV final (`world_happiness_2015-2019_combined.csv`)
    qui contient les données des 5 années, nettoyées et fusionnées.

    Elle est utilisée par les pages suivantes :
    - "5_📊_Partie 2 - Visualisation avec Plotly"
    - "6_📝_Dashboard"

    Gère les erreurs `FileNotFoundError` si le fichier est manquant.

    Returns:
        pd.DataFrame | None:
            - Le DataFrame **harmonisé**, prêt pour l'analyse.
            - None si le chargement échoue.
    """

    file_path = './data/world_happiness_2015-2019_combined.csv'
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"ERREUR CRITIQUE : Le fichier {file_path} est manquant.")
        st.error("Assurez-vous d'avoir exécuté la page d'harmonisation (4_♻️) au moins une fois.")
        return None
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue en chargeant {file_path}: {e}")
        return None