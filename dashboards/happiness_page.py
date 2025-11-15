"""
Module de Rendu pour le Dashboard "World Happiness Report".

Ce script n'est pas une page autonome, mais un module. Il contient
la fonction principale `render_happiness_dashboard()` qui est
appelée par le routeur principal (`6_📝_Dashboard.py`) lorsque
l'utilisateur sélectionne ce dataset.

Son rôle est de :
1.  Construire l'intégralité de l'interface du dashboard Happiness.
2.  Afficher les filtres de la barre latérale (sidebar)
    spécifiques à ce dataset (ex: sliders, multiselects).
3.  Calculer et afficher les KPIs (Indicateurs Clés).
4.  Créer et afficher tous les graphiques interactifs Plotly
    (Choropleth, Scatter, Line, Bar Race).
"""

# Importation des dépendances
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.chart_styles import get_happiness_layout
from utils.pandas_helpers import get_extremes_by_year

def render_happiness_dashboard(world_happiness_df):
    st.header("Dashboard World Happiness Report")
    st.markdown("""
    Cette section propose une exploration **interactive** des facteurs du bonheur mondial, en utilisant la bibliothèque **Plotly Express**.  
    L'objectif est d'utiliser des visualisations dynamiques pour explorer les données.  
    **Passez votre souris** sur les graphiques pour afficher les détails, **zoomez** sur les cartes, et **regardez les animations** (bar chart race) pour comprendre les tendances.
    """)
    st.divider()

    # ===========================================================
    # DÉFINITION DE LA CHARTE GRAPHIQUE
    # ===========================================================
    CONTINUOUS_PALETTE, CATEGORICAL_PALETTE, GLOBAL_TEMPLATE_LAYOUT = get_happiness_layout()

    # ===========================================================
    # FILTRE GLOBAL
    # ===========================================================
    st.sidebar.header("Filtres Globaux")

    # Filtre unique pour contrôler les KPIs, la Carte et le Nuage de points.
    all_years = world_happiness_df["Year"].unique()
    all_years.sort() 
    selected_year = st.sidebar.slider(
        "Sélectionnez une année",
        min_value=int(all_years.min()),
        max_value=int(all_years.max()),
        value=int(all_years.max())
    )

    # Filtrage du DataFrame basé sur le filtre unifié
    df_filtered_year = world_happiness_df[world_happiness_df['Year'] == selected_year]

    # ===========================================================
    # Les KPI
    # ===========================================================
    st.subheader(f"Indicateurs Clés pour {selected_year}")
    
    avg_score = round(df_filtered_year['Score'].mean(), 2)
    avg_gdp = round(df_filtered_year['GDP_per_Capita'].mean(), 2)
    avg_health = round(df_filtered_year['Health_Life_Expectancy'].mean(), 2)
    country_count = df_filtered_year['Country'].nunique()

    # Affichage avec st.columns
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, border=True)
    kpi_col1.metric("Score de Bonheur (Moy.)", avg_score)
    kpi_col2.metric("PIB par Hab. (Moy.)", avg_gdp)
    kpi_col3.metric("Espérance de Vie (Moy.)", avg_health)
    kpi_col4.metric("Nombre de Pays", country_count)
    st.divider()

    # ===================================================================================
    # Graphe 1 : Carte mondiale
    # ===================================================================================
    st.subheader("Analyse Géographique")
    
    st.sidebar.subheader("Filtres de la Carte")
    map_list = ["Score", "GDP_per_Capita", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable_map = st.sidebar.selectbox("Choisissez une variable pour la carte", map_list)

    # Échelle (range_color) calculée sur le DF COMPLET
    global_min_val = world_happiness_df[select_box_variable_map].min()
    global_max_val = world_happiness_df[select_box_variable_map].max()

    fig_map = px.choropleth(
        df_filtered_year, 
        locations='Country',
        locationmode='country names', 
        color=select_box_variable_map, 
        hover_name='Country',
        hover_data={'Region': True, 'Rank': True, 'GDP_per_Capita': ':.2f', 'Year': True, 'Country': False},
        color_continuous_scale=CONTINUOUS_PALETTE,
        range_color = [global_min_val, global_max_val], 
        title=f'Carte : {select_box_variable_map} en {selected_year}'
    )
    fig_map.update_layout(GLOBAL_TEMPLATE_LAYOUT)
    fig_map.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='natural earth'))
    
    # Affichage
    st.plotly_chart(fig_map, use_container_width=True)
    
    with st.expander("🔍 Lire l'analyse de la carte"):
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
    st.divider()

    # ===================================================================================
    # Graphe 2 : Nuage de points
    # ===================================================================================
    st.subheader("Analyse des Facteurs : Bonheur vs PIB")

    # Échelle calculée sur le DF COMPLET
    global_min_gdp = world_happiness_df['GDP_per_Capita'].min() * 0.9
    global_max_gdp = world_happiness_df['GDP_per_Capita'].max() * 1.05
    global_min_score = world_happiness_df['Score'].min() * 0.9
    global_max_score = world_happiness_df['Score'].max() * 1.05

    fig_scatter = px.scatter(
        df_filtered_year,
        x='GDP_per_Capita',
        y='Score',
        color="Region", 
        size='Social_Support', 
        hover_name='Country', 
        range_x = [global_min_gdp, global_max_gdp],
        range_y = [global_min_score, global_max_score],
        title = f'Bonheur vs. PIB en {selected_year}',
        labels = {'GDP_per_Capita': 'PIB par Habitant', 'Score': 'Score de Bonheur'}
    )
    fig_scatter.update_layout(GLOBAL_TEMPLATE_LAYOUT)
    fig_scatter.update_layout(title_x=0.5, title_y=0.95, title_yanchor='top')

    st.plotly_chart(fig_scatter, use_container_width=True)
    with st.expander("🔍 Lire l'analyse du nuage de points"):
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
    st.divider()

    # ===================================================================================
    # Graphe 3 : Line
    # ===================================================================================
    st.subheader("Analyse Temporelle (Comparaison de Pays)")
    
    st.sidebar.subheader("Filtres de la Courbe")
    map_list_line = ["Score", "GDP_per_Capita", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable_line = st.sidebar.selectbox("Choisissez une variable", map_list_line, key="Line")
    
    all_countries = world_happiness_df['Country'].unique()
    all_countries.sort()
    selected_countries = st.sidebar.multiselect(
        "Sélectionnez des pays à comparer",
        options=all_countries,
        default=["France", "Germany", "United States", "Japan", "India"], max_selections=10
    )

    if not selected_countries:
        st.warning("Veuillez sélectionner au moins un pays dans la barre latérale pour afficher le graphique.")
    else:
        df_line_filtered = world_happiness_df[world_happiness_df['Country'].isin(selected_countries)]
        fig_line = px.line(
            df_line_filtered, 
            x='Year', 
            y=select_box_variable_line, 
            color='Country', 
            markers=True, 
            hover_name='Country',
            title=f'Évolution de : {select_box_variable_line} (2015-2019)',
            labels={'Year': 'Année'}
        )
        fig_line.update_layout(GLOBAL_TEMPLATE_LAYOUT)
        fig_line.update_layout(title_x=0.5, title_y=0.9, title_yanchor='top')
        st.plotly_chart(fig_line, use_container_width=True)
    
    with st.expander("🔍 Lire l'analyse de la courbe"):
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
        * **Cas Particuliers :** C'est l'outil parfait pour repérer des anomalies. Y a-t-il un pays dont le score de "Confiance dans le Gouvernement" (`Trust_Government_Corruption`) chute soudainement une année ?""")
    st.divider()

    # ===================================================================================
    # Graphe 4 : Heatmap
    # ===================================================================================
    st.subheader("Analyse des Corrélations (toutes années confondues)")
    
    @st.cache_data
    def get_corr_matrix(df):
        numeric_cols = ['Score', 'GDP_per_Capita', 'Social_Support', 'Health_Life_Expectancy', 'Freedom', 'Trust_Government_Corruption', 'Generosity']
        return df[numeric_cols].corr()

    corr_matrix = get_corr_matrix(world_happiness_df)

    fig_heatmap = px.imshow(
        img = corr_matrix, 
        x = corr_matrix.columns, 
        y = corr_matrix.index, 
        color_continuous_scale = 'RdBu', 
        color_continuous_midpoint = 0, 
        zmin = -1, zmax = 1, 
        text_auto = True, 
        aspect = "auto", 
        title = 'Matrice de Corrélation des Facteurs du Bonheur'
    )
    fig_heatmap.update_traces(texttemplate="%{z:.2f}")
    fig_heatmap.update_layout(GLOBAL_TEMPLATE_LAYOUT)
    fig_heatmap.update_layout(title_x=0.5, title_y=0.95, title_yanchor='top')

    st.plotly_chart(fig_heatmap, use_container_width=True)
    with st.expander("🔍 Lire l'analyse de la heatmap"):
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
    st.divider()

    # ===================================================================================
    # Graphe 5 : Top 10 et Flop 10 (Bar Chart Race)
    # ===================================================================================
    st.subheader("Top & Flop 10 (Bar Chart Race)")

    st.sidebar.subheader("Filtres Top & Flop")
    map_list_race = ["Score", "GDP_per_Capita", "Social_Support", "Health_Life_Expectancy", "Freedom", "Trust_Government_Corruption", "Generosity"]
    select_box_variable_race = st.sidebar.selectbox("Choisissez une variable", map_list_race, key="Race")

    # --- Préparation des données  ---
    top_10_final = get_extremes_by_year(world_happiness_df, select_box_variable_race, ascending=False)
    flop_10_final = get_extremes_by_year(world_happiness_df, select_box_variable_race, ascending=True)
    
    # --- Création des graphiques ---
    
    # Échelle Top 10
    max_top = top_10_final[select_box_variable_race].max() * 1.05
    min_top = top_10_final[select_box_variable_race].min() * 0.9 # Pour ne pas commencer à 0
    if min_top < 0: min_top = 0 # Sauf si les valeurs sont négatives

    fig_top = px.bar(
        top_10_final,
        x=select_box_variable_race, y='Country', orientation='h',
        animation_frame='Year', animation_group='Country',
        color='Region', hover_name='Country',
        range_x=[min_top, max_top],
        title=f'Top 10 : {select_box_variable_race} (2015-2019)',
        labels={'Country':'Pays'}
    )
    fig_top.update_layout(GLOBAL_TEMPLATE_LAYOUT, yaxis_categoryorder='total ascending')
    fig_top.update_layout(title_x=0.5, title_y=0.95, title_yanchor='top')

    # Échelle Flop 10
    max_flop = flop_10_final[select_box_variable_race].max() * 1.05
    min_flop = flop_10_final[select_box_variable_race].min() * 0.9
    if min_flop < 0: min_flop = 0

    fig_flop = px.bar(
        flop_10_final,
        x=select_box_variable_race, y='Country', orientation='h',
        animation_frame='Year', animation_group='Country',
        color='Region', hover_name='Country',
        range_x=[min_flop, max_flop],
        title=f'Flop 10 : {select_box_variable_race} (2015-2019)',
        labels={'Country':'Pays'}
    )
    fig_flop.update_layout(GLOBAL_TEMPLATE_LAYOUT, yaxis_categoryorder='total ascending')
    fig_flop.update_layout(title_x=0.5, title_y=0.95, title_yanchor='top')

    col_top_flop_1, col_top_flop_2 = st.columns(2, gap="medium")

    with col_top_flop_1:
        st.plotly_chart(fig_top, use_container_width=True)
        with st.expander("🔍 Lire l'analyse du Top 10"):
            st.markdown("""
            ### 📈 Analyse : Le "Bar Chart Race" du Top 10

            Ce graphique animé montre "la course" des 10 pays les plus performants pour la variable sélectionnée.

            **Comment l'utiliser ?**
            1.  **Sélecteur de Variable :** Choisissez ce pour quoi vous voulez voir la course (ex: "Score", "GDP_per_Capita").
            2.  **Animation :** Appuyez sur le bouton "Play" (▶) du slider temporel pour voir les pays changer de rang au fil des ans (2015-2019).

            **Quoi observer ? (Les "Patterns")**

            * **La Stabilité des "Élites" :** Le Top 10 est un **club très fermé**. Vous remarquerez que, quelle que soit la variable, ce sont presque toujours les mêmes pays qui s'échangent les places (Suisse, Danemark, Norvège, Finlande, etc.).
            * **La Domination Régionale :** Regardez les couleurs (`color='Region'`). Le Top 10 est presque exclusivement composé de **"Western Europe"**, **"North America"** et **"Australia and New Zealand"**.
            * **La "Race" :** Le `yaxis_categoryorder='total ascending'` (le code qui fait la "race") montre qu'il est très difficile d'entrer dans ce Top 10, et tout aussi difficile d'en sortir. C'est la visualisation d'une **stabilité structurelle** (économies solides, systèmes de santé robustes, confiance élevée).""")

    with col_top_flop_2:
        st.plotly_chart(fig_flop, use_container_width=True)
        with st.expander("🔍 Lire l'analyse du Flop 10"):
            st.markdown("""
            ### 📉 Analyse : Le "Bar Chart Race" du Flop 10

            Ce graphique animé est le miroir du précédent : il montre "la course" des 10 pays les **moins performants**.

            **Comment l'utiliser ?**
            Même chose que le Top 10. Sélectionnez une variable (ex: "Score" ou "Health_Life_Expectancy") et appuyez sur "Play".

            **Quoi observer ? (Les "Patterns")**

            * **La Concentration de la Difficulté :** Le constat est tragique et immédiat. Regardez les couleurs (`color='Region'`) : le Flop 10 est dominé de manière écrasante par une seule région, **"Sub-Saharan Africa"**.
            * **La "Trappe" :** Contrairement au Top 10, les barres sont toutes écrasées à gauche, montrant un "effet de plancher". Si vous choisissez "GDP_per_Capita", vous visualisez la **"trappe de pauvreté"** : les pays ont du mal à décoller.
            * **L'Impact des Conflits :** Selon la variable, vous verrez apparaître des pays d'autres régions, souvent en raison de conflits ou de crises graves (ex: Syrie, Afghanistan, Yémen, Venezuela) qui détruisent le `Social_Support` et la `Health_Life_Expectancy`.
            * **La "Volatilité" :** Le "Flop 10" est souvent plus volatile que le "Top 10", non pas à cause d'une amélioration, mais parce qu'un pays s'effondre encore plus vite qu'un autre.""")