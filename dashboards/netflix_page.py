"""
Module de Rendu pour le Dashboard "Netflix".

Ce script n'est pas une page autonome, mais un module. Il contient
la fonction principale `render_netflix_dashboard()` qui est
appelée par le routeur principal (`6_📝_Dashboard.py`) lorsque
l'utilisateur sélectionne ce dataset.

Son rôle est de :
1.  Construire l'intégralité de l'interface du dashboard Netflix.
2.  Appliquer la charte graphique `Seaborn` (`setup_netflix_theme`).
3.  Afficher les filtres de la barre latérale (sidebar)
    spécifiques à ce dataset (ex: sliders, selectbox).
4.  Calculer et afficher les KPIs (Indicateurs Clés).
5.  Créer (et mettre en cache) tous les graphiques statiques `Seaborn`
    (countplot, barplot, heatmap, etc.).
"""

# Importation des dépendances
import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd 
from utils.chart_styles import setup_netflix_theme

# =============================================================================
# --- CHARTE GRAPHIQUE ---
main_palette, binary_palette, heatmap_cmap, LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED = setup_netflix_theme()

# ==========================================================
# FONCTIONS DE CRÉATION DE GRAPHIQUES (MISES EN CACHE)
# ==========================================================

@st.cache_data
def create_countplot_figure(data_df, palette, color):
    """Crée et retourne la figure Matplotlib pour le countplot."""
    fig, ax = plt.subplots()
    sns.countplot(
        data=data_df,
        x='type',
        palette=palette,
        width=0.75,
        ax=ax
    )
    # Personnalisation
    ax.set_title('Distribution des Types de Contenu')
    ax.set_xlabel('Type de Contenu')
    ax.set_ylabel('Nombre total')
    
    for container in ax.containers:
        ax.bar_label(container, fontsize=12, color=color)
    return fig

@st.cache_data
def create_heatmap_figure(data_df):
    """Crée et retourne la figure Matplotlib pour la heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_cols = ['release_year', 'year_added', 'month_added', 'lag_time', 'duration_min', 'duration_seasons']
    corr_matrix = data_df[numeric_cols].corr()
    sns.heatmap(
        corr_matrix,
        annot=True, 
        fmt=".2f",
        cmap=heatmap_cmap, 
        linewidths=0.5, 
        cbar_kws={"label": "Coefficient de Corrélation"},
        ax=ax
    )
    ax.set_title('Matrice de Corrélation')
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    return fig

@st.cache_data
def create_boxplot_movies(data_df, color):
    """Crée et retourne la figure boxplot pour les films."""
    fig1, ax1 = plt.subplots()
    sns.boxplot(
        data=data_df[data_df['type'] == 'Movie'],
        x='duration_min',
        color=color,
        ax=ax1)
    ax1.set_title('Distribution de la Durée des Films (en minutes)')
    ax1.set_xlabel('Durée (minutes)')
    return fig1

@st.cache_data
def create_boxplot_series(data_df, color) :
    """Crée et retourne la figure boxplot pour les séries."""
    fig2, ax2 = plt.subplots()
    sns.boxplot(
        data=data_df[data_df['type'] == 'TV Show'].dropna(subset=['duration_seasons']),
        x='duration_seasons',
        color=color,
        ax=ax2)
    ax2.set_title('Distribution du Nombre de Saisons (Séries TV)')
    ax2.set_xlabel('Nombre de Saisons')
    return fig2

@st.cache_data
def create_barplot_figure(data_df, num_top, color) :
    """
    Crée et retourne la figure barplot pour le Top N Pays.
    """
    top_data = data_df['main_country'].value_counts().head(num_top).reset_index()
    top_data.columns = ['country', 'count']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        data=top_data,
        x='count',
        y='country',
        color=color,  
        saturation=0.9,    
        ax=ax
    )
    ax.set_title(f'Top {num_top} des Pays Producteurs')
    ax.set_xlabel('Nombre de Titres')
    ax.set_ylabel('Pays')
    sns.despine(left=True, bottom=True)
    return fig

@st.cache_data
def create_histplot_figure(data_df, selectbox_year, bins, color, dark_grey_color):
    """Crée et retourne la figure histplot."""
    fig, ax = plt.subplots()
    sns.histplot(
        data=data_df,
        x=selectbox_year,
        bins=bins,           
        color=color,     
        kde=True,              
        line_kws={           
            'color': dark_grey_color,
            'linewidth': 3}, 
        ax=ax)
    # Personnalisation
    if selectbox_year == "release_year":
        ax.set_title('Distribution des années de sortie')
        ax.set_xlabel('Année de sortie')
    else:
        ax.set_title("Distribution des Années d'ajout")
        ax.set_xlabel("Année d'ajout")
    ax.set_ylabel('Fréquence')
    return fig

# ==========================================================
# FONCTION DE RENDU PRINCIPALE
# ==========================================================

def render_netflix_dashboard(netflix_df):
    st.header("Dashboard Netflix")
    st.markdown("""
    Cette section propose une analyse **statistique** du catalogue Netflix, en utilisant la bibliothèque **Seaborn**.  
    L'objectif est d'identifier la stratégie de contenu de Netflix (Films vs Séries), sa concentration géographique, et l'évolution de son catalogue dans le temps.  
    Les graphiques sont statiques mais sont **régénérés dynamiquement** lorsque vous utilisez les filtres de la barre latérale.
    """)
    st.divider()

    # ===========================================================
    # FILTRES GLOBAUX DE LA SIDEBAR
    # ===========================================================
    st.sidebar.subheader("Filtres Netflix")
    
    # --- Filtre 1: Type (pour KPIs et graphiques) ---
    selected_type = st.sidebar.selectbox("Type de productions", ["Tous", "Movie", "TV Show"])
    
    # --- Filtre 2: Top N (pour Barplot) ---
    nb_top = st.sidebar.number_input("Nombre de pays (Top N)", min_value=5, value=10, max_value=15)

    # --- Filtres 3 & 4: Histogramme ---
    list_year = ["release_year", "year_added"]
    year_selection = st.sidebar.selectbox("Variable pour l'histogramme", list_year)
    nb_bins = st.sidebar.slider("Nombre de Bins (Histogramme)", min_value=10, value=30, max_value=100)

    # ===========================================================
    # FILTRAGE DES DONNÉES
    # ===========================================================
    if selected_type != "Tous":
        df_filtered = netflix_df[netflix_df['type'] == selected_type]
    else:
        df_filtered = netflix_df

    # ===========================================================
    # Les KPI
    # ===========================================================
    st.subheader("Indicateurs Clés")
    
    # Calculs
    total_titles = df_filtered.shape[0]
    avg_lag_time = 0
    if not df_filtered['lag_time'].isnull().all():
        avg_lag_time = int(df_filtered['lag_time'].mean())
        
    most_prod_country = "N/A"
    if not df_filtered['main_country'].isnull().all():
        most_prod_country = df_filtered['main_country'].mode()[0]

    # Colonnes des KPIs 
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3, border=True)
    kpi_col1.metric("Nombre total de titres", total_titles)
    kpi_col2.metric("Délai moyen d'ajout (j)", f"{avg_lag_time} j")
    kpi_col3.metric("Top Pays Producteur", most_prod_country)
    st.divider()

    # ===================================================================================
    # Affichage des Graphiques
    # ===================================================================================
    st.subheader("Analyses Visuelles")

    # Création des colonnes
    col_graph1, col_graph2 = st.columns(2, gap="medium")

    # Graphe 1 : Countplot
    with col_graph1:
        # Appel de la fonction cachée
        fig_countplot = create_countplot_figure(df_filtered, binary_palette, DARK_GREY)
        st.pyplot(fig_countplot)
        with st.expander("🔍 Lire l'analyse"):
            st.markdown("""
                ### 📈 Analyse : Répartition Films vs. Séries

                **1. Le Constat (Ce que le graphique montre)**

                Le `countplot` affiche une **nette asymétrie** dans le catalogue : il y a significativement **plus de Films (Movies) que de Séries (TV Shows)**.

                **2. L'Analyse (Pourquoi ?)**

                Cette distribution n'est pas un hasard, elle est le reflet direct de la stratégie commerciale de Netflix à travers le temps :

                * **Stratégie de la "Longue Traîne" :** Pour construire un catalogue massif et attirer les premiers abonnés, il était plus rapide et économique d'acquérir les droits de licence d'un très grand nombre de **films existants**.
                * **Coût et Engagement :** Un film est un investissement ponctuel. Une série, en revanche, est un **engagement à long terme** (multiples saisons, coûts de production/licence récurrents).
                * **Modèles d'Usage :** Les films comblent un besoin (une soirée de 2h), tandis que les séries (les "Originals" en particulier) sont l'outil principal de **rétention** et de "binge-watching" qui crée le buzz.

                **Conclusion**  
                Le catalogue de Netflix est un équilibre. Il est composé d'une large base de films (le volume pour satisfaire tous les goûts) complétée par des séries à gros budget (la rétention pour fidéliser).""")

    # Graphe 2 : Heatmap
    with col_graph2:
        # Appel de la fonction cachée
        fig_heatmap = create_heatmap_figure(netflix_df)
        st.pyplot(fig_heatmap)
        with st.expander("🔍 Lire l'analyse"):
            st.markdown("""
            ### 📈 Analyse : Matrice de Corrélation

            Cette "heatmap" (carte de chaleur) quantifie la relation linéaire entre les variables numériques de notre dataset, sur une échelle de -1 (négative) à +1 (positive).

            **1. L'Aperçu Stratégique Clé : `release_year` vs `lag_time`**

            * **Constat :** Nous observons une **corrélation négative forte** (score d'environ -0.6 à -0.8).
            * **Analyse :** C'est l'enseignement le plus important. Cela signifie que **plus un contenu est récent (`release_year` élevé), plus son délai d'ajout (`lag_time`) est faible**. C'est la confirmation statistique de la stratégie "Netflix Originals" : en produisant son propre contenu, Netflix le diffuse quasi-instantanément (`lag_time` proche de 0).

            **2. Validation des Données : `duration_min` vs `duration_seasons`**

            * **Constat :** Une corrélation négative très forte (proche de -1).
            * **Analyse :** C'est une validation de la cohérence de nos données. Ces deux variables **s'excluent mutuellement** : un titre est soit un film (une valeur dans `duration_min`), soit une série (une valeur dans `duration_seasons`), mais jamais les deux.

            **3. Autres Observations**

            * **`release_year` vs `year_added` (Positive Forte) :** Corrélation intuitive. Elle confirme que le contenu ajouté récemment (`year_added`) est aussi, en général, du contenu produit récemment (`release_year`).
            * **Absence de Corrélation (`month_added`) :** Le mois d'ajout ne montre aucun lien linéaire avec les autres facteurs, ce qui est attendu.

            **Conclusion :**
            Cette matrice valide la structure de nos données (films vs séries) et, plus important encore, elle fournit une preuve quantitative de l'évolution stratégique de Netflix vers la production et la diffusion immédiate de son propre contenu.""")

    st.divider()

    # Graphe 3 : Boxplots
    col_box1, col_box2 = st.columns(2, gap="medium")
    
    # Appel des fonctions cachées
    boxplot_movies = create_boxplot_movies(netflix_df, NETFLIX_RED)
    boxplot_series = create_boxplot_series(netflix_df, DARK_GREY)

    with col_box1:
        st.pyplot(boxplot_movies)
    with col_box2:
        st.pyplot(boxplot_series)

    with st.expander("🔍 Lire l'analyse des Boxplots"):
        st.markdown("""
        ### 📈 Analyse Comparée : Durée des Films vs. Séries

        Ces deux "boxplots" (boîtes à moustaches) illustrent parfaitement les **deux stratégies de contenu radicalement différentes** de Netflix pour les films et les séries.

        #### 1. Le Film : Le Distributeur Classique

        Ce boxplot montre la répartition de la durée (en minutes) de tous les films.

        * **Le Constat :** La boîte (le 50% central du catalogue) est concentrée autour de **90-110 minutes**. La ligne médiane (le film "typique") se situe également dans cette plage.
        * **L'Analyse :** Netflix respecte les **standards de l'industrie cinématographique**. Le format du long-métrage classique est la norme.
        * **Les Outliers (Points isolés) :** Ils sont nombreux et cruciaux pour la stratégie de "niche" :
            * **À gauche (< 60 min) :** Documentaires courts, comédies spéciales (stand-up), ou programmes pour enfants.
            * **À droite (> 150 min) :** Films d'auteur longs, épopées historiques, ou versions "Director's Cut".

        #### 2. La Série : L'Investisseur à Haut Risque

        Ce graphique, qui montre le nombre de saisons, est le plus révélateur de la stratégie Netflix.

        * **Le Constat :** Le graphique est **totalement écrasé à gauche**. La ligne **médiane** (le point central de 50% des données) est située à **1 saison**.
        * **L'Analyse :** C'est l'enseignement principal. La moitié de toutes les séries du catalogue n'ont jamais dépassé leur première saison.
            1.  **Le "Cimetière Netflix" :** Cela reflète la stratégie "impitoyable" de Netflix, qui annule rapidement les séries qui n'atteignent pas leurs objectifs d'audience.
            2.  **La Montée des Mini-séries :** Une grande partie de ces "1 saison" sont aussi des "Limited Series" (ex: *Le Jeu de la Dame*), un format volontairement court, moins risqué et très populaire.
            3.  **Les "Hits" sont l'Exception :** Les séries à succès (les outliers comme *Stranger Things* ou *The Crown*) sont l'exception statistique qui finance le reste.

        #### 3. Conclusion : Films (Volume) vs. Séries (Rétention)

        * **Question :** Les films sont-ils plus longs que les séries ?
        * **Réponse :** Les unités (minutes vs. saisons) sont incomparables. Mais si l'on pose une **hypothèse** (une série médiane = 1 saison de 8 épisodes * 45 min = 360 min), on constate qu'une série est **largement plus longue** qu'un film médian (100 min).

        **Conclusion :** Netflix utilise les **Films** pour le **volume** (satisfaire tous les goûts) et les **Séries** pour la **rétention** (créer des "hits" qui fidélisent les abonnés).""")
    
    st.divider()
    
    # Graphe 4 : Barplot & Graphe 5 : Histplot
    col_bar, col_hist = st.columns(2, gap="medium")

    # Graphe 4 : Barplot
    with col_bar:
        st.subheader(f"Top {nb_top} des Pays")
        # Appel de la fonction caché
        fig_barplot = create_barplot_figure(df_filtered, nb_top, NETFLIX_RED)
        st.pyplot(fig_barplot)
        with st.expander("🔍 Lire l'analyse"):
            st.markdown("""
            ### 📈 Analyse : Domination Géographique

            Le `barplot` illustre la répartition géographique des productions de contenu sur Netflix, en se concentrant sur les **N** premiers pays (défini par le widget).

            **1. Le Constat (Ce que le graphique montre)**

            Quelle que soit la valeur de N (5, 10 ou 15), le constat est sans appel :

            * **Hégémonie Américaine :** Les **États-Unis** ne sont pas seulement en tête, ils dominent de manière écrasante. Leur production représente souvent plus que les 9 autres pays du top 10 réunis.
            * **Les Puissances Secondaires :** L'**Inde** (grâce à Bollywood et à sa large population) et le **Royaume-Uni** (forte industrie télévisuelle) se distinguent clairement comme les deux autres piliers de la production.
            * **La "Longue Traîne" :** On observe un **fossé important** après le trio de tête. La contribution des autres pays chute rapidement, ce qui montre que si le catalogue est "international", il est en réalité fortement concentré sur quelques acteurs majeurs.

            **2. L'Analyse (Pourquoi ?)**

            Cette domination s'explique par une combinaison de facteurs historiques et économiques :

            * **Héritage d'Hollywood :** Les États-Unis sont les pionniers de l'industrie cinématographique moderne et disposent d'un catalogue historique inégalé.
            * **Origine de Netflix :** Netflix est une entreprise américaine. Son service a d'abord été lancé et optimisé pour son marché domestique.
            * **Force d'Exportation Culturelle :** Le contenu américain (films et séries en langue anglaise) a la plus grande force d'exportation culturelle au monde.
""")

    # Graphe 5 : Histplot
    with col_hist:
        st.subheader("Distribution Temporelle")
        # Appel de la fonction cachée
        fig_hist = create_histplot_figure(df_filtered, year_selection, nb_bins, NETFLIX_RED, DARK_GREY)
        st.pyplot(fig_hist)
        with st.expander("🔍 Lire l'analyse"):
            st.markdown("""
            ### 📈 Analyse : Évolution Temporelle du Catalogue

            Cet histogramme montre la distribution du contenu Netflix soit par **Année de Sortie** (son "âge" réel), soit par **Année d'Ajout** (son arrivée sur la plateforme). L'analyse change radicalement en fonction de votre choix.

            #### 1. Si vous sélectionnez "release_year" (Année de Sortie)

            * **Le Constat :** Le graphique est **fortement asymétrique à gauche** (*left-skewed*). La grande majorité des films et séries disponibles ont été produits au cours des 5 à 10 dernières années.
            * **L'Analyse :** Cela illustre la stratégie de Netflix axée sur la **"fraîcheur"**. Le modèle économique repose sur un renouvellement constant, le lancement de "Netflix Originals" (qui ont un `lag_time` de 0) et l'acquisition de contenus récents. Le catalogue n'est pas une "archive" du cinéma, c'est une plateforme de nouveautés.

            #### 2. Si vous sélectionnez "year_added" (Année d'Ajout)

            * **Le Constat :** Le graphique montre une **croissance exponentielle** des ajouts de contenu, culminant autour de 2018-2019, suivie d'une **baisse notable** en 2020-2021.
            * **L'Analyse :** C'est l'histoire de l'essor du streaming. La baisse de 2020 n'est pas un désintérêt, mais le résultat de deux facteurs majeurs :
            1. **COVID-19 :** L'arrêt brutal de toutes les productions mondiales a tari le "pipeline" de nouveaux contenus.
            2. **La Concurrence :** L'arrivée de Disney+, HBO Max, etc., a non seulement fragmenté le marché mais a aussi poussé Netflix à pivoter d'une stratégie de "volume" à une stratégie de "qualité" (blockbusters).""")