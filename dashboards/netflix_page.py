# Imporation des dépendances
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import  seaborn as sns
import plotly.express as px

def render_netflix_dashboard(netflix_df):
    st.header("Dashboard Netflix")

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
        netflix_df,
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
    corr_matrix = netflix_df[numeric_cols].corr()

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
        data=netflix_df[netflix_df['type'] == 'Movie'],
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
        data=netflix_df[netflix_df['type'] == 'TV Show'].dropna(subset=['duration_seasons']),
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
    st.sidebar.write("")
    st.sidebar.subheader("Top des poys producteurs")
    nb_top10_countries = st.sidebar.number_input("Modifiez le nombre de pays", min_value=5, value=10, max_value=15)
    top_10_countries = netflix_df['main_country'].value_counts().head(nb_top10_countries).reset_index()
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
    ax.set_title(f'Top {nb_top10_countries} des Pays Producteurs')
    ax.set_xlabel('Nombre de Titres')
    ax.set_ylabel('Pays')

    # Cacher les bordures
    sns.despine(left=True, bottom=True) 

    with interactif_graph_col[0] :
        # Affichage du graphique
        st.pyplot(fig)

    # Graphe 5 : Histogramme ==================================
    st.sidebar.write("")
    st.sidebar.subheader("Distribution des sorties / Ajouts des productions")
    hist_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)

    # Widget 1
    nb_bins = st.sidebar.slider("Faites varier le nombre de bins", min_value=1, value=20, max_value=100)
    # Widget 2
    list_year = ["release_year", "year_added"]
    year_selection = st.sidebar.selectbox("Choisissez la variable", list_year)

    fig, ax = plt.subplots()
    sns.histplot(
        data=netflix_df,
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
    if year_selection == "release_year" :
        ax.set_title('Distribution des années de sortie du contenu')
        ax.set_xlabel('Année de sortie')
    else :
        ax.set_title("Distribution des Années d'ajout du contenu")
        ax.set_xlabel('Année d\'ajout')

    ax.set_ylabel('Fréquence')

    with interactif_graph_col[1] :
        # Affichage du graphe
        st.pyplot(fig)