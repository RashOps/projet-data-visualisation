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
    """
    Applique le thème Seaborn global pour Netflix et met en cache les ressources.
    
    Cette fonction exécute `sns.set_theme()` (une opération de setup)
    et la met en cache avec @st.cache_resource pour n'être exécutée
    qu'une seule fois.

    Elle retourne les palettes et couleurs nécessaires pour les pages :
    - `dashboards/netflix_page.py`
    - `pages/3_📈_Partie 1 - Les graphiques Seaborn.py`

    Returns:
        tuple: Un tuple contenant les palettes et couleurs principales
               (main_palette, binary_palette, heatmap_cmap, ...)
    """
    # =============================================================================
    # --- CHARTE GRAPHIQUE ---

    # 1. Définir les couleurs
    # Palette de couleurs
    NETFLIX_RED = "#E50914"
    NETFLIX_BLACK = "#221f1f"
    LIGHT_GREY = "#B3B3B3"
    DARK_GREY = "#4D4D4D"

    # Palette pour les graphiques simples 
    # Un dégradé de gris vers le rouge
    main_palette = sns.color_palette([LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED])

    # Palette pour les graphiques binaires (Movie vs TV Show)
    binary_palette = {
        "Movie": NETFLIX_RED,
        "TV Show": DARK_GREY
    }

    # Palette pour les heatmaps (de blanc vers rouge)
    heatmap_cmap = sns.light_palette(NETFLIX_RED, as_cmap=True)

    # 2. Définir le style global
    sns.set_theme(
        style="whitegrid",  
        font="Arial",       
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
    """
    Définit et retourne la charte graphique pour Plotly.
    
    Cette fonction ne nécessite pas de cache car elle ne fait que
    définir un dictionnaire, ce qui est une opération instantanée.

    Elle retourne les palettes et le template layout nécessaires pour les pages :
    - `dashboards/happiness_page.py`
    - `pages/5_📊_Partie 2 - Visualisation avec Plotly.py`
    
    Returns:
        tuple: Un tuple contenant les palettes et le template
               (CONTINUOUS_PALETTE, CATEGORICAL_PALETTE, GLOBAL_TEMPLATE_LAYOUT)
    """
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
        
        # Légende
        legend=dict(
            orientation='h', # Légende horizontale
            yanchor='bottom',
            y=1.02, # Placée juste au-dessus du graphique
            xanchor='right',
            x=1,
            title_text='' # Cacher le titre de la légende
        ),
        
        # Interactivité
        hovermode='closest', # Montre l'infobulle de l'élément le plus proche
        
        # Style de l'infobulle
        hoverlabel=dict(
            bgcolor="black", # Fond noir pour l'infobulle
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )

    return CONTINUOUS_PALETTE, CATEGORICAL_PALETTE, GLOBAL_TEMPLATE_LAYOUT