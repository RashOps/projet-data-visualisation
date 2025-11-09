# Imporation des dépendances
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import  seaborn as sns
import plotly.express as px

# Configuration de la page principale
st.set_page_config(
    page_title="Dashboard",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state = "expanded"
)

# Netflix dataset ======================================================================================================
# Chargement du dataframe
from data_loader import load_netflix_data_analysis
netflix = load_netflix_data_analysis()



















# World Happiness Report dataset ======================================================================================================
# Chargement du dataframe
from data_loader import load_happiness_data_analysis
netflix = load_happiness_data_analysis()