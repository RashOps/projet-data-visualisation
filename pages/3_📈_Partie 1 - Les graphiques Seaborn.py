# Imporation des dépendances
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page principale
st.set_page_config(
    page_title="Partie 1 - Les graphiques Seaborn",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state = "expanded"
)

st.sidebar.subheader("Visualisation des graphiques Seaborn 📈")

# ===========================================================================================================================
st.title("Création des graphiques avec Seaborn")

# =============================================================================================================================

st.info("""
    **Note** : Si vous n'avez pas encore vu les étapes du nettoyage du dataset original,
    Cliquez sur le lien ci-dessous pour acceder aux étapes du nettoyage.""", 
    icon="💡"
    )

st.link_button("Analyse exploratoire et nettoyage", url="/Partie_1_-_Analyse_Exploratoire")

# =============================================================================================================================
# Visualisation du dataset nettoyé
st.subheader("Visualisation du dataset nettoyé")
st.markdown("""
    Après le nettoyage de notre dataframe, et la création d'un nouveau dataframe exploitable,
    nous nous attaquerons à la création des graphiques avec Seaborn afin d'analyser nos données.
    Qui sera précédé par une analyse descriptive du dataframe nettoyé.
""")

# Chargmenet du dataframe
from data_loader import load_netflix_data_analysis
netflix = load_netflix_data_analysis()

st.dataframe(netflix)

# ===========================================================================================================================
# Analyse descriptive
st.divider()
st.write("")
st.subheader("Pré-analyse : analyse descriptive")

st.markdown("""
    Dans cette analyse, nous verrons : 
    - Nombre de films vs séries, 
    - La répartition des contenus par pays et par année
    - La répartition par genres les plus représentés
""")

with st.expander("Découvrez le code") : 
    with st.echo() :
        # Analyse descriptive - Partie 1 : Nombre de film VS Serie
        nbre_production_total = netflix['show_id'].count() # Détermination du nombre total de production (films + Series)
        nbre_production_par_type = netflix.groupby('type').count()['show_id']

        # Répartition des productions par pays (Suite)
        repartition_prod_pay = netflix.groupby('main_country').count()['show_id'].reset_index()
        repartition_prod_pay_sorted = repartition_prod_pay.sort_values(by=['show_id'], ascending=False)


        # Analyse descriptive - Partie 2 : Répartition des productions par année de production
        repartition_prod_year = netflix.groupby(['release_year']).count()['show_id'].reset_index()
        repartition_prod_year_sorted = repartition_prod_year.sort_values(by=['show_id'], ascending=False)

# Nombres Séries VS Films
text = f"On observe ainsi : **{nbre_production_par_type['Movie']} films** et **{nbre_production_par_type['TV Show']} series**, sur **{nbre_production_total} productions totales**."
st.info(text, icon="✨")

# Création des colonnes
col1, col2 = st.columns(2)


# Repartition des contenus par pays ==================================
with col1 : 
    st.markdown("#### Répartition du contenus par pays")
    nb_pays = st.number_input("Entrez un nombre pour voir la liste du classement des pays .", min_value=5, max_value=99)
    st.markdown("""
        Entrez un nombre pour voir le classement des pays basé sur la repartition du contenus par pays.  
        Entrez 99 pour voir l'entièreté du classement.""")

    if nb_pays == 99 : 
        st.dataframe(repartition_prod_pay_sorted)
    else :
        st.dataframe(repartition_prod_pay_sorted.head(nb_pays))


# Repartition des contenus par années ================================
with col2 : 
    st.markdown("#### Répartition du contenus par années de production")
    nb_years = st.number_input("Entrez un nombre pour voir la liste de la repartition de contenu par année.", min_value=5, max_value=99)
    st.markdown("""
    Entrez un nombre pour voir le classement des années basé sur la repartition du contenus.  
    Entrez 99 pour voir l'entièreté du classement.""")
    if nb_pays == 99 : 
        st.dataframe(repartition_prod_year_sorted)
    else :
        st.dataframe(repartition_prod_year_sorted.head(nb_years))

st.markdown("""
    Ainsi nous prenons connaissances du nombre de films, de séries, et du nombre total de production,
    Qui se poursuie avec la visualisation de la répartition des contenus produits par pays et par année de production et leur classement.
""")


# Repartition du contenu par genre =================================
st.markdown("#### Répartition du contenus par genre")

with st.expander("Découvrez le code") : 
    with st.echo() :
        # Analyse descriptive - Partie 3 : Répartition des productions par genre
        repartition_prod_genre = netflix.groupby(['main_genre']).count()['show_id'].reset_index()
        repartition_prod_genre_sorted = repartition_prod_genre.sort_values(by=['show_id'], ascending=False)

