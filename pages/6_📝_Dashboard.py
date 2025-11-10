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
    layout="wide",
    initial_sidebar_state = "expanded"
)
    
st.title("Dashboard")
st.sidebar.write("Dashboard 📝")

# Choix du dataset
list_dataset = ["Netflix", "World Happiness Report"]
dataframe = st.sidebar.selectbox("Choisissez un dataset", list_dataset)
st.sidebar.write("")

# Chargement du dataframe netflix
from data_loader import load_netflix_data_analysis
netflix = load_netflix_data_analysis()

# Chargement du dataframe World Happiness Report
from data_loader import load_happiness_data_analysis
world_happiness_report = load_happiness_data_analysis()

# Netflix dataset ======================================================================================================
if dataframe == "Netflix" :

    # =============================================================================
    # --- CHARTE GRAPHIQUE ---

    # 1. Définir les couleurs
    # Palette de couleurs
    NETFLIX_RED = "#E50914"
    NETFLIX_BLACK = "#221f1f"
    LIGHT_GREY = "#B3B3B3"
    DARK_GREY = "#4D4D4D"

    # Palette pour les graphiques simples (ex: top 10)
    # Un dégradé de gris vers le rouge
    main_palette = sns.color_palette([LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED])

    # Palette pour les graphiques binaires (Movie vs TV Show)
    binary_palette = {
        "Movie": NETFLIX_RED,
        "TV Show": DARK_GREY
    }

    # Palette pour les heatmaps (de blanc vers rouge)
    heatmap_cmap = sns.light_palette(NETFLIX_RED, as_cmap=True)

    # 2. Définir le style global (Polices et Fond)
    sns.set_theme(
        style="whitegrid",  # Fond blanc avec des grilles légères
        font="Arial",       # Police propre et lisible (si installée, sinon "sans-serif")
        rc={
            # Police et couleur pour les titres
            "axes.titlecolor": NETFLIX_BLACK,
            "axes.titlesize": 18,
            "axes.titleweight": "bold",
            
            # Police et couleur pour les étiquettes (axes x/y)
            "axes.labelcolor": DARK_GREY,
            "axes.labelsize": 14,
            "axes.labelweight": "bold",
            
            # Police et couleur pour les "ticks" (valeurs sur les axes)
            "xtick.color": DARK_GREY,
            "ytick.color": DARK_GREY,
        }
    )
    # ===================================================================================
    # Netflix dataset ===================================================================

    st.subheader("Graphes Statiques")

    graph_stat_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)

    # Gaphe 1 : Diagramme ==================================
    fig, ax = plt.subplots()

    sns.countplot(
        netflix,
        x='type',
        palette=binary_palette,
        width=0.75,
        ax=ax
    )

    # Personnalisation
    ax.set_title('Distribution des Types de Contenu')
    ax.set_xlabel('Type de Contenu')
    ax.set_ylabel('Nombre total')

    # Ajout des étiquettes de valeur au-dessus des barres
    ax.bar_label(ax.containers[0], fontsize=12, color=DARK_GREY)
    ax.bar_label(ax.containers[1], fontsize=12, color=DARK_GREY)

    with graph_stat_col[0] :
        # Affichage du graphe
        st.pyplot(fig)

    # Graphe 2 : Heatmap ===================
    fig, ax = plt.subplots()

    numeric_cols = ['release_year', 'year_added', 'month_added', 'lag_time', 'duration_min', 'duration_seasons']
    corr_matrix = netflix[numeric_cols].corr()

    sns.heatmap(
        corr_matrix,
        annot=True,          
        fmt=".2f",           # Formatage à 2 décimales
        cmap=heatmap_cmap,   
        linewidths=0.5,      
        cbar_kws={           
            # Personnalisation de la barre de couleur
            "label": "Coefficient de Corrélation"
        })

    # Personnalisation
    ax.set_title('Matrice de Corrélation')

    # Faire pivoter les étiquettes pour la lisibilité
    plt.xticks(rotation=90) 
    plt.yticks(rotation=0)

    with graph_stat_col[1] :
        # Affichage du graphe
        st.pyplot(fig)

    # Graphe 3 : Boxplot ======================

    boxplot_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)
    # Graphique 1 : Durée des films
    fig1, ax1 = plt.subplots()
    sns.boxplot(
        data=netflix[netflix['type'] == 'Movie'],
        x='duration_min',
        color=NETFLIX_RED,
        ax=ax1)

    # Personnalisation 
    ax1.set_title('Distribution de la Durée des Films (en minutes)')
    ax1.set_xlabel('Durée (minutes)')
    plt.show()


    # Graphique 2 : Nombre de Saisons des Séries
    fig2, ax2 = plt.subplots()
    sns.boxplot(
        data=netflix[netflix['type'] == 'TV Show'].dropna(subset=['duration_seasons']),
        x='duration_seasons',
        color=DARK_GREY, # Couleur unique pour les séries
        ax=ax2)
    # Personnalisation 
    ax2.set_title('Distribution du Nombre de Saisons (Séries TV)')
    ax2.set_xlabel('Nombre de Saisons')

    with boxplot_col[0] :
        # Affichage graphe de la Durée des films
        st.pyplot(fig1)

    with boxplot_col[1] :
        # A ffichage graphe de la Durée des séries
        st.pyplot(fig2)


    st.write("")
    st.write("")
    st.divider()
    st.subheader("Gaphes intéractifs")

    interactif_graph_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)
    # Graphe 4 : Diagramme en barre ============================
    # Préparation des données (Top 10)
    st.sidebar.write("Top des poys producteurs")
    nb_top10_countries = st.sidebar.number_input("Modifiez le nombre de pays", min_value=5, value=10, max_value=15)
    top_10_countries = netflix['main_country'].value_counts().head(nb_top10_countries).reset_index()
    top_10_countries.columns = ['country', 'count']

    fig, ax = plt.subplots()
    sns.barplot(
        data=top_10_countries,
        x='count',
        y='country',
        color=NETFLIX_RED,  
        saturation=0.9,     
        ax=ax
    )

    # Personnalisation 
    ax.set_title('Top 10 des Pays Producteurs')
    ax.set_xlabel('Nombre de Titres')
    ax.set_ylabel('Pays')

    # Cacher les bordures
    sns.despine(left=True, bottom=True) 

    with interactif_graph_col[0] :
        # Affichage du graphique
        st.pyplot(fig)

    # Graphe 5 : Histogramme ==================================
    st.sidebar.write("")
    st.sidebar.write("Distribution des sorties / Ajouts des productions")
    hist_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)

    # Widget 1
    nb_bins = st.sidebar.slider("Faites varier le nombre de bins", min_value=1, value=20, max_value=100)
    # Widget 2
    list_year = ["release_year", "year_added"]
    year_selection = st.sidebar.selectbox("Choisissez la variable", list_year)

    fig, ax = plt.subplots()
    sns.histplot(
        data=netflix,
        x=year_selection,
        bins=nb_bins,               
        color=NETFLIX_RED,       
        kde=True,              
        line_kws={             
            # Personnalisation de la ligne KDE
            'color': DARK_GREY,
            'linewidth': 3}, 
        ax=ax)

    # Personnalisation
    ax.set_title('Distribution des Années de Sortie du Contenu')
    ax.set_xlabel('Année de Sortie')
    ax.set_ylabel('Fréquence')

    with interactif_graph_col[1] :
        # Affichage du graphe
        st.pyplot(fig)


