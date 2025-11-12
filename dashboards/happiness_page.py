# Imporation des dépendances
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import  seaborn as sns
import plotly.express as px
from utils.chart_styles import get_happiness_layout

def render_happiness_dashboard(world_happiness_df) :
    st.header("Dashboard World Happiness Report")
    st.markdown("""
    Cette section propose une exploration **interactive** des facteurs du bonheur mondial, en utilisant la bibliothèque **Plotly Express**.  
    L'objectif est d'utiliser des visualisations dynamiques pour explorer les données.  
    **Passez votre souris** sur les graphiques pour afficher les détails, **zoomez** sur les cartes, et **regardez les animations** (bar chart race) pour comprendre les tendances.
    """)

    # ===========================================================
    # Les KPI
    st.divider()
    st.sidebar.subheader("Explorez les KPIs")

    list_year_kpi = world_happiness_df["Year"].unique()

    selected_type = st.sidebar.selectbox("Années", list_year_kpi)
    if selected_type == 2015 or selected_type == 2016 or selected_type == 2017 or selected_type == 2018 or selected_type == 2019 :
        df_filtered = world_happiness_df[world_happiness_df['Year'] == selected_type]

    # Section KPIs
    st.subheader("Indicateurs Clés")
    avg_score = round(df_filtered['Score'].mean(), 2)
    avg_gdp = round(df_filtered['GDP_per_Capita'].mean(), 2)
    avg_health = round(df_filtered['Health_Life_Expectancy'].mean(), 2)
    country_count = df_filtered['Country'].nunique()

    # Affichage avec st.columns
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, border=True)

    with kpi_col1 : 
        st.metric("Score de Bonheur (Moy.)", avg_score)
    with kpi_col2: 
        st.metric("PIB par Hab. (Moy.)", avg_gdp)
    with kpi_col3 : 
        st.metric("Espérance de Vie (Moy.)", avg_health)
    with kpi_col4 : 
        st.metric("Nombre de Pays", country_count)

    st.divider()

    # ===========================================================================================
    # DÉFINITION DE LA CHARTE GRAPHIQUE PLOTLY
    CONTINUOUS_PALETTE, CATEGORICAL_PALETTE, GLOBAL_TEMPLATE_LAYOUT = get_happiness_layout()

    # ===================================================================================
    # World Happiness Report Graphes =====================================================

    # Graphe 1 : Carte mondiale
    # Widget 1 ==================================
    st.sidebar.subheader("Carte mondiale")
    st.sidebar.write("Filtre Année")
    all_years_1 = world_happiness_df['Year'].unique()
    # Trie des années
    all_years_1.sort() 

    selected_year_1 = st.sidebar.slider(
        "Sélectionnez une année",
        min_value=int(all_years_1.min()),
        max_value=int(all_years_1.max()),
        value=int(all_years_1.max()), key="Carte mondiale")
    
    # Widget 2 =========
    map_list = ["Score", "GDP_per_Capita", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable = st.sidebar.selectbox("Choisissez une variable", map_list)

    st.subheader("Graphes Intéractifs")

    # Echelle de coloration
    world_happiness_report_grahe1_filtred = world_happiness_df[world_happiness_df["Year"] == selected_year_1]
    global_min_score = world_happiness_report_grahe1_filtred[select_box_variable].min() # Valeur min
    global_max_score = world_happiness_report_grahe1_filtred[select_box_variable].max() # Valeur max
    st.write(f"Échelle de score globale fixée de {global_min_score:.2f} à {global_max_score:.2f}")

    fig = px.choropleth(
        world_happiness_report_grahe1_filtred,
        locations='Country',
        locationmode='country names', 

        color=select_box_variable, 

        # Bases de l'animation
        animation_frame='Year', 
        animation_group='Country', 

        # Valeurs hoover
        hover_name='Country',
        hover_data={
            'Region': True,
            'Rank': True,
            'GDP_per_Capita': ':.2f',
            'Year': True,
            'Country': False},

        color_continuous_scale=CONTINUOUS_PALETTE,

        # Application de l'echelle
        range_color = [global_min_score, global_max_score],

        title=f'Carte mondiale de la variable {select_box_variable} en {selected_year_1}'
    )

    # Application de notre template
    fig.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    # Personnalisation de la carte
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth'
        )
    )
    st.plotly_chart(fig, selection_mode="points")


    st.write("")
    st.write("")
    st.write("")
    st.divider()
    # Graphe 2 : Nuage des points ===============================
    # Echelle de coloration des bornes globales des axes X et Y
    st.sidebar.write("")
    st.sidebar.subheader("Nuage des points")

    # Widget 1
    all_years_2 = world_happiness_df['Year'].unique()
    # Trie des années
    all_years_2.sort() 

    selected_year_2 = st.sidebar.slider(
        "Sélectionnez une année",
        min_value=int(all_years_2.min()),
        max_value=int(all_years_2.max()),
        value=int(all_years_2.max()), key="Nuage des points")
    
    
    # Filtrage du dataframe
    world_happiness_report_grahe2_filtred = world_happiness_df[world_happiness_df["Year"] == selected_year_2]

    global_min_gdp = world_happiness_report_grahe2_filtred['GDP_per_Capita'].min() * 0.9
    global_max_gdp = world_happiness_report_grahe2_filtred['GDP_per_Capita'].max() * 1.05

    global_min_score = world_happiness_report_grahe2_filtred['Score'].min() * 0.9
    global_max_score = world_happiness_report_grahe2_filtred['Score'].max() * 1.05

    st.write(f"Axe X (PIB) fixé de {global_min_gdp:.2f} à {global_max_gdp:.2f}")
    st.write(f"Axe Y (Score) fixé de {global_min_score:.2f} à {global_max_score:.2f}")

    fig = px.scatter(
        world_happiness_report_grahe2_filtred,

        x='GDP_per_Capita',
        y='Score',

        color="Region", 
        size='Social_Support', 

        hover_name='Country',

        # Les bases de l'animation
        animation_frame = 'Year',       
        animation_group = 'Country',     
        
        # Application de l'échelle
        range_x = [global_min_gdp, global_max_gdp],
        range_y = [global_min_score, global_max_score],
                                            
        title = 'Évolution du Bonheur vs. PIB (2015-2019)',
        labels = { 
            'GDP_per_Capita': 'PIB par Habitant',
            'Score': 'Score de Bonheur'}
    )

    # Application de notre template
    fig.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    fig.update_layout(
        title_x=0.5,        
        title_y=0.05,     
        title_yanchor='top'  
    )

    st.plotly_chart(fig)


    st.write("")
    st.write("")
    st.write("")
    st.divider()
    # Graphe 3 : Line =============================
    st.sidebar.write("")
    st.sidebar.subheader("Line")
    # Widget 1
    map_list_1 = ["GDP_per_Capita", "Score", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable_1 = st.sidebar.selectbox("Choisissez une variable", map_list_1, key="Line")
    
    # Widget 2
    all_countries = world_happiness_df['Country'].unique()
    all_countries.sort()

    selected_countries = st.sidebar.multiselect(
        "Sélectionnez des pays à comparer",
        options=all_countries,
        default=["France", "Germany", "United States", "Japan", "India"], max_selections=10)

    # Filtrage du DataFrame pour les pays sélectionnés
    df_filtered = world_happiness_df[world_happiness_df['Country'].isin(selected_countries)]


    # Création du graphique 
    fig = px.line(
        df_filtered,  
        
        x='Year',           
        y=select_box_variable_1, 
        
        color='Country',    
        markers=True,       
        
        hover_name='Country',
        title=f'Courbe de la variable {select_box_variable_1} (2015-2019)',
        labels={
            'Year': 'Année'
        }
    )

    # Application de notre template
    fig.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    fig.update_layout(
        title_x=0.5,
        title_y=0.9,
        title_yanchor='top'
    )

    # Affichage du graphe
    st.plotly_chart(fig)




    st.write("")
    st.write("")
    st.write("")
    st.divider()
    # Graphe 4 : Heatmap =============================
    # Préparation les données : Création de la matrice de corrélation
    numeric_cols = ['Score', 'GDP_per_Capita', 'Social_Support', 'Health_Life_Expectancy', 'Freedom', 'Trust_Government_Corruption', 'Generosity']
    corr_matrix = world_happiness_df[numeric_cols].corr()

    # Création la heatmap interactive
    fig = px.imshow(
        img = corr_matrix,                     
        
        x = corr_matrix.columns,             
        y = corr_matrix.index,               
        
        color_continuous_scale = 'RdBu',       
        color_continuous_midpoint = 0,         
        zmin = -1, zmax = 1,                
        
        text_auto = True,                 
        aspect = "auto",                     
        
        title = 'Matrice de Corrélation Interactive'
    )

    # Formatage du texte pour n'avoir que 2 décimales
    fig.update_traces(texttemplate="%{z:.2f}")

    # Application de notre template
    fig.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    fig.update_layout(
        title_x=0.5,        # Recentrage du titre
        title_y=0.95,       # Positionne le titre verticalement (5% du bas)
        title_yanchor='top'   # Ancrage du titre à cette position
    )

    # Affichage du graphe
    st.plotly_chart(fig)



    st.write("")
    st.write("")
    st.write("")
    st.divider()
    # Graphe : Top 10 et Flop 10 =============================

    st.write("")
    st.subheader("Top & Flop")

    # Widget 1 
    st.sidebar.write("")
    st.sidebar.subheader("Top & Flop")
    map_list_2 = ["GDP_per_Capita", "Score", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable_2_top = st.sidebar.selectbox("Choisissez une variable", map_list_2, key="Top")
    select_box_variable_2_flop = st.sidebar.selectbox("Choisissez une variable", map_list_2, key="Flop")


    # Liste de nos dataframes a concatener (top 10) ===============================================================
    # Preparation des données
    top_to_concat = []

    # top des pays par PIB 2015
    top_10_2015 = world_happiness_df[world_happiness_df['Year']==2015].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2015)

    # top des pays par PIB 2016
    top_10_2016 = world_happiness_df[world_happiness_df['Year']==2016].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2016)

    # top des pays par PIB 2017
    top_10_2017 = world_happiness_df[world_happiness_df['Year']==2017].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2017)

    # top des pays par PIB 2018
    top_10_2018 = world_happiness_df[world_happiness_df['Year']==2018].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2018)

    # top des pays par PIB 2019
    top_10_2019 = world_happiness_df[world_happiness_df['Year']==2019].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2019)

    # dataframe final Top 10 
    top_10_final = pd.concat(top_to_concat, ignore_index=True)

    # Liste de nos dataframes a concatener (flop 10) ===============================================================
    # Preparation des données
    flop_to_concat = []

    # flop des pays par PIB 2015
    flop_10_2015 = world_happiness_df[world_happiness_df['Year']==2015].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2015)

    # flop des pays par PIB 2016
    flop_10_2016 = world_happiness_df[world_happiness_df['Year']==2016].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2016)

    # flop des pays par PIB 2017
    flop_10_2017 = world_happiness_df[world_happiness_df['Year']==2017].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2017)

    # flop des pays par PIB 2018
    flop_10_2018 = world_happiness_df[world_happiness_df['Year']==2018].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2018)

    # flop des pays par PIB 2019
    flop_10_2019 = world_happiness_df[world_happiness_df['Year']==2019].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2019)

    # dataframe final Flop 10
    flop_10_final = pd.concat(flop_to_concat, ignore_index=True)
    
    # Top 10 ================================================================
    # Echelle des valeurs pour l'axe des abscisses
    
    max_gdp = top_10_final[select_box_variable_2_top].max() * 1.05 # 5% de marge
    min_gdp = 0 # Les barres commencent à 0

    fig_top = px.bar(
        top_10_final,
        x=select_box_variable_2_top,
        y='Country',
        orientation='h',

        # Paramètres animations
        animation_frame='Year',
        animation_group='Country',

        color='Region',
        hover_name='Country',

        # Fixation de l'axe X
        range_x=[min_gdp, max_gdp],

        title=f'Top 10 des Pays selon la variable {select_box_variable_2_top} (2015-2019)',
        labels={'Country':'Pays'}
    )

    # Application de notre template
    fig_top.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    # Ajout du tri des barres (l'effet "Race")
    fig_top.update_layout(yaxis_categoryorder='total ascending')

    fig_top.update_layout(
        title_x=0.5,        
        title_y=0.95,       
        title_yanchor='top'  
    )

    # Flop 10 =========================================================================
    # Echelle des valeurs pour l'axe des abscisses
    max_gdp = flop_10_final[select_box_variable_2_flop].max() * 1.05 # 5% de marge
    min_gdp = 0 # Les barres commencent à 0

    fig_flop = px.bar(
        flop_10_final,
        x=select_box_variable_2_flop,
        y='Country',
        orientation='h',

        # Paramètres animations
        animation_frame='Year',
        animation_group='Country',

        color='Region',
        hover_name='Country',

        # Fixation de l'axe X
        range_x=[min_gdp, max_gdp],

        title=f'Flop 10 des Pays selon la variable {select_box_variable_2_flop} (2015-2019)',
        labels={'Country':'Pays'}
    )

    # Application de notre template
    fig_flop.update_layout(GLOBAL_TEMPLATE_LAYOUT)

    # Ajout du tri des barres (l'effet "Race")
    fig_flop.update_layout(yaxis_categoryorder='total ascending')

    fig_flop.update_layout(
        title_x=0.5,        
        title_y=0.95,       
        title_yanchor='top'  
    )

    col_top_flop = st.columns(2, gap="medium", vertical_alignment="center", width=1300)

    with col_top_flop[0] :
        # Affichage du graphe du Top 10 
        st.plotly_chart(fig_top)

    with col_top_flop[1] :
        # Affichage du graphe du Flop 10
        st.plotly_chart(fig_flop)