nb_genre = st.number_input("Entrez un nombre pour voir la liste de la repartition de contenu par genre.", min_value=5, max_value=99)

st.markdown("""
Entrez un nombre pour voir le classement des genres sur la repartition du contenus.
Entrez 99 pour voir l'entièreté du classement.""")
if nb_pays == 99 : 
    st.dataframe(repartition_prod_genre_sorted)
else :
    st.dataframe(repartition_prod_genre_sorted.head(nb_genre))


# ===========================================================================================================================
# Création d'une charte graphique
st.subheader("Création d'une charte graphique et d'un template pour les graphiques")
st.markdown("""
🎨 Charte Graphique (Inspiration Netflix)
##### 1. Couleurs
La charte définit une palette de couleurs de base composée de quatre teintes principales :

- Rouge Netflix (un rouge vif : #E50914)  
- Noir Netflix (un noir profond : #221f1f)  
- Gris Clair (#B3B3B3)  
- Gris Foncé (#4D4D4D)  

À partir de celles-ci, des palettes spécifiques sont créées :

- Palette Principale : Conçue pour les graphiques simples (comme un top 10), elle utilise un dégradé allant du gris clair au gris foncé, puis au noir et enfin au rouge Netflix.  
- Palette Binaire : Utilisée pour les comparaisons "Movie" vs "TV Show". Les "Movies" sont représentés en Rouge Netflix, et les "TV Shows" en gris foncé.

Palette Heatmap : Pour les cartes de chaleur, une palette de couleurs (cmap) est définie, allant du blanc au Rouge Netflix.

##### 2. Style Global des Graphiques
Le thème général (appliqué via Seaborn) est défini pour assurer la cohérence de tous les graphiques :

- Fond : Un style "whitegrid" est utilisé, fournissant un fond blanc avec de légères lignes de grille.  
- Police : La police préférée est "Arial" (ou une police "sans-serif" par défaut) pour sa grande lisibilité.

Les paramètres typographiques des graphiques sont finement ajustés :

- Titres des graphiques : Ils sont affichés en gras, en taille 18, et utilisent la couleur Noir Netflix.  
- Étiquettes des axes (X et Y) : Elles sont en gras, en taille 14, et de couleur gris foncé.  
- Valeurs sur les axes (ticks) : Les chiffres indiquant les valeurs sur les axes sont également de couleur gris foncé.
""")

st.info("Charte graphique fait avec Gemini", icon="ℹ️")

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

# ==========================================================================================================================
# Premier graphe : countplot() ======================================================
st.divider()
st.subheader("Gaphe 1 : Comparaison films VS séries avec un countplot")

with st.expander("Découvrez le code") : 
    with st.echo() : 
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

# Affichage du graphe
st.pyplot(fig)

st.markdown("""
    Commme vu précédemment lors de l'analyse descriptive, le diagramme `countplot` nous donne les mêmes resultats du nombres de films et de séries.
    A raison de 6131 films contre 2676 pour les séries. Cependant Pourquoi y'a t'il plus de films que de séries sur le catalogue netflix ?  
    Cette asymétrie s'explique historiquement par la stratégie de Netflix :

    1.**Coûts de Licence** : Il était plus rentable d'acquérir les droits d'un grand nombre de films existants pour construire rapidement un catalogue volumineux.  
    2.**Modèle de "Longue Traîne (Long Tail)"** : Un large inventaire de films permet de satisfaire des goûts de niche et d'attirer une base d'utilisateurs plus large.  
    3.**Coûts de Production** : Les séries, en particulier les productions originales, représentent un investissement beaucoup plus lourd et à plus long terme (coût par épisode, engagement sur plusieurs saisons) que la plupart des films."
""")


# Deuxieme Graphe : barplot() ==============================================
st.write("")
st.write("")
st.subheader("Gaphe 2 : Top 10 des pays producteurs avec barplot")

nb_top10_countries = st.number_input("Entrez un nombre pour modifier le graphe", min_value=5, value=10, max_value=15)

with st.expander("Découvrez le code") : 
    with st.echo() :
        # Préparation des données (Top 10)
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

# Affichage du graphique
st.pyplot(fig)

st.markdown("""
    Le graphique `barplot` illustre une **domination écrasante des États-Unis** en tant que principal pays producteur de contenu sur Netflix.

    Cette hégémonie s'explique par plusieurs facteurs :

    1.  **Héritage Historique :** Les États-Unis, avec des institutions comme Hollywood, sont les pionniers de l'industrie cinématographique mondiale. Ils disposent du catalogue historique le plus vaste et de la plus grande capacité de production.  
    2.  **Origine de Netflix :** Netflix étant une entreprise américaine, son marché domestique initial a été logiquement construit autour du contenu américain.  
    3.  **Influence Culturelle :** Le contenu américain (en langue anglaise) bénéficie d'une force d'exportation culturelle majeure, le rendant populaire et facilement distribuable à l'échelle mondiale.  

    Bien que Netflix investisse de plus en plus dans des productions locales (Corée du Sud, Espagne, Inde...), son catalogue de base reste profondément ancré dans l'immense bibliothèque de contenu américaine.
""")

