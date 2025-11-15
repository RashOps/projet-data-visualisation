"""
Page "Processus" : Visualisation Statique Seaborn (Netflix).

Ce script correspond à la page "3_📈_Partie 1 - Les graphiques Seaborn"
de l'application. Son objectif est de documenter le processus
d'analyse et de visualisation (statique), conformément au
cahier des charges de la Partie 1.

Il contient :
1.  Le chargement du dataset nettoyé (`netflix_cleaned.csv`).
2.  La définition de la charte graphique Seaborn (`setup_netflix_theme`).
3.  Le code de création de chaque graphique statique (countplot,
    barplot, boxplot, histplot, heatmap).
4.  L'analyse textuelle et l'interprétation détaillée sous chaque
    graphique, répondant aux questions du projet.

Cette page est le "rapport d'analyse" statique, distincte du
Dashboard interactif.
"""

# Importation des dépendances
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.chart_styles import setup_netflix_theme
from data_loader import load_netflix_data_analysis 

# Configuration de la page principale
st.set_page_config(
    page_title="Visualisation Seaborn du dataset Netflix",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state = "expanded"
)

st.sidebar.subheader("Visualisation des graphiques Seaborn 📈")

# ===========================================================================================================================
# Titre principal
st.title("Création des graphiques avec Seaborn")

# =============================================================================================================================

st.info("""
    **Note** : Si vous n'avez pas encore vu les étapes du nettoyage du dataset original, cliquez sur le lien ci-dessous pour accéder aux étapes du nettoyage.""", 
    icon="💡")

st.link_button("Analyse exploratoire et nettoyage", url="/Partie_1_-_Analyse_Exploratoire")

# =============================================================================================================================
st.subheader("Visualisation du dataset nettoyé")

# Chargement du dataframe
netflix = load_netflix_data_analysis()

if netflix is None:
    st.error("Échec du chargement du fichier 'netflix_cleaned.csv'.")
    st.stop() 

st.markdown("""
    Après le nettoyage de notre dataframe et la création d'un nouveau dataframe exploitable, nous nous attaquerons à la création des graphiques avec **Seaborn** afin d'analyser nos données.

    Cette étape sera précédée par une **analyse descriptive** du dataframe nettoyé.
""")

st.dataframe(netflix, use_container_width=True) 

# ===========================================================================================================================
# Analyse descriptive
st.divider()
st.write("")
st.subheader("Analyse descriptive préliminaire")

st.markdown("""
    Dans cette analyse, nous verrons :

    * Le nombre de films vs séries.
    * La répartition des contenus par pays et par année.
    * La répartition des genres les plus représentés.
""")

with st.expander("Découvrir le code (Analyse Descriptive)"):
    with st.echo():
        # Analyse descriptive - Partie 1 : Nombre de film VS Serie
        nbre_production_total = netflix['show_id'].count()
        nbre_production_par_type = netflix.groupby('type').count()['show_id']

        # Répartition des productions par pays
        repartition_prod_pay = netflix.groupby('main_country').count()['show_id'].reset_index()
        repartition_prod_pay_sorted = repartition_prod_pay.sort_values(by=['show_id'], ascending=False)

        # Analyse descriptive - Partie 2 : Répartition des productions par année de production
        repartition_prod_year = netflix.groupby(['release_year']).count()['show_id'].reset_index()
        repartition_prod_year_sorted = repartition_prod_year.sort_values(by=['show_id'], ascending=False)
        
        # Analyse descriptive - Partie 3 : Répartition des productions par genre
        repartition_prod_genre = netflix.groupby(['main_genre']).count()['show_id'].reset_index()
        repartition_prod_genre_sorted = repartition_prod_genre.sort_values(by=['show_id'], ascending=False)

# Nombres Séries VS Films
text = f"Nous observons ainsi : **{nbre_production_par_type['Movie']} films** et **{nbre_production_par_type['TV Show']} séries**, sur **{nbre_production_total} productions totales**."
st.info(text, icon="✨")

# Création des colonnes
col1, col2 = st.columns(2)

# Repartition des contenus par pays ==================================
with col1:
    st.markdown("#### Répartition du contenus par pays")
    nb_pays = st.number_input("Entrez un nombre pour voir la liste du classement des pays, ou 99 pour voir toute la liste.", min_value=5, value=5, max_value=99)
    
    if nb_pays == 99:
        st.dataframe(repartition_prod_pay_sorted, use_container_width=True)
    else:
        st.dataframe(repartition_prod_pay_sorted.head(nb_pays), use_container_width=True)

