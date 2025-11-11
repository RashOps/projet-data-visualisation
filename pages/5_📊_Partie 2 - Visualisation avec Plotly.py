# Imporation des dépendances
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration de la page principale
st.set_page_config(
    page_title="Partie 2 - Visualisation avec Plotly",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state = "expanded"
)

st.sidebar.subheader("Visualisation des grpahes avec Plotly 📊")

# Chargement du dataframe
from data_loader import load_happiness_data_analysis
world_happiness_report = load_happiness_data_analysis()

# ===========================================================================================
st.title("Visualisation Plotly et Analyse descriptive")
st.subheader("Dataframe : World Happiness Report")
st.dataframe(world_happiness_report)

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

st.markdown("""
    #### 🎨 Charte Graphique (Plotly)

Pour garantir la cohérence visuelle de tous les graphiques interactifs (Partie 2), une charte graphique centralisée est définie.

##### 1. Palettes de Couleurs

Deux types de palettes sont définis pour s'adapter aux différents types de données :

* **Palettes Continues :** Pour les échelles numériques (comme le score de bonheur, le PIB, etc.), la palette **'Viridis'** est utilisée pour sa clarté et sa bonne perception des nuances.
* **Palettes Catégorielles :** Pour les données discrètes (comme les régions du monde), la palette **'Safe'** est choisie pour ses couleurs distinctes et accessibles.

##### 2. Thème (Template) Global

Un template de layout (`GLOBAL_TEMPLATE_LAYOUT`) est appliqué à tous les graphiques. Il est basé sur le thème `plotly_white` (fond blanc, grilles légères) et personnalisé comme suit :

* **Typographie :**
    * La police principale pour tous les textes est **"Arial"** (taille 12) en gris foncé (`#333333`), offrant un look moderne et plus doux que le noir pur.

* **Titre Principal :**
    * Le titre du graphique est **centré**, en **gras**, et d'une taille de **20pt** pour une hiérarchie claire.

* **Axes (X et Y) :**
    * Les titres des axes sont mis en avant en **gras** (taille 14pt).
    * Les grilles sont rendues très subtiles (couleur `#EAEAEA`) pour ne pas surcharger la visualisation.

* **Légende :**
    * Elle est placée **horizontalement au-dessus du graphique** (plutôt que sur le côté) pour maximiser l'espace horizontal de la visualisation.
    * Le titre de la légende est masqué pour éviter les informations redondantes.

* **Interactivité (Hover) :**
    * Le mode `hovermode='closest'` est activé pour que l'infobulle de l'élément le plus proche du curseur s'affiche, facilitant l'exploration.
    * Les infobulles elles-mêmes ont un fond blanc et une police Arial pour une lisibilité maximale.
""")

st.info("Charte graphique fait avec Gemini", icon="ℹ️")

# ==========================================================================================================================
st.write("")
st.write("")
st.divider() # =============================================================
st.subheader("Visualisation Interactive avec Plotly")
st.markdown("""##### Carte mondiale du score de bonheur avec gradients de couleur""")

# choropleth() : Carte mondiale du score de bonheur avec gradients de couleur

