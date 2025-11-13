"""
Page du Dashboard Interactif (Routeur Principal).

Ce script est la page "Dashboard" principale. Il ne contient pas
de graphiques lui-même, mais agit comme un **routeur** central.

Son rôle est de :
1.  Charger les deux DataFrames principaux (Netflix, Happiness)
    via le `data_loader` (qui les met en cache).
2.  Afficher le `st.sidebar.selectbox` principal qui permet
    de choisir entre "Netflix" et "World Happiness Report".
3.  Utiliser une structure `if/else` pour appeler la fonction
    de rendu appropriée (`render_netflix_dashboard` ou
    `render_happiness_dashboard`).

Cette architecture modulaire (importer depuis `/dashboards`) permet
de garder ce fichier propre et de séparer la logique de chaque
dashboard, le rendant plus facile à maintenir et à déboguer.
"""

# Imporation des dépendances
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import  seaborn as sns
import plotly.express as px
from data_loader import load_netflix_data_analysis, load_happiness_data_analysis
from dashboards.netflix_page import render_netflix_dashboard
from dashboards.happiness_page import render_happiness_dashboard

# Configuration de la page principale
st.set_page_config(
    page_title="Dashboard",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state = "expanded"
)
    
st.title("Dashboard")
st.sidebar.subheader("Dashboard 📝")

# Choix du dataset
list_dataset = ["Netflix", "World Happiness Report"]
dataframe = st.sidebar.selectbox("Choisissez un dataset", list_dataset)
st.sidebar.write("")

# Chargement des dataframes
netflix = load_netflix_data_analysis()
if netflix is None:
    st.stop()

world_happiness_report = load_happiness_data_analysis()
if world_happiness_report is None:
    st.stop()

# Routage avec les modules
if dataframe == "Netflix":
    render_netflix_dashboard(netflix)
else:
    render_happiness_dashboard(world_happiness_report)
