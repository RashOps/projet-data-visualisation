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
    with st.expander("🔍 Lire l'analyse") :
        st.markdown("""
        ### 📈 Analyse : Carte Interactive (Choropleth)

        Cette carte mondiale est l'outil d'exploration principal de ce dashboard. Elle vous permet d'analyser la distribution géographique de n'importe quel facteur du bonheur.

        **Comment l'utiliser ?**

        1.  **Sélecteur de Variable :** Utilisez le `selectbox` "Choisissez une variable" dans la barre latérale pour changer la métrique affichée (ex: "Score" de bonheur, "GDP_per_Capita", "Health_Life_Expectancy").
        2.  **Sélecteur d'Année :** Utilisez le `slider` "Sélectionnez une année" pour figer la carte sur une année précise.
        3.  **Interactivité :** Passez votre souris sur un pays pour voir ses détails. Zoomez et déplacez-vous sur la carte pour explorer des régions spécifiques.

        **Quoi observer ? (Les "Patterns")**

        * **La Fracture Nord/Sud :** Quelle que soit la variable positive que vous choisissez (Bonheur, PIB, Santé), vous observerez une très nette **fracture géographique**. L'Europe de l'Ouest, l'Amérique du Nord et l'Océanie affichent systématiquement les scores les plus élevés.
        * **Les Clusters Régionaux :** Les pays ont tendance à "se regrouper" par région. L'Afrique Subsaharienne et l'Asie du Sud affichent souvent les scores les plus bas, tandis que l'Amérique Latine se situe dans la moyenne.
        * **Corrélation Richesse/Santé/Bonheur :** En basculant la variable entre "Score", "GDP_per_Capita" et "Health_Life_Expectancy", vous remarquerez que la carte change très peu. C'est la preuve visuelle que ces trois indicateurs sont **extrêmement corrélés**.

        *Note : Le code fixe l'échelle de couleur (`range_color`) en fonction de la sélection, garantissant que les comparaisons entre les années (en bougeant le slider) sont visuellement justes.*
    """)


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
    with st.expander("🔍 Lire l'analyse") :
        st.markdown("""
        ### 📈 Analyse : La Relation entre Richesse et Bonheur

        Ce nuage de points (bubble chart) est l'une des visualisations les plus importantes. Il explore la relation entre la **Richesse** d'un pays (Axe X : PIB par Habitant) et son **Bonheur** (Axe Y : Score).

        **Comment l'utiliser ?**

        * **Couleur :** Représente le "cluster" géographique (`Region`).
        * **Taille de la Bulle :** Représente l'importance du **Soutien Social** (`Social_Support`).
        * **Interactivité :** Passez votre souris sur une bulle pour voir le nom du pays et ses métriques.

        **1. Le Constat (Ce que le graphique montre)**

        On observe une **corrélation positive très nette** : les bulles forment un nuage qui monte de gauche à droite.

        **2. L'Analyse (Pourquoi ?)**

        * **"L'argent fait le bonheur" (en partie) :** Le constat est clair : en moyenne, **plus un pays est riche, plus son score de bonheur est élevé**. Le PIB par habitant est un prédicteur majeur du bien-être.
        * **Les Clusters Régionaux :** Les couleurs ne sont pas mélangées au hasard. On voit distinctement le "cluster" de l'Europe de l'Ouest (en haut à droite : riche et heureux) et celui de l'Afrique Subsaharienne (en bas à gauche : pauvre et moins heureux).
        * **L'argent ne fait pas tout (L'importance de la Taille) :** Regardez les pays qui ont un PIB *similaire* (sur la même ligne verticale). Certains ont de **grosses bulles** (fort soutien social) et sont plus heureux, tandis que d'autres ont de **petites bulles** (faible soutien social) et sont moins heureux.
        * **Conclusion :** Le bonheur repose sur un triptyque : **Richesse** (PIB), **Santé** (vu sur la heatmap) et **Communauté** (Soutien Social, la taille des bulles). Un pays riche avec des liens sociaux faibles sera moins heureux qu'un pays riche avec des liens sociaux forts.
        """)


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
    with st.expander("🔍 Lire l'analyse") :
        st.markdown("""
        ### 📈 Analyse : Évolution Temporelle (2015-2019)

        Ce graphique linéaire est conçu pour **comparer directement** l'évolution de plusieurs pays sur la métrique de votre choix.

        **Comment l'utiliser ?**

        1.  **Sélecteur de Variable :** Utilisez le `selectbox` "Choisissez une variable" pour définir l'axe Y (ex: "Score", "Freedom", "GDP_per_Capita").
        2.  **Sélecteur de Pays :** Utilisez le `multiselect` pour ajouter ou retirer les pays que vous souhaitez comparer (limité à 10 pour la lisibilité).
        3.  **Interactivité :** Passez votre souris sur les lignes ou les marqueurs pour voir les valeurs exactes pour une année et un pays donné.

        **Quoi observer ? (Les "Patterns")**

        * **Stabilité des Tendances :** Pour la plupart des pays, les indicateurs (bonheur, PIB, santé) sont **remarquablement stables**. Les lignes sont relativement plates. Cela montre que le bien-être d'un pays est une métrique "lourde" qui évolue lentement sur le long terme.
        * **Le Classement change peu :** Les hiérarchies sont bien établies. Si vous sélectionnez (par exemple) la Suisse, la France et l'Inde, vous verrez que leurs lignes restent largement parallèles sans jamais se croiser. Un pays "riche" reste "riche" et un pays "pauvre" reste "pauvre" sur cette courte période de 5 ans.
        * **Absence de Crise (sur cette période) :** Les données s'arrêtant en 2019, nous ne voyons pas l'impact d'événements mondiaux majeurs (comme le COVID-19 en 2020) qui auraient pu provoquer des chutes brutales.
        * **Cas Particuliers :** C'est l'outil parfait pour repérer des anomalies. Y a-t-il un pays dont le score de "Confiance dans le Gouvernement" (`Trust_Government_Corruption`) chute soudainement une année ?
        """)



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
    with st.expander("🔍 Lire l'analyse") :
        st.markdown("""
        ### 📈 Analyse : Quels facteurs sont les plus importants ?

        Cette matrice de corrélation interactive (`heatmap`) est l'une des visualisations les plus importantes du projet. Elle quantifie la **force de la relation** entre toutes les variables (de -1 à +1).

        **Comment la lire ?**
        * **Rouge Vif (+1) :** Corrélation positive forte (quand l'un augmente, l'autre aussi).
        * **Bleu Vif (-1) :** Corrélation négative forte (quand l'un augmente, l'autre diminue).
        * **Blanc/Gris (0) :** Aucune relation linéaire.

        **1. L'Enseignement Principal : Le Triptyque du Bonheur**

        Pour comprendre ce qui "fait" le bonheur, regardez la **première ligne (ou colonne) `Score`** :

        | Facteur | Corrélation (~) | Importance |
        |:---|:---|:---|
        | **`GDP_per_Capita`** | ~0.78 | 💰 **Richesse** |
        | **`Health_Life_Expectancy`** | ~0.76 | 🩺 **Santé** |
        | **`Social_Support`** | ~0.75 | 🤝 **Communauté** |

        L'analyse est sans appel : le bonheur d'un pays repose sur ce triptyque. La richesse, la santé et des liens sociaux forts sont les prédicteurs les plus puissants.

        **2. Les Facteurs Secondaires**

        * **`Freedom`** (~0.55) et **`Trust_Government_Corruption`** (~0.40) ont une importance **modérée**.
        * **`Generosity`** (~0.14) est le facteur le **moins influent**. La générosité d'une nation n'est pas (statistiquement) un moteur de son bonheur global.

        **3. Inter-Corrélations**

        Remarquez aussi que les facteurs du triptyque sont eux-mêmes corrélés (ex: `GDP_per_Capita` et `Health_Life_Expectancy` sont rouge vif). Cela montre un cercle vertueux : les pays riches ont tendance à avoir de meilleurs systèmes de santé, ce qui contribue au bonheur.
    """)


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

    @st.cache_data
    def get_extremes_by_year(df, variable_col, ascending=False, n=10):
        """
        Groupe par 'Year', puis pour chaque année, trouve les N
        premiers/derniers pays pour la 'variable_col' sélectionnée.
        """
        return (df.groupby('Year')
                .apply(lambda x: x.sort_values(variable_col, ascending=ascending).head(n))
                .reset_index(drop=True))
    
    # --- Appel de la fonction pour le Top 10 ---
    top_10_final = get_extremes_by_year(
        world_happiness_df,
        select_box_variable_2_top, # <-- Utilise la variable du widget
        ascending=False)
    
    # --- Appel de la fonction pour le Flop 10 ---
    flop_10_final = get_extremes_by_year(
        world_happiness_df,
        select_box_variable_2_flop, # <-- Utilise la variable du widget
        ascending=True)
    
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
        with st.expander("🔍 Lire l'analyse") :
            st.markdown("""
            ### 📈 Analyse : Le "Bar Chart Race" du Top 10

            Ce graphique animé montre "la course" des 10 pays les plus performants pour la variable sélectionnée.

            **Comment l'utiliser ?**
            1.  **Sélecteur de Variable :** Choisissez ce pour quoi vous voulez voir la course (ex: "Score", "GDP_per_Capita").
            2.  **Animation :** Appuyez sur le bouton "Play" (▶) du slider temporel pour voir les pays changer de rang au fil des ans (2015-2019).

            **Quoi observer ? (Les "Patterns")**

            * **La Stabilité des "Élites" :** Le Top 10 est un **club très fermé**. Vous remarquerez que, quelle que soit la variable, ce sont presque toujours les mêmes pays qui s'échangent les places (Suisse, Danemark, Norvège, Finlande, etc.).
            * **La Domination Régionale :** Regardez les couleurs (`color='Region'`). Le Top 10 est presque exclusivement composé de **"Western Europe"**, **"North America"** et **"Australia and New Zealand"**.
            * **La "Race" :** Le `yaxis_categoryorder='total ascending'` (le code qui fait la "race") montre qu'il est très difficile d'entrer dans ce Top 10, et tout aussi difficile d'en sortir. C'est la visualisation d'une **stabilité structurelle** (économies solides, systèmes de santé robustes, confiance élevée).
        """)

    with col_top_flop[1] :
        # Affichage du graphe du Flop 10
        st.plotly_chart(fig_flop)
        with st.expander("🔍 Lire l'analyse") :
            st.markdown("""
            ### 📉 Analyse : Le "Bar Chart Race" du Flop 10

            Ce graphique animé est le miroir du précédent : il montre "la course" des 10 pays les **moins performants**.

            **Comment l'utiliser ?**
            Même chose que le Top 10. Sélectionnez une variable (ex: "Score" ou "Health_Life_Expectancy") et appuyez sur "Play".

            **Quoi observer ? (Les "Patterns")**

            * **La Concentration de la Difficulté :** Le constat est tragique et immédiat. Regardez les couleurs (`color='Region'`) : le Flop 10 est dominé de manière écrasante par une seule région, **"Sub-Saharan Africa"**.
            * **La "Trappe" :** Contrairement au Top 10, les barres sont toutes écrasées à gauche, montrant un "effet de plancher". Si vous choisissez "GDP_per_Capita", vous visualisez la **"trappe de pauvreté"** : les pays ont du mal à décoller.
            * **L'Impact des Conflits :** Selon la variable, vous verrez apparaître des pays d'autres régions, souvent en raison de conflits ou de crises graves (ex: Syrie, Afghanistan, Yémen, Venezuela) qui détruisent le `Social_Support` et la `Health_Life_Expectancy`.
            * **La "Volatilité" :** Le "Flop 10" est souvent plus volatile que le "Top 10", non pas à cause d'une amélioration, mais parce qu'un pays s'effondre encore plus vite qu'un autre.
        """)