# World Happiness Report dataset =======================================================================================
if dataframe == "World Happiness Report" : 
    # ===========================================================================================
    # DÉFINITION DE LA CHARTE GRAPHIQUE PLOTLY

    # 1. Palettes de couleurs
    CONTINUOUS_PALETTE = 'Viridis' # Pour les scores (PIB, Bonheur...)
    CATEGORICAL_PALETTE = 'Safe' # Pour les catégories (Régions...)

    # 2. Template de Layout
    GLOBAL_TEMPLATE_LAYOUT = dict(
        # Le thème de base (fond blanc, grilles légères)
        template='plotly_white', 
        
        # Définition des polices
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#333333" # Gris très foncé, plus doux que le noir
        ),
        
        # Titre principal
        title=dict(
            font=dict(size=20, weight="bold"),
            x=0.5, # Centrer le titre
            xanchor='center'
        ),
        
        # Axes X et Y
        xaxis=dict(
            title_font=dict(size=14, weight="bold"),
            tickfont=dict(size=12),
            gridcolor='#EAEAEA', # Grille très claire
            zerolinecolor='#DDDDDD' # Ligne du zéro
        ),
        yaxis=dict(
            title_font=dict(size=14, weight="bold"),
            tickfont=dict(size=12),
            gridcolor='#EAEAEA',
        ),
        
        # Légende (pour les catégories)
        legend=dict(
            orientation='h', # Légende horizontale
            yanchor='bottom',
            y=1.02, # Placée juste au-dessus du graphique
            xanchor='right',
            x=1,
            title_text='' # Cacher le titre de la légende (souvent redondant)
        ),
        
        # Interactivité (la partie la plus importante)
        hovermode='closest', # Montre l'infobulle de l'élément le plus proche
        
        # Style de l'infobulle (hover)
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )

    # ===================================================================================
    # World Happiness Report Graphes =====================================================

    # Graphe 1 : Carte mondiale

    # Widget 1 ==================================
    st.sidebar.subheader("Carte mondiale")
    st.sidebar.write("Filtre Année")
    all_years_1 = world_happiness_report['Year'].unique()
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
    world_happiness_report_grahe1_filtred = world_happiness_report[world_happiness_report["Year"] == selected_year_1]
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
    all_years_2 = world_happiness_report['Year'].unique()
    # Trie des années
    all_years_2.sort() 

    selected_year_2 = st.sidebar.slider(
        "Sélectionnez une année",
        min_value=int(all_years_2.min()),
        max_value=int(all_years_2.max()),
        value=int(all_years_2.max()), key="Nuage des points")
    
    
    # Filtrage du dataframe
    world_happiness_report_grahe2_filtred = world_happiness_report[world_happiness_report["Year"] == selected_year_2]

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
    all_countries = world_happiness_report['Country'].unique()
    all_countries.sort()

    selected_countries = st.sidebar.multiselect(
        "Sélectionnez des pays à comparer",
        options=all_countries,
        default=["France", "Germany", "United States", "Japan", "India"], max_selections=10)

    # Filtrage du DataFrame pour les pays sélectionnés
    df_filtered = world_happiness_report[world_happiness_report['Country'].isin(selected_countries)]


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
    corr_matrix = world_happiness_report[numeric_cols].corr()

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
    top_10_2015 = world_happiness_report[world_happiness_report['Year']==2015].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2015)

    # top des pays par PIB 2016
    top_10_2016 = world_happiness_report[world_happiness_report['Year']==2016].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2016)

    # top des pays par PIB 2017
    top_10_2017 = world_happiness_report[world_happiness_report['Year']==2017].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2017)

    # top des pays par PIB 2018
    top_10_2018 = world_happiness_report[world_happiness_report['Year']==2018].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2018)

    # top des pays par PIB 2019
    top_10_2019 = world_happiness_report[world_happiness_report['Year']==2019].sort_values("GDP_per_Capita", ascending=False).head(10)
    top_to_concat.append(top_10_2019)

    # dataframe final Top 10 
    top_10_final = pd.concat(top_to_concat, ignore_index=True)

    # Liste de nos dataframes a concatener (flop 10) ===============================================================
    # Preparation des données
    flop_to_concat = []

    # flop des pays par PIB 2015
    flop_10_2015 = world_happiness_report[world_happiness_report['Year']==2015].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2015)

    # flop des pays par PIB 2016
    flop_10_2016 = world_happiness_report[world_happiness_report['Year']==2016].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2016)

    # flop des pays par PIB 2017
    flop_10_2017 = world_happiness_report[world_happiness_report['Year']==2017].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2017)

    # flop des pays par PIB 2018
    flop_10_2018 = world_happiness_report[world_happiness_report['Year']==2018].sort_values("GDP_per_Capita", ascending=True).head(10)
    flop_to_concat.append(flop_10_2018)

    # flop des pays par PIB 2019
    flop_10_2019 = world_happiness_report[world_happiness_report['Year']==2019].sort_values("GDP_per_Capita", ascending=True).head(10)
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
