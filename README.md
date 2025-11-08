# Analyse de Données et Dashboard Streamlit : Netflix & World Happiness

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-blue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-blue?logo=plotly)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-darkblue?logo=seaborn)

Ce projet est un dashboard web interactif, construit avec **Streamlit**, qui présente une analyse de données complète de deux datasets distincts. Il a été réalisé dans le cadre d'un projet de data visualisation, démontrant des compétences en nettoyage de données, analyse exploratoire (EDA), et en création de visualisations statiques et interactives.

**L'une des particularités de ce projet est l'utilisation de Streamlit, un framework que j'ai appris spécifiquement pour transformer une analyse de données statique (type Jupyter Notebook) en une application web multi-pages dynamique et accessible.**

---

## 🚀 Aperçu du Dashboard

![dashboard_screenshot](./images/dashboard_screenshot.png)

---

## 🛠️ Stack Technique

Ce projet met en œuvre un pipeline de data analyse complet, de la donnée brute au dashboard web.

* **Langage :** Python
* **Analyse & Manipulation de Données :** Pandas
* **Visualisation de Données (Statique) :** Matplotlib & Seaborn
* **Visualisation de Données (Interactive) :** Plotly Express
* **Dashboarding & Application Web :** Streamlit

---

## 📂 Structure du Projet & Analyses

L'application est structurée en plusieurs pages, chacune se concentrant sur une étape clé du processus d'analyse.

### Partie 1 : Analyse du Catalogue Netflix (avec Seaborn)

Cette partie se concentre sur l'analyse exploratoire d'un dataset statique pour en tirer des conclusions claires, en utilisant **Seaborn** pour des visualisations statistiques.

* **Page 1 : Analyse Exploratoire (Netflix)**
    * Détaille le processus de **Data Cleaning** : gestion des valeurs nulles, transformation des types (`date_added`), et feature engineering (`main_country`, `main_genre`, `lag_time`).
    * Présente le dataframe nettoyé utilisé pour les visualisations.

* **Page 2 : Graphiques (Seaborn)**
    * **Distribution des Contenus :** `countplot` montrant la répartition Films vs. Séries.
    * **Analyse Géographique :** `barplot` du Top 10 des pays producteurs.
    * **Analyse Temporelle :** `histplot` de la distribution des années de sortie.
    * **Analyse de Durée :** `boxplot` comparant la durée des films (minutes) et des séries (saisons).
    * **Corrélations :** `heatmap` des variables numériques pour identifier les liens (ex: `lag_time` vs `release_year`).

### Partie 2 : Analyse du World Happiness Report (avec Plotly)

Cette partie démontre la capacité à gérer des données plus complexes (fichiers multiples) et à créer des visualisations **interactives** avec **Plotly**.

* **Page 3 : Harmonisation des Datasets**
    * Démontre un processus de **Data Cleaning avancé** en chargeant 5 fichiers CSV distincts (2015-2019).
    * **Harmonisation des Schémas :** Renommage et mappage des colonnes (ex: `Happiness Score` vs `Score`).
    * **Concaténation** finale en un seul dataset master propre.

* **Page 4 : Visualisation (Plotly)**
    * **Analyse Géographique :** `choropleth` (carte mondiale) interactive des scores de bonheur.
    * **Analyse des Facteurs :** `scatter` interactif pour explorer la relation entre le PIB et le score de bonheur.
    * **Évolution Temporelle :** `lineplot` pour suivre l'évolution des scores par région ou pays.
    * **Corrélations :** `heatmap` interactive des facteurs de bonheur (PIB, Santé, Liberté...).

---

## 🔧 Lancer le Projet Localement

Pour explorer l'application sur votre machine :

1.  **Clonez le dépôt :**
    ```bash
    git clone [https://github.com/RashOps/projet-data-visualisation.git](https://github.com/RashOps/projet-data-visualisation.git)
    cd VOTRE_PROJET
    ```

2.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancez l'application Streamlit :**
    ```bash
    streamlit run 1_Accueil.py
    ```