# Troisième Graphe : histplot() ==============================================
st.write("")
st.write("")
st.subheader("Gaphe 3 : Distribution des productions en fonctions des années de sortie avec un histplot")

nb_bins = st.number_input("Faites varier le nombre de bins", min_value=20, value=50, max_value=100)

with st.expander("Découvrez le code") : 
    with st.echo() :
        fig, ax = plt.subplots()

        sns.histplot(
            data=netflix,
            x='release_year',
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

# Affichage du graphe
st.pyplot(fig)

st.markdown("""
L'histogramme `histplot` montre la distribution des contenus Netflix en fonction de leur année de sortie.

**1. Le Constat : Une forte concentration sur le contenu récent**

Le graphique est fortement **asymétrique à gauche** (*left-skewed*). On observe deux choses :
* **Le Pic :** La grande majorité des films et séries disponibles ont été produits au cours des 5 à 10 dernières années, avec un pic très net sur les années les plus récentes (ex: 2017-2021).  
* **La Traîne :** Une longue "traîne" s'étend vers la gauche, indiquant que, bien que des contenus plus anciens (des années 80, 90 ou 2000) soient présents, ils sont beaucoup moins nombreux.  

**2. L'Analyse : Une stratégie axée sur la "fraîcheur"**

Cette distribution n'est pas un hasard, elle reflète directement la stratégie commerciale de Netflix :

* **Focus sur la Nouveauté :** L'argument marketing principal de Netflix est le contenu "frais", nouveau et original. C'est essentiel pour acquérir de nouveaux abonnés et retenir les clients existants.  
* **L'Ère du Streaming :** L'augmentation exponentielle des titres récents coïncide avec l'investissement massif de Netflix dans la production de contenu original (à partir de 2015-2016) pour concurrencer les studios traditionnels.  
* **Gestion des Licences :** Le contenu plus ancien est souvent acquis via des licences temporaires et coûteuses. Netflix préfère investir dans des contenus qu'il possède (les "Originals").  

**Conclusion :** Ce graphique illustre que le modèle économique de Netflix est basé sur un renouvellement constant, se positionnant comme une plateforme de nouveautés plutôt que comme une archive du cinéma.
""")

# Quatrième Graphe : heatmap() ==============================================
st.write("")
st.write("")
st.subheader("Gaphe 4 : Matrice de corrélation avec un heatmap")

with st.expander("Découvrez le code") : 
    with st.echo() :
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

# Affichage du graphe
st.pyplot(fig)

st.markdown("""
    Cette matrice de corrélation `heatmap` nous permet de quantifier les relations linéaires entre les différentes variables numériques de notre dataset.

    Les scores vont de +1 (corrélation positive parfaite, en rouge) à -1 (corrélation négative parfaite).

    **1. L'Aperçu Stratégique Clé : `release_year` vs `lag_time`**

    * **Constat :** Nous observons une **corrélation négative forte** (score d'environ -0.6 à -0.8) entre l'année de sortie (`release_year`) et le délai d'ajout (`lag_time`).  
    * **Analyse :** C'est l'enseignement le plus important. Cela signifie que **plus un contenu est récent, plus son délai d'ajout sur Netflix est faible**. C'est la confirmation statistique de la stratégie "Netflix Originals" : en produisant son propre contenu, Netflix le diffuse quasi-instantanément (`lag_time` proche de 0), contrairement aux contenus sous licence (plus anciens) pour lesquels il fallait attendre la fin des droits de diffusion.  

    **2. Validation des Données : `duration_min` vs `duration_seasons`**

    * **Constat :** Une corrélation négative très forte (proche de -1) existe entre la durée en minutes et la durée en saisons.  
    * **Analyse :** C'est une validation de la cohérence de nos données. Ces deux variables **s'excluent mutuellement** : un titre est soit un film (une valeur dans `duration_min`), soit une série (une valeur dans `duration_seasons`), mais jamais les deux.  

    **3. Autres Observations**

    * **`release_year` vs `year_added` (Positive Forte) :** Cette corrélation positive élevée est intuitive. Elle confirme que le contenu ajouté récemment (`year_added`) sur la plateforme est aussi, en général, du contenu produit récemment (`release_year`).  
    * **Absence de Corrélation (`month_added`) :** La variable `month_added` ne montre aucune corrélation significative avec les autres. C'est attendu : le mois d'ajout (Janvier vs Juillet) est une donnée cyclique qui n'a pas de lien linéaire avec l'année de production ou la durée d'un titre.  

    **Conclusion :**
    Cette matrice valide la structure de nos données (films vs séries) et, plus important encore, elle fournit une preuve quantitative de l'évolution stratégique de Netflix vers la production et la diffusion immédiate de son propre contenu.
""")

# Cinquième Graphe : boxplot() ==============================================
st.write("")
st.write("")
st.subheader("Gaphe 5 : Durée moyenne selon le type de contenu  avec un boxplot")

with st.expander("Découvrez le code") : 
    with st.echo() :

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

col3, col4 = st.columns(2)

# Affichage de nos boxplots
with col3 :
    # Affichage graphe de la Durée des films
    st.pyplot(fig1)
with col4 : 
    # Affichage graphe de la Durée des séries
    st.pyplot(fig2)

st.markdown("""
    L'analyse de la durée des contenus via des boxplots révèle deux stratégies de catalogue distinctes pour les films et les séries TV.
    Le boxplot des films montre la répartition de leur durée en minutes.
            
    #### 1. Distribution de la Durée des Films

    **Observations (Le Constat) :**

    * **Format Standard :** La boîte centrale (l'écart interquartile) montre que 50% des films du catalogue se situent dans le format standard de l'industrie, **autour de 90 à 110 minutes**.
    * **Médiane :** La durée médiane (la plus typique) se trouve également dans cet intervalle.
    * **Outliers (Points Isolés) :** De nombreux points sont visibles en dehors des moustaches, indiquant une grande variété de formats.

    **Interprétation (L'Analyse) :**

    Cette concentration confirme que **Netflix respecte les standards de l'industrie cinématographique**. Les outliers ne sont pas des erreurs mais illustrent la **diversité du catalogue** :

    * **À gauche (> 150 min) :** Présence de films d'auteur, épopées historiques ou versions longues (ex: *The Irishman*).
    * **À droite (< 60 min) :** Présence de documentaires courts, comédies spéciales (stand-up) et programmes jeunesse.

    Pour les films, Netflix agit donc en **distributeur classique**, couvrant le format standard tout en assurant la diversité avec des formats de niche.

    #### 2. Distribution du Nombre de Saisons (Séries TV)

    Le boxplot des séries TV est l'indicateur le plus révélateur de la stratégie de production.

    **Observations (Le Constat) :**

    * **Forte Asymétrie :** Le graphique est extrêmement asymétrique, écrasé vers la gauche.
    * **Médiane à 1 Saison :** Le point crucial est la **médiane située à 1**. Cela signifie que **50% de toutes les séries du catalogue n'ont jamais dépassé leur première saison**.
    * **Outliers Rares :** Les séries à succès (4, 5, 10 saisons ou plus) sont si rares qu'elles apparaissent toutes comme des points isolés (outliers).

    **Interprétation (L'Analyse) :**

    Cet enseignement est majeur : le catalogue de séries est dominé par des **mini-séries** ou des **séries annulées prématurément**.

    1.  **Le "Cimetière Netflix" :** La médiane à 1 saison illustre la stratégie de Netflix d'annuler rapidement les séries qui n'atteignent pas leurs objectifs d'audience.
    2.  **La Montée des Mini-séries :** Ce chiffre s'explique aussi par la popularité croissante des "Limited Series" (ex: *Le Jeu de la Dame*), un format narratif complet, moins risqué et moins coûteux qu'une série sur plusieurs années.
    3.  **Les "Hits" sont l'Exception :** Le modèle économique est clair : lancer un grand nombre de séries pour en trouver quelques-unes (les outliers) qui deviendront des succès mondiaux (ex: *Stranger Things*, *The Crown*).

    Pour les séries, Netflix agit donc en **investisseur à haut risque** : il finance un grand nombre de "pilotes" (Saison 1), accepte qu'une majorité échoue (médiane à 1), afin de trouver les quelques "hits" qui fidéliseront les abonnés.

""")

# ===============================================================================================================
# Questions analyses Netflix
st.write("")
st.write("")
st.subheader("Domination géographique") # =====================================
st.markdown("""
    **Question** :  Quels pays dominent la production
    Netflix ? Identifier les principaux
    producteurs de contenu et leur
    contribution relative au catalogue
    global.
""")

with st.expander("Découvrez le code") : 
    with st.echo() : 
        # Domination géographique
        nbr_total_production = netflix['show_id'].count()
        repartition_prod_pay_sorted['contribution_pays_%'] = repartition_prod_pay_sorted['show_id'] * 100 / nbr_total_production
    
nb_repartition_prod = st.number_input("Decouvrez la contribution d'autres pays", min_value=5, value=10, max_value=99)   
st.dataframe(repartition_prod_pay_sorted.head(nb_repartition_prod))

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