with st.expander("Découvrez le code") : 
    with st.echo() :
        # Echelle de coloration
        global_min_score = world_happiness_report['Score'].min() # Valeur min
        global_max_score = world_happiness_report['Score'].max() # Valeur max
        st.write(f"Échelle de score globale fixée de {global_min_score:.2f} à {global_max_score:.2f}")

        fig = px.choropleth(
            world_happiness_report,
            locations='Country',
            locationmode='country names', 

            color='Score', 

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

            title='Évolution du Score de Bonheur dans le Monde (2015-2019)'
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

st.plotly_chart(fig)

st.markdown("""
    ##### Analyse et Interprétation
    Ce graphique animé révèle la distribution géographique du bonheur et son évolution sur 5 ans.
    * Polarisation Géographique : L'observation la plus immédiate est la polarisation marquée du bonheur. L'Amérique du Nord, l'Europe de l'Ouest et l'Océanie affichent des scores élevés constants (couleurs vives/jaunes), tandis que l'Afrique subsaharienne et l'Asie du Sud montrent des scores structurellement bas (couleurs sombres/violettes).
    * Stabilité des Tendances : L'animation de 2015 à 2019 montre une inertie significative. Les pays "heureux" le restent, et les pays "malheureux" peinent à s'améliorer. Il n'y a pas de bouleversement majeur de la carte en 5 ans.
    * Micro-Tendances : Bien que la structure globale soit stable, l'animation permet de repérer des changements subtils. On peut observer certaines régions d'Europe de l'Est s'éclaircir légèrement, indiquant une amélioration progressive, tandis que des pays en situation de crise (comme le Venezuela, non visible sur ce dataset mais exemple typique) pourraient s'assombrir.

    Conclusion  
    Le bonheur mondial est géographiquement polarisé et très stable. Les facteurs structurels qui définissent un pays (richesse, institutions, culture) semblent avoir plus d'impact à long terme que les variations annuelles.
""")

st.write("")
st.write("") # =================================================================
st.markdown("""##### Nuage de points : Relation PIB <=> bonheur avec hover interactif""")

# Nuage des points scatter() : Relation PIB bonheur avec hover interactif

with st.expander("Découvrez le code") : 
    with st.echo() :
        # 2. Echelle de coloration des bornes globales des axes X et Y
        global_min_gdp = world_happiness_report['GDP_per_Capita'].min() * 0.9
        global_max_gdp = world_happiness_report['GDP_per_Capita'].max() * 1.05

        global_min_score = world_happiness_report['Score'].min() * 0.9
        global_max_score = world_happiness_report['Score'].max() * 1.05

        st.write(f"Axe X (PIB) fixé de {global_min_gdp:.2f} à {global_max_gdp:.2f}")
        st.write(f"Axe Y (Score) fixé de {global_min_score:.2f} à {global_max_score:.2f}")

        fig = px.scatter(
            world_happiness_report,

            x='GDP_per_Capita',
            y='Score',

            color='Region', 
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
st.markdown("""
    ##### Analyse et Interprétation
    Ce graphique animé est le cœur de notre analyse, montrant la relation entre la richesse (PIB) et le bonheur (Score).

    * Corrélation Forte et Positive : La tendance principale est indéniable : les points forment un nuage qui s'étire du bas-gauche vers le haut-droit. Cela confirme que les pays plus riches sont, en moyenne, significativement plus heureux.
    * Le Mouvement ("La Course") : En appuyant sur "Play", on observe que la majorité des "bulles" (pays) se déplacent lentement vers la droite (leur PIB augmente) et légèrement vers le haut (leur score de bonheur s'améliore). L'animation illustre une tendance globale à l'amélioration du bien-être et de la richesse sur cette période.
    * L'Importance des "Outliers" : Les pays les plus instructifs sont ceux qui dévient de la tendance principale :
    * Au-dessus de la ligne (ex: Amérique Latine) : Des pays comme le Costa Rica ou le Mexique affichent systématiquement un score de bonheur bien plus élevé que leur PIB ne le laisserait supposer. Cela prouve que des facteurs non économiques, comme le Social_Support (soutien social), sont des moteurs essentiels du bonheur.
    * En dessous de la ligne (ex: Asie de l'Est/Moyen-Orient) : Certains pays, bien que riches, affichent un score plus bas. Cela peut suggérer un impact négatif de la perception de la corruption (Trust_Government_Corruption) ou un manque de liberté (Freedom).

    Conclusion  
    L'argent contribue fortement au bonheur, mais il n'est pas le seul facteur. L'animation montre que si la croissance économique est une tendance de fond, la "qualité" du bonheur (être heureux sans être riche) dépend fortement du tissu social.
""")


st.write("")
st.write("") # =================================================================
st.markdown("""##### Évolution temporelle des pays pour les régions sélectionnées""")
st.markdown("""##### Corrélation entre indicateurs""")

# line() : evolution temporelle
with st.expander("Découvrez le code") : 
    with st.echo() :
        countries_to_plot = [
            'France', 
            'United States', 
            'China', 
            'India', 
            'Nigeria',
            'Brazil'
        ]

        # Filtrage du DataFrame pour les pays sélectionnés
        df_filtered = world_happiness_report[world_happiness_report['Country'].isin(countries_to_plot)]


        # Création du graphique 
        fig = px.line(
            df_filtered,  
            
            x='Year',           
            y='GDP_per_Capita', 
            
            color='Country',    
            markers=True,       
            
            hover_name='Country',
            title='Évolution du PIB par Habitant (2015-2019)',
            labels={
                'GDP_per_Capita': 'PIB par Habitant',
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

st.markdown("""
    ##### Analyse Détaillée : Évolution du PIB par Habitant (2015-2019)
    Graphique : px.line() avec x='Year', y='GDP_per_Capita', et color='Country'.

    ###### Objectif de la Visualisation
    Ce graphique est fondamental pour comprendre la dynamique de la richesse mondiale. En remplaçant l'animation (inutile ici) par un filtrage des pays (color='Country') et en plaçant le temps sur l'axe X (x='Year'), nous ne regardons plus un "instantané" statique, mais nous suivons les trajectoires économiques de pays spécifiques.

    ###### Interprétation des Niveaux (Clusters de Richesse)
    L'observation la plus immédiate est la stratification claire du monde en "clusters" de richesse, visible par la position verticale des lignes :
    1. Cluster à Haut Revenu : Les lignes des États-Unis et de la France se situent très haut sur le graphique. Elles partent d'un niveau de PIB par habitant déjà très élevé en 2015.
    2. Cluster Émergent / Moyen : Les lignes de la Chine et du Brésil se trouvent dans la partie médiane.
    3. Cluster à Faible Revenu / en Développement : Les lignes de l'Inde et du Nigeria sont positionnées en bas du graphique, indiquant un point de départ beaucoup plus bas.

    Conclusion (Niveaux)  
    Le graphique met en évidence l'énorme disparité de richesse absolue entre les nations développées et les nations en développement.

    ###### Interprétation des Tendances (Vitesse et Volatilité)
    La partie la plus importante de ce graphique n'est pas la position des lignes, mais leur pente (leur inclinaison) :

    * Croissance Mature (Pente Faible) : Les États-Unis et la France affichent des lignes relativement plates. Bien qu'ils soient riches, leur croissance annuelle du PIB par habitant est stable et mature, sans "explosion" visible sur cette période de 5 ans.
    * Croissance Rapide (Pente Forte) : La Chine et l'Inde montrent les pentes les plus raides. Bien qu'elles partent de plus bas, leur économie (en termes de PIB/habitant) croît visiblement plus vite que celle des pays riches. C'est l'illustration parfaite de la "croissance des marchés émergents".
    * Volatilité Économique : Le Brésil et le Nigeria, dont les économies sont souvent liées aux cycles des matières premières, peuvent présenter des lignes plus erratiques. On peut y observer des périodes de stagnation ou même de légers "creux", reflétant une instabilité économique que les autres pays du panel ne connaissent pas de la même manière.

    Conclusion (Tendances)  
    Le graphique raconte une histoire de convergence et de divergence. Alors que des pays comme la Chine et l'Inde convergent (rattrapent) rapidement, la volatilité reste un obstacle majeur pour d'autres (Brésil, Nigeria). Les pays riches, quant à eux, maintiennent leur avance grâce à une croissance plus lente mais stable.

    Synthèse Globale  
    Ce graphique linéaire est bien plus efficace qu'une animation pour cette analyse. Il transforme un "plat de spaghettis" (si nous n'avions pas filtré) ou une série d'images confuses (votre tentative avec animation_frame) en un récit comparatif clair. Il prouve que la "richesse" (un stock, la position de la ligne) et la "croissance" (un flux, la pente de la ligne) sont deux concepts distincts mais essentiels pour comprendre l'économie mondiale.
""")


st.write("")
st.write("") # =================================================================
st.markdown("""
    ##### Top 10 et flop 10 des pays 
    La construction du diagramme en barre du top 10 et flop 10 des pays en fonctions du PIB necessite une étape intermédiaire.  
    Et cette étape consiste à creer un nouveau dataframe qui regroupe le top 10 / flop 10 par année. Car en construisant nos graphes directement sur le dataframe de base,
    on fera un top / flop sans différence d'année, ce qui n'est pas notre objectif.
""")

st.markdown("""###### Préparation des données""")

st.markdown("""
    Le script suivant permettra de : 
             
    1. **Etape 1** : Creer un liste qui accueillira nos differents Top 10 de chaque année  
    2. **Etape 2** : En se basant sur notre dataframe orginel 'world_happiness_report', on cree un Top 10 par année en appliquant des filtres  
    3. **Etape 3** : Puis on crée un nouveau dataframe avec les differents Tops 10 par année à l'aide de la fonction `pd.concat()` de pandas.  
    3. **Etape 4** : On repette la même opération pour le flop 10, en remplacant `False` par `True` dans le paramètre 'ascending'
    
    Ensuite on utilisera notre nouveau dataframe "top_10_final" et "flop_10_final" pour construire notre graphique.
""")

with st.expander("Découvrez le code") : 
    with st.echo() :
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

st.write("")
st.markdown("""###### Création de nos grahiques : Top 10 et Flop 10""")

with st.expander("Découvrez le code") : 
    with st.echo() :
        # Top 10 ================================================================
        # Echelle des valeurs pour l'axe des abscisses
        max_gdp = top_10_final['GDP_per_Capita'].max() * 1.05 # 5% de marge
        min_gdp = 0 # Les barres commencent à 0

        fig_top = px.bar(
            top_10_final,
            x='GDP_per_Capita',
            y='Country',
            orientation='h',

            # Paramètres animations
            animation_frame='Year',
            animation_group='Country',

            color='Region',
            hover_name='Country',

            # Fixation de l'axe X
            range_x=[min_gdp, max_gdp],

            title='Top 10 des Pays par PIB par Habitant (2015-2019)',
            labels={
                'GDP_per_Capita':'PIB par habitants',
                'Country':'Pays'
            }
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
        max_gdp = flop_10_final['GDP_per_Capita'].max() * 1.05 # 5% de marge
        min_gdp = 0 # Les barres commencent à 0

        fig_flop = px.bar(
            flop_10_final,
            x='GDP_per_Capita',
            y='Country',
            orientation='h',

            # Paramètres animations
            animation_frame='Year',
            animation_group='Country',

            color='Region',
            hover_name='Country',

            # Fixation de l'axe X
            range_x=[min_gdp, max_gdp],

            title='Flop 10 des Pays par PIB par Habitant (2015-2019)',
            labels={
                'GDP_per_Capita':'PIB par habitants',
                'Country':'Pays'
            }
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

# Affichage du graphe du Top 10 
st.plotly_chart(fig_top)

# Affichage du graphe du Flop 10
st.plotly_chart(fig_flop)

st.markdown("""
    "Bar Chart Race" : Top 10 et Flop 10 du PIB  
    Graphique : px.bar() (horizontal) avec animation_frame='Year' et yaxis_categoryorder='total ascending'.

    ###### Analyse et Interprétation (Top 10)
    * Le Club des Riches : L'animation du "Top 10" est marquée par une extrême stabilité. Les mêmes pays (Luxembourg, Singapour, Suisse, Norvège, Qatar, etc.) dominent le classement chaque année.
    * Légers Ajustements : Le seul "mouvement" visible est un léger reclassement à l'intérieur de ce groupe d'élite (le #1 et le #2 peuvent échanger leur place), mais il n'y a quasiment jamais de nouvel entrant.

    Conclusion (Top 10)  
    La richesse extrême est une position très "collante" (sticky). L'animation démontre qu'il est incroyablement difficile pour une nouvelle nation de percer dans le groupe de tête des pays les plus riches à court terme.

    ###### Analyse et Interprétation (Flop 10)
    * Volatilité de la Pauvreté : À l'inverse total du Top 10, le "Flop 10" (les pays avec le PIB le plus bas) est caractérisé par une forte instabilité.
    * Entrées et Sorties Constantes : L'animation montre des pays qui entrent et sortent constamment du classement. Ces pays (ex: Burundi, R.A. Centrafricaine, Soudan du Sud) sont souvent sujets à des chocs externes extrêmes : guerres civiles, catastrophes naturelles, ou crises humanitaires.
    * La "Course" vers le bas : Un pays peut sembler s'améliorer (sortir du Flop 10) non pas parce que son économie s'est redressée, mais parce qu'un autre pays a subi un effondrement encore plus grave.

    Conclusion (Flop 10)  
    Le bas de l'échelle économique n'est pas un état stable, mais un état de crise permanente. L'animation montre que la pauvreté extrême est liée à une volatilité et une vulnérabilité immenses.
""")

st.write("")
st.write("") # =================================================================
st.markdown("""##### Corrélation entre indicateurs""")

# heatmap() Corrélation entre indicateurs

with st.expander("Découvrez le code") : 
    with st.echo() :
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
        # '%{z:.2f}' veut dire : "prends la valeur (z) et formate-la (f) avec 2 décimales"
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

st.markdown("""
    Matrice de Corrélation Statique (2015-2019)

    Graphique : px.imshow() (statique) sur la matrice de corrélation du DataFrame combiné.
    Analyse et Interprétation

    Cette heatmap nous donne la "formule mathématique" du bonheur en quantifiant la relation entre nos différentes variables sur l'ensemble de la période.
    * Les Moteurs du Bonheur : En regardant la ligne Score, les trois corrélations les plus fortes sont, de loin :
        1. GDP_per_Capita (ex: approximativement 0.78) : La richesse.
        2. Social_Support (ex: approximativement 0.75) : Le tissu social, la famille, les amis.
        2. Health_Life_Expectancy (ex: approximativement 0.76) : L'espérance de vie en bonne santé.

    * L'Importance de la Société : Des facteurs comme la Freedom (Liberté, approximativement 0.55) et la Trust_Government_Corruption (Confiance, approximativement 0.40) sont également des indicateurs positifs, mais dans une moindre mesure que le triptyque "Argent, Santé, Amis". La Generosity est, quant à elle, très faiblement corrélée.
    * Multicolinéarité : Le graphique révèle que les facteurs sont liés entre eux. Par exemple, le GDP_per_Capita et la Health_Life_Expectancy sont très fortement corrélés (case très rouge), ce qui est logique : les pays plus riches ont de meilleurs systèmes de santé.

    Conclusion  
    La heatmap confirme que le bonheur n'est pas une question d'argent uniquement. C'est un équilibre presque égal entre la richesse (PIB), la santé (Espérance de vie) et la communauté (Soutien social).
""")

st.write("")
st.write("")
st.divider() # =============================================================
st.subheader("Analyse finale : World Happiness")

st.markdown("""
    🎯 **Objectif**  
    Créer des visualisations de données dynamiques et interactives (avec **Plotly**) pour explorer le dataset *World Happiness Report*.  
    L'objectif est d'analyser les données sous différents angles, d'identifier les tendances et de comprendre les facteurs qui contribuent au bien-être mondial.

    ### 📂 Dataset  
    **World Happiness Report** (fichiers de 2015, 2016, 2017, 2018 et 2019).

    ### 🛠️ Préparation des Données : L'Harmonisation  

    #### Problème : Incohérence des schémas  
    Les 5 fichiers CSV (un par année) ne pouvaient pas être utilisés directement car leurs noms de colonnes différaient.  
    Exemple :  
    - 2015 : `Economy (GDP per Capita)`  
    - 2017 : `Economy..GDP.per.Capita.`  
    - 2019 : `GDP per capita`  

    #### Solution :  
    1. **Définition d'un Schéma Unifié** : Un "noyau commun" de colonnes pertinentes a été défini (ex: `Score`, `GDP_per_Capita`, `Social_Support`, etc.).  
    2. **Harmonisation** : Chaque fichier a été chargé, ses colonnes renommées pour correspondre au schéma unifié, et les colonnes superflues supprimées.  
    3. **Enrichissement** :  
    - Ajout d'une colonne `Year` à chaque fichier (ex: `df_2015['Year'] = 2015`).  
    - La colonne `Region` (manquante après 2017) a été rétro-ingéniérée à partir de 2016.  
    4. **Concaténation** : Les 5 DataFrames ont été empilés avec `pd.concat()`.  

    **Résultat :** Un unique DataFrame final (`df_final.csv`) de **782 lignes et 11 colonnes**, prêt pour l'analyse temporelle et interactive.

    ---

    ### 📊 Analyse Exploratoire et Visualisations

    #### 1. Quels sont les pays les plus heureux ?  
    **Graphique pertinent :** `px.bar()` (horizontal, Top 10 des pays 2019).  

    ##### Analyse et Interprétation  
    - **Domination Nordique** : Finlande, Danemark, Norvège, Islande, Suisse, Pays-Bas.  
    - **Équilibre, pas richesse extrême** : Les plus riches (Luxembourg, Singapour) ne sont pas forcément les plus heureux.  
    - **Formule du succès** : Richesse + Soutien social + Santé + Liberté + Faible corruption.  

    **Conclusion :** Le bonheur est un équilibre entre prospérité économique, solidarité sociale et confiance civique.

    ##### 2. Y a-t-il un lien entre le PIB et le Bonheur ?  
    **Graphique pertinent :** `px.scatter()` animé (x=`GDP_per_Capita`, y=`Score`).  

    ##### Analyse et Interprétation  
    - **Corrélation positive nette** : Les pays riches tendent à être plus heureux.  
    - **Rendements décroissants** : L'impact du PIB diminue après un certain seuil.  
    - **Outliers** :  
    - *Heureux mais pauvres* : Costa Rica, Mexique.  
    - *Riches mais moroses* : certains pays développés.  

    **Conclusion :** L'argent améliore le bonheur surtout jusqu'à la satisfaction des besoins essentiels. Ensuite, le lien s'affaiblit au profit du soutien social.

    ---

    #### 3. Comment les scores évoluent-ils dans le temps ?  
    **Graphiques pertinents :** `px.line()`, `px.choropleth()`, `px.bar()` animé.  

    ##### Analyse et Interprétation  
    - **Stabilité globale** : Peu de changements majeurs sur 5 ans.  
    - **Trajectoires contrastées** :  
    - Croissance lente : France, États-Unis.  
    - Croissance rapide : Chine, Inde.  
    - Volatilité : Brésil, Nigeria.  

    **Conclusion :** Le bonheur et la richesse évoluent lentement. La croissance économique soutenue reste la force la plus influente à moyen terme.

    ---

    #### 4. Quels facteurs influencent le plus le bonheur ?  
    **Graphique pertinent :** `px.imshow()` (heatmap de corrélation).  

    ##### Analyse et Interprétation  
    | Facteur | Corrélation (~) | Importance |
    |----------|----------------|-------------|
    | GDP_per_Capita | 0.78 | 💰 Richesse |
    | Health_Life_Expectancy | 0.76 | 🩺 Santé |
    | Social_Support | 0.75 | 🤝 Communauté |
    | Freedom | 0.55 | 🕊️ Liberté |
    | Trust_Government_Corruption | 0.40 | ⚖️ Confiance |
    | Generosity | 0.14 | 💡 Faible impact |

    **Conclusion :** Le bonheur repose sur un triptyque : **Argent**, **Santé**, **Communauté**.

    ---

    #### 5. Y a-t-il des "patterns" géographiques du bien-être ?  
    **Graphiques pertinents :** `px.choropleth()`, `px.scatter(color='Region')`.  

    ##### Analyse et Interprétation  
    - **Fracture Nord/Sud** : L'Europe de l'Ouest et l'Océanie sont en tête, l'Afrique subsaharienne en bas.  
    - **Clusters régionaux** :  
    - Europe de l'Ouest → Riche et heureuse.  
    - Afrique subsaharienne → Pauvre et malheureuse.  
    - Amérique Latine → Moyenne en PIB mais haute en bonheur.  
    - Asie de l'Est → Forte hétérogénéité.  

    **Conclusion :** Le bonheur a une composante culturelle et géographique. Le continent d'origine influence fortement le bien-être global.
""")