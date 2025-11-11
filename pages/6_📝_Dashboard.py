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
st.sidebar.write("Dashboard 📝")

# Choix du dataset
list_dataset = ["Netflix", "World Happiness Report"]
dataframe = st.sidebar.selectbox("Choisissez un dataset", list_dataset)
st.sidebar.write("")

# Chargement des dataframes
netflix = load_netflix_data_analysis()
world_happiness_report = load_happiness_data_analysis()

# Routage avec les modules
if dataframe == "Netflix":
    render_netflix_dashboard(netflix)
else:
    render_happiness_dashboard(world_happiness_report)
