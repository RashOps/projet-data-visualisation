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

# Imporation des dépendances
import streamlit as st
import matplotlib.pyplot as plt
import  seaborn as sns
from utils.chart_styles import setup_netflix_theme

def render_netflix_dashboard(netflix_df):
    st.header("Dashboard Netflix")
    st.markdown("""
    Cette section propose une analyse **statistique** du catalogue Netflix, en utilisant la bibliothèque **Seaborn**.  
    L'objectif est d'identifier la stratégie de contenu de Netflix (Films vs Séries), sa concentration géographique, et l'évolution de son catalogue dans le temps.  
    Les graphiques sont statiques mais sont **régénérés dynamiquement** lorsque vous utilisez les filtres de la barre latérale.
    """)

    # ===========================================================
    # Les KPI
    st.divider()
    st.sidebar.subheader("Explorez les KPIs")
    selected_type = st.sidebar.selectbox("Type de productions", ["Tous", "Movie", "TV Show"])
    if selected_type != "Tous":
        df_filtered = netflix_df[netflix_df['type'] == selected_type]
    else:
        df_filtered = netflix_df

    # Section KPIs
    st.subheader("Indicateurs Clés")

    # Calculs
    total_titles = df_filtered.shape[0]
    avg_lag_time = int(df_filtered['lag_time'].mean())
    most_prod_country = df_filtered['main_country'].mode()[0]

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3, border=True)

    with kpi_col1 :
        st.metric("Nombre total de titres", total_titles)
    with kpi_col2 : 
        st.metric("Délai moyen d'ajout (jours)", f"{avg_lag_time} j")
    with kpi_col3 :
        st.metric("Top Pays Producteur", most_prod_country)

    st.divider()

    # =============================================================================
    # --- CHARTE GRAPHIQUE ---
    main_palette, binary_palette, heatmap_cmap, LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED = setup_netflix_theme()

    # ===================================================================================
    # Netflix dataset ===================================================================
    st.subheader("Graphes Statiques")

    graph_stat_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)
    # Gaphe 1 : Diagramme ==================================
    # Création de la fonction
    @st.cache_data
    def create_countplot_figure(data_df, palette, color) :
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

        # Ajout des étiquettes de valeur au-dessus des barres
        ax.bar_label(ax.containers[0], fontsize=12, color=color)
        ax.bar_label(ax.containers[1], fontsize=12, color=color)

        # Gérer le cas où il n'y a qu'un seul container (si filtré)
        for container in ax.containers:
            ax.bar_label(container, fontsize=12, color=color)
        return fig
    
    # Appel de la fonction
    fig_countplot = create_countplot_figure(netflix_df, binary_palette, DARK_GREY)

    with graph_stat_col[0] :
        # Affichage du graphe
        st.pyplot(fig_countplot)
        with st.expander("🔍 Lire l'analyse") :
            st.markdown("""
                ### 📈 Analyse : Répartition Films vs. Séries

                **1. Le Constat (Ce que le graphique montre)**

                Le `countplot` affiche une **nette asymétrie** dans le catalogue : il y a significativement **plus de Films (Movies) que de Séries (TV Shows)**.

                **2. L'Analyse (Pourquoi ?)**

                Cette distribution n'est pas un hasard, elle est le reflet direct de la stratégie commerciale de Netflix à travers le temps :

                * **Stratégie de la "Longue Traîne" :** Pour construire un catalogue massif et attirer les premiers abonnés, il était plus rapide et économique d'acquérir les droits de licence d'un très grand nombre de **films existants**.
                * **Coût et Engagement :** Un film est un investissement ponctuel. Une série, en revanche, est un **engagement à long terme** (multiples saisons, coûts de production/licence récurrents).
                * **Modèles d'Usage :** Les films comblent un besoin (une soirée de 2h), tandis que les séries (les "Originals" en particulier) sont l'outil principal de **rétention** et de "binge-watching" qui crée le buzz.

                **Conclusion :** Le catalogue de Netflix est un équilibre. Il est composé d'une large base de films (le volume pour satisfaire tous les goûts) complétée par des séries à gros budget (la rétention pour fidéliser).
            """)


    # Graphe 2 : Heatmap ===================
    # Création de la fonction
    @st.cache_data
    def create_heatmap_figure(data_df) :
        fig, ax = plt.subplots()
        numeric_cols = ['release_year', 'year_added', 'month_added', 'lag_time', 'duration_min', 'duration_seasons']
        corr_matrix = data_df[numeric_cols].corr()

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

        return fig
    
    # Appel de la fonction
    fig_heatmap = create_heatmap_figure(netflix_df)

    with graph_stat_col[1] :
        # Affichage du graphe
        st.pyplot(fig_heatmap)
        with st.expander("🔍 Lire l'analyse") :
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
            Cette matrice valide la structure de nos données (films vs séries) et, plus important encore, elle fournit une preuve quantitative de l'évolution stratégique de Netflix vers la production et la diffusion immédiate de son propre contenu.
            """)

    # Graphe 3 : Boxplot ======================
    boxplot_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)


    # Graphique 1 : Durée des films
    # Création de la fonction
    @st.cache_data
    def create_boxplot_movies(data_df, color) :
        fig1, ax1 = plt.subplots()
        sns.boxplot(
            data=data_df[data_df['type'] == 'Movie'],
            x='duration_min',
            color=color,
            ax=ax1)

        # Personnalisation 
        ax1.set_title('Distribution de la Durée des Films (en minutes)')
        ax1.set_xlabel('Durée (minutes)')

        return fig1
    
    # Appel de la fonction
    boxplot_movies = create_boxplot_movies(netflix_df, NETFLIX_RED)


    # Graphique 2 : Nombre de Saisons des Séries
    # Création de la fonction
    @st.cache_data
    def create_boxplot_series(data_df, color) :
        fig2, ax2 = plt.subplots()
        sns.boxplot(
            data=data_df[data_df['type'] == 'TV Show'].dropna(subset=['duration_seasons']),
            x='duration_seasons',
            color=color,
            ax=ax2)
        
        # Personnalisation 
        ax2.set_title('Distribution du Nombre de Saisons (Séries TV)')
        ax2.set_xlabel('Nombre de Saisons')

        return fig2

    # Appel de la fonction
    boxplot_series = create_boxplot_series(netflix_df, DARK_GREY)

    with boxplot_col[0] :
        # Affichage graphe de la Durée des films
        st.pyplot(boxplot_movies)

    with boxplot_col[1] :
        # A ffichage graphe de la Durée des séries
        st.pyplot(boxplot_series)

    with st.expander("🔍 Lire l'analyse") :
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

        **Conclusion :** Netflix utilise les **Films** pour le **volume** (satisfaire tous les goûts) et les **Séries** pour la **rétention** (créer des "hits" qui fidélisent les abonnés).
        """)

    st.write("")
    st.write("")
    st.divider()
    st.subheader("Gaphes intéractifs")

    interactif_graph_col = st.columns(2, gap="medium", vertical_alignment="center", width=1300)
    # Graphe 4 : Diagramme en barre ============================
    # Préparation des données (Top 10)
    st.sidebar.write("")
    st.sidebar.subheader("Top des pays producteurs")
    nb_top10_countries = st.sidebar.number_input("Modifiez le nombre de pays", min_value=5, value=10, max_value=15)
    top_10_countries = netflix_df['main_country'].value_counts().head(nb_top10_countries).reset_index()
    top_10_countries.columns = ['country', 'count']

    # Création de la fonction
    @st.cache_data
    def create_barplot_figure(data_df, color) :
        fig, ax = plt.subplots()
        sns.barplot(
            data=data_df,
            x='count',
            y='country',
            color=color,  
            saturation=0.9,     
            ax=ax
        )

        # Personnalisation 
        ax.set_title(f'Top {nb_top10_countries} des Pays Producteurs')
        ax.set_xlabel('Nombre de Titres')
        ax.set_ylabel('Pays')

        # Cacher les bordures
        sns.despine(left=True, bottom=True)

        return fig

    # Appel de la fonction
    barplot_fig =  create_barplot_figure(top_10_countries, NETFLIX_RED)

    with interactif_graph_col[0] :
        # Affichage du graphique
        st.pyplot(barplot_fig)
        with st.expander("🔍 Lire l'analyse") :
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

    # Graphe 5 : Histogramme ==================================
    st.sidebar.write("")
    st.sidebar.subheader("Distribution des sorties / Ajouts des productions")

    # Widget 1
    nb_bins = st.sidebar.slider("Faites varier le nombre de bins", min_value=1, value=20, max_value=100)
    # Widget 2
    list_year = ["release_year", "year_added"]
    year_selection = st.sidebar.selectbox("Choisissez la variable", list_year)

    # Création de la fonction
    @st.cache_data
    def create_histplot_figure(data_df, selectbox_year, bins, color, dark_grey_color) :
        fig, ax = plt.subplots()
        sns.histplot(
            data=data_df,
            x=selectbox_year,
            bins=bins,               
            color=color,       
            kde=True,              
            line_kws={             
                # Personnalisation de la ligne KDE
                'color': dark_grey_color,
                'linewidth': 3}, 
            ax=ax)

        # Personnalisation
        if selectbox_year == "release_year" :
            ax.set_title('Distribution des années de sortie du contenu')
            ax.set_xlabel('Année de sortie')
        else :
            ax.set_title("Distribution des Années d'ajout du contenu")
            ax.set_xlabel('Année d\'ajout')

        ax.set_ylabel('Fréquence')

        return fig

    # Appel de la fonction
    histplot_fig = create_histplot_figure(netflix_df, year_selection, nb_bins, NETFLIX_RED, DARK_GREY)

    with interactif_graph_col[1] :
        # Affichage du graphe
        st.pyplot(histplot_fig)
        with st.expander("🔍 Lire l'analyse") :
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
            2. **La Concurrence :** L'arrivée de Disney+, HBO Max, etc., a non seulement fragmenté le marché mais a aussi poussé Netflix à pivoter d'une stratégie de "volume" à une stratégie de "qualité" (blockbusters).
            """)