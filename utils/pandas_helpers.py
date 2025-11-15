"""
Cette page regroupe et met en cache les fonctions utiles afin d'aléger le code des autres pages.
"""

import pandas as pd
import streamlit as st

@st.cache_data
def get_extremes_by_year(df, variable_col, ascending=False, n=10):
        """
        Groupe par 'Year', puis pour chaque année, trouve les N
        premiers/derniers pays pour la 'variable_col' sélectionnée.
        """
        return (df.groupby('Year')
                .apply(lambda x: x.sort_values(variable_col, ascending=ascending).head(n))
                .reset_index(drop=True)) 