# Repartition des contenus par années ================================
with col2:
    st.markdown("#### Répartition du contenus par années de production")
    nb_years = st.number_input("Entrez un nombre pour voir la liste de la repartition des titres par année, ou 99 pour voir toute la liste.", min_value=5, value=5, max_value=99)
    
    if nb_years == 99:
        st.dataframe(repartition_prod_year_sorted, use_container_width=True)
    else:
        st.dataframe(repartition_prod_year_sorted.head(nb_years), use_container_width=True)

# Repartition du contenu par genre =================================
st.write("")
st.write("")
st.markdown("#### Répartition du contenus par genre")

nb_genre = st.number_input("Entrez un nombre pour voir la liste de la repartition de contenu par genre, ou 99 pour voir toute la liste.", min_value=5, value=5, max_value=99)

if nb_genre == 99:
    st.dataframe(repartition_prod_genre_sorted, use_container_width=True)
else:
    st.dataframe(repartition_prod_genre_sorted.head(nb_genre), use_container_width=True)

# ===========================================================================================================================
# --- Chargement de la charte graphique ---
st.subheader("Chargement de la charte graphique")
st.markdown("Nous chargeons la charte graphique définie dans `utils/chart_styles.py`.")

with st.echo():
    main_palette, binary_palette, heatmap_cmap, LIGHT_GREY, DARK_GREY, NETFLIX_BLACK, NETFLIX_RED = setup_netflix_theme()

st.info("Charte graphique appliquée (`sns.set_theme()`).", icon="🎨")

# ==========================================================================================================================
# Graphe 1 : countplot() ======================================================
st.divider()
st.subheader("Graphe 1 : Comparaison films VS séries (`countplot`)")

with st.expander("Découvrir le code"):
    with st.echo():
        # Optimisation (Mise en cache)
        @st.cache_data
        def create_countplot_figure(data_df, palette, color):
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

# Affichage du graphe
fig_countplot = create_countplot_figure(netflix, binary_palette, DARK_GREY)
st.pyplot(fig_countplot)

with st.expander("🔍 Lire l'analyse"):
    st.markdown("""
    Comme l'a confirmé le diagramme `countplot`, le catalogue Netflix est dominé par les films.
    Cette disproportion s'explique historiquement par :
    1.  **Coûts de Licence :** Plus rentable d'acquérir des films existants pour construire un catalogue volumineux.
    2.  **Modèle de la "Longue Traîne" :** Satisfaire des goûts de niche très variés.
    3.  **Coûts de Production :** Les séries sont un investissement plus lourd et à plus long terme.
    """)


# Graphe 2 : barplot() ==============================================
st.write("")
st.write("")
st.subheader("Graphe 2 : Top N des pays producteurs (`barplot`)")

nb_top_countries = st.number_input("Entrez un nombre pour modifier le graphe", min_value=5, value=10, max_value=15)

with st.expander("Découvrir le code"):
    with st.echo():
        # Optimisation (Mise en cache)
        @st.cache_data
        def create_barplot_figure(data_df, num_top, color):
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

# Affichage du graphique
fig_barplot = create_barplot_figure(netflix, nb_top_countries, NETFLIX_RED)
st.pyplot(fig_barplot)

with st.expander("🔍 Lire l'analyse"):
    st.markdown("""
    Le `barplot` illustre une **domination écrasante des États-Unis**.
    Cela s'explique par :
    1.  **Héritage Historique (Hollywood)**
    2.  **Origine de Netflix** (entreprise américaine)
    3.  **Influence Culturelle** (forte exportation du contenu US)
    """)

# Graphe 3 : histplot() ==============================================
st.write("")
st.write("")
st.subheader("Graphe 3 : Distribution par années de sortie (`histplot`)")

nb_bins_hist = st.number_input("Faites varier le nombre de bins", min_value=20, value=50, max_value=100)

with st.expander("Découvrir le code"):
    with st.echo():
        # Optimisation (Mise en cache)
        @st.cache_data
        def create_histplot_figure(data_df, bins, color, dark_grey_color):
            fig, ax = plt.subplots()
            sns.histplot(
                data=data_df,
                x='release_year',
                bins=bins,
                color=color,
                kde=True,
                line_kws={
                    'color': dark_grey_color,
                    'linewidth': 3
                },
                ax=ax)
            ax.set_title('Distribution des Années de Sortie du Contenu')
            ax.set_xlabel('Année de Sortie')
            ax.set_ylabel('Fréquence')
            return fig

# Affichage du graphe
fig_hist = create_histplot_figure(netflix, nb_bins_hist, NETFLIX_RED, DARK_GREY)
st.pyplot(fig_hist)

with st.expander("🔍 Lire l'analyse"):
    st.markdown("""
    L'histogramme montre une **asymétrie à gauche** prononcée :
    * **Le Pic :** La majorité du catalogue a été produite ces 5-10 dernières années.
    * **L'Analyse :** C'est la stratégie de la "fraîcheur". Netflix se positionne comme une plateforme de **nouveautés** (grâce aux "Originals") plutôt que comme une **archive** du cinéma.
    """)

# Graphe 4 : heatmap() ==============================================
st.write("")
st.write("")
st.subheader("Graphe 4 : Matrice de corrélation (`heatmap`)")

with st.expander("Découvrir le code"):
    with st.echo():
        # Optimisation (Mise en cache)
        @st.cache_data
        def create_heatmap_figure(data_df):
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

# Affichage du graphe
fig_heatmap = create_heatmap_figure(netflix)
st.pyplot(fig_heatmap)

with st.expander("🔍 Lire l'analyse"):
    st.markdown("""
    Cette matrice quantifie les relations linéaires entre les variables :
    1.  **`release_year` vs `lag_time` (Négative Forte)** : C'est la confirmation de la stratégie "Originals". Plus un contenu est récent (`release_year` haut), plus son délai d'ajout (`lag_time`) est faible.
    2.  **`duration_min` vs `duration_seasons` (Négative Forte)** : C'est une validation des données. Un titre est soit un film, soit une série, jamais les deux.
    """)

# Graphe 5 : boxplot() ==============================================
st.write("")
st.write("")
st.subheader("Graphe 5 : Durée moyenne selon le type de contenu (`boxplot`)")

with st.expander("Découvrir le code"):
    with st.echo():
        # Optimisation (Mise en cache)
        @st.cache_data
        def create_boxplots_figures(data_df, movie_color, series_color):
            # Graphique 1 : Durée des films
            fig1, ax1 = plt.subplots()
            sns.boxplot(
                data=data_df[data_df['type'] == 'Movie'],
                x='duration_min',
                color=movie_color,
                ax=ax1)
            ax1.set_title('Distribution de la Durée des Films (en minutes)')
            ax1.set_xlabel('Durée (minutes)')

            # Graphique 2 : Nombre de Saisons des Séries
            fig2, ax2 = plt.subplots()
            sns.boxplot(
                data=data_df[data_df['type'] == 'TV Show'].dropna(subset=['duration_seasons']),
                x='duration_seasons',
                color=series_color,
                ax=ax2)
            ax2.set_title('Distribution du Nombre de Saisons (Séries TV)')
            ax2.set_xlabel('Nombre de Saisons')
            
            return fig1, fig2

col3, col4 = st.columns(2)

# Affichage de nos boxplots
fig_box1, fig_box2 = create_boxplots_figures(netflix, NETFLIX_RED, DARK_GREY)
with col3:
    st.pyplot(fig_box1)
with col4:
    st.pyplot(fig_box2)

with st.expander("🔍 Lire l'analyse"):
    st.markdown("""
    Ces boxplots révèlent deux stratégies distinctes :

    #### 1. Distribution de la Durée des Films
    * **Le Constat :** La boîte centrale est concentrée autour de **90-110 minutes**.
    * **L'Analyse :** Netflix respecte les standards de l'industrie. Les "outliers" (points isolés) montrent la diversité du catalogue (formats courts et longs). Netflix agit en **distributeur classique**.

    #### 2. Distribution du Nombre de Saisons
    * **Le Constat :** Le graphique est "écrasé" à gauche. La **médiane est à 1 saison**.
    * **L'Analyse :** C'est l'enseignement principal. Plus de 50% des séries n'ont jamais dépassé la saison 1.
        1.  **Le "Cimetière Netflix" :** Annulation rapide des séries peu performantes.
        2.  **Les Mini-séries :** Un format populaire et moins risqué.
        3.  **Les "Hits" sont l'Exception :** Les outliers (ex: *Stranger Things*) sont l'exception, pas la règle.
    * **Conclusion :** Pour les séries, Netflix agit en **investisseur à haut risque**.
    """)

# ===============================================================================================================
# Questions analyses Netflix
st.write("")
st.write("")
st.header("Analyse supplémentaire (Questions du Cahier des Charges)")

st.subheader("Domination géographique") 
st.markdown("""
    **Question** : Quels pays dominent la production Netflix ? 
""")

with st.expander("Découvrir le code"):
    with st.echo():
        repartition_prod_pay_sorted['contribution_pays_%'] = (repartition_prod_pay_sorted['show_id'] * 100 / nbre_production_total).round(2)
    
nb_repartition_prod = st.number_input("Découvrez la contribution d'autres pays", min_value=5, value=10, max_value=99)
st.dataframe(repartition_prod_pay_sorted.head(nb_repartition_prod), use_container_width=True)

st.markdown("""
    L'analyse de cette répartition met en lumière trois points majeurs :

    * **Hégémonie Américaine :** Les **États-Unis** ne sont pas seulement en tête, ils dominent de manière écrasante. Avec plus d'un tiers (**36,5 %**) du catalogue total, leur production représente plus que les 9 autres pays du top 10 réunis.  
    * **Les Puissances Secondaires :** L'**Inde** (grâce à Bollywood) et le **Royaume-Uni** (forte industrie télévisuelle) se distinguent clairement comme les deux autres piliers de production, bien que loin derrière les États-Unis.  
    * **La Longue Traîne :** On observe un **fossé important** après le trio de tête. La contribution des autres pays chute rapidement (passant de 7,1 % pour le Royaume-Uni à seulement 3 % pour le Canada). Cela montre que si le catalogue est international, il est en réalité fortement concentré sur quelques acteurs majeurs.
""")


st.write("")
st.write("")
st.subheader("Évolution temporelle") # =====================================
st.markdown("""
    **Question** : Comment évolue la quantité de contenu publié dans le temps ?
    Analyser les tendances de croissance et les périodes clés d'expansion.
""")

st.markdown("""
    #### 1. Les Grandes Périodes de Croissance

    L'évolution du nombre de contenus ajoutés sur Netflix peut être décomposée en trois phases distinctes :

    * **Phase 1 : L'ère DVD (1997-2007)**
        À sa création, Netflix se concentrait sur la location de DVD. La croissance des contenus ajoutés à son service de streaming (lancé plus tard) était donc logiquement faible.

    * **Phase 2 : L'essor du Streaming (2007-2019)**
        À partir de 2007, Netflix se lance dans le streaming en ligne. Le nombre de contenus ajoutés connaît alors une croissance rapide, devenant exponentielle jusqu'à atteindre un pic historique dans la période 2018-2019.

    * **Phase 3 : Le Ralentissement (2020-2021)**
        On observe une baisse notable et soudaine des ajouts de contenu à partir de 2020.

    #### 2. Pourquoi une Baisse à Partir de 2020 ?

    Cette rupture de tendance s'explique principalement par deux hypothèses :

    * **Hypothèse 1 : L'impact du COVID-19 (L'explication la plus probable)**
        Les ajouts de contenu ne sont pas instantanés. La plupart des productions mondiales (films et séries) ont été **mises à l'arrêt total à partir de mars 2020**. Par conséquent, le "pipeline" de nouveaux contenus qui devaient sortir fin 2020 et en 2021 s'est tari. Il s'agit d'une **rupture de la chaîne de production mondiale** plutôt que d'un désintérêt stratégique de Netflix.

    * **Hypothèse 2 : Saturation et Concurrence**
        Les années 2019-2020 ont vu l'arrivée de concurrents majeurs (Disney+, HBO Max, Apple TV+). Face à un marché saturé, Netflix a pu commencer à **pivoter sa stratégie** : passant d'une "croissance à tout prix" (maximiser le volume) à une **stratégie de "qualité et d'exclusivité"** (produire moins, mais des "blockbusters" plus impactants).
""")


st.write("")
st.write("") 
st.subheader("Comparaison durée") # =====================================
st.markdown("""
    **Question** : Les films sont-ils en moyenne plus longs que les séries ? 
    Comparer les distributions de durée entre les deux types de contenu.
""")

st.markdown("""
    #### 1. La Difficulté de la Comparaison Directe

    Une comparaison directe de la "longueur" est délicate, car nos `boxplots` utilisent des unités de mesure incompatibles :

    * Les films sont mesurés en **minutes**.
    * Les séries sont mesurées en **saisons**.

    De plus, il nous manque des informations clés : le nombre d'épisodes par saison et la durée moyenne de ces épisodes.

    #### 2. Hypothèse pour l'Estimation

    Pour contourner ce problème, nous allons poser une hypothèse basée sur une série TV standard. Prenons une série type de **8 épisodes**, avec une durée moyenne de **45 minutes** par épisode.

    > **Calcul :** 8 épisodes * 45 minutes/épisode = **360 minutes**

    #### 3. Conclusion

    Notre analyse a montré que :

    1.  La durée médiane d'un **film** sur Netflix est d'environ **100 minutes**.
    2.  La durée médiane d'une **série** est de **1 saison**.

    Même en se basant sur la série la plus "courte" (1 saison), celle-ci représente déjà **360 minutes** de visionnage.

    **En conclusion, une seule saison de série est en moyenne 3 à 4 fois plus longue qu'un film.**
""")