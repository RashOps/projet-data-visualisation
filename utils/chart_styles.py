"""
Module de Centralisation des Chartes Graphiques (DRY).

Ce module a pour objectif de centraliser toute la configuration
stylistique des graphiques, en respectant le principe DRY
(Don't Repeat Yourself), afin de garantir une identité visuelle
cohérente à travers toute l'application.

Il fournit des fonctions "setup" distinctes pour :

1.  **Netflix (Seaborn) :**
    - `setup_netflix_theme()`: Applique le `sns.set_theme()` global
      et retourne les palettes de couleurs (NETFLIX_RED, binary_palette, etc.).
    - L'utilisation de `@st.cache_resource` garantit que ce
      thème n'est appliqué qu'une seule fois.

2.  **World Happiness (Plotly) :**
    - `get_happiness_layout()`: Retourne le dictionnaire de
      template global (`GLOBAL_TEMPLATE_LAYOUT`) pour tous
      les graphiques Plotly.
"""

import seaborn as sns
import streamlit as st
import plotly.express as px

# Charte graphique Netflix
@st.cache_resource
def setup_netflix_theme():
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

    return main_palette, binary_palette, heatmap_cmap, LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED


# Charte graphique World Happiness Report
def get_happiness_layout() :
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

    return CONTINUOUS_PALETTE, CATEGORICAL_PALETTE, GLOBAL_TEMPLATE_LAYOUT