from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def app():
    from sklearn.impute import SimpleImputer
    import pandas as pd
    import numpy as np
    import streamlit as st    
    import matplotlib.pyplot as plt
    import plotly.express as px
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    
    #Funktion zur Bestimmung der optimalen Anzahl an Clustern
    def find_optimal_clusters(data, max_k=10):             ## werde ich hier nicht benutzen, da der Aufruf sehr lange dauert...
        # Elbow-Methode
        kmeans = KMeans(random_state=42)
        visualizer = KElbowVisualizer(kmeans, k=(2, max_k))
        visualizer.fit(data)
        optimal_k_elbow = visualizer.elbow_value_

        # Silhouetten-Score für Feintuning
        silhouette_scores = {}
        for k in range(2, max_k+1):
            kmeans = KMeans(n_clusters=k, random_state=40)
            labels = kmeans.fit_predict(data)
            silhouette_scores[k] = silhouette_score(data, labels)

        optimal_k_silhouette = max(silhouette_scores, key=silhouette_scores.get)

        # Endgültige Wahl basierend auf beiden Methoden
        optimal_k = optimal_k_silhouette if silhouette_scores[optimal_k_silhouette] > silhouette_scores.get(optimal_k_elbow, 0) else optimal_k_elbow
        return optimal_k, silhouette_scores
    



    st.header("Analyse der Krankenkassendaten:")
    
    # CSV-Datei laden
    csv_file = "pdf_csv_daten/Krankenkassen_alle_Zahlen_okay_plus-Kategorie.csv"
    df = pd.read_csv(csv_file)

    # Fehlende Werte mit Median ersetzen eigentlich hier unnötig, weil die Daten vollständig sein müssten ..bis auf einen Wert in Tage_je_Fall (weil nur 2 Fälle).
    imputer = SimpleImputer(strategy="median")
    df_imputed = df.copy()
    df_imputed[["Faelle","Tage_je_Fall", "Pflicht_alle"]] = imputer.fit_transform(df[["Faelle","Tage_je_Fall", "Pflicht_alle"]])

    # Daten normalisieren -  
        ## die Werte innerhalb einer Spalte werden auf eine vergleichbare Skala gebracht, sodass die Spalten leichter miteinander verglichen werden können
         
    scaler = StandardScaler()
    df_scaled = df_imputed.copy()
    df_scaled[["Faelle","Tage_je_Fall", "Pflicht_alle"]] = scaler.fit_transform(df_imputed[["Faelle","Tage_je_Fall", "Pflicht_alle"]])

    

    ########################################################################################
    '''
    ########## Dauert mehrere Minuten, vermutlich weil der Datensatz zu groß ist ###########


    # Berechnung der optimalen Anzahl an Clustern
    optimal_k, silhouette_scores = find_optimal_clusters(df_scaled[['Faelle', 'Tage', 'Tage_je_Fall', 'Pflicht_alle', 'freiwillig', 'male']])

        
    # Visualisierung der Silhouetten-Scores
    plt.figure(figsize=(6, 3))
    plt.plot(list(silhouette_scores.keys()), list(silhouette_scores.values()), marker='o', linestyle='-')
    plt.xlabel("Anzahl der Cluster")
    plt.ylabel("Silhouetten-Score")
    plt.title("Silhouetten-Score für verschiedene Clustergrößen")
    plt.grid()
    plt.show()

    # Visualisierung aller getesteten Clustergrößen als kleine Subplots
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))  # Anpassung der Größe für kompakte Darstellung
    axes = axes.flatten()

    for i, k in enumerate(range(2, 11)):  # Zeige Clustergrößen von 2 bis 10
        kmeans = KMeans(n_clusters=k, random_state=40)
        df_scaled.loc[:, 'Cluster'] = kmeans.fit_predict(df_scaled[['Faelle', 'Tage', 'Tage_je_Fall', 'Pflicht_alle', 'freiwillig', 'male']])
        
        axes[i].scatter(df_scaled.iloc[:, 0], df_scaled.iloc[:, 1], c=df_scaled['Cluster'], cmap='viridis', alpha=0.5)
        axes[i].set_title(f'K={k}')
        axes[i].set_xlabel("Feature 1")
        axes[i].set_ylabel("Feature 2")

    plt.tight_layout()
    st.pyplot(fig)

    ########################################################################################
    '''

    ##########################################################################
    # Daten fertig für Machine Learning mit KMeans 🤖
    ##########################################################################
    st.subheader("🤖 Mustererkennung mit **K-Means Clustering**\n")
   # Textbereich mit Beschreibung
    st.text_area("Beschreibung:", "Dargestellt sind hier zweimal die Dauer der Arbeitsunfähigkeit pro Fall gegen die Fallzahlen verschiedener Gruppen.\n"
             "Die Gruppen wurden aus den einzelnen Angaben zu den Jahren, ob mit Krankenhausaufenthalt (1) oder ohne (0), ob männlich (1) oder weiblich (0), "
             "ob Pflichtversichert mit (1) oder ohne Einbezug von Rentnern (0) gebildet.\n"
             "Die farbliche Markierung kennzeichnet in der ersten Darstellung die Diagnosestellung nach ICD-Schlüssel (A).\n"
             "In der zweiten Darstellung richtet sich die farbliche Unterscheidung nach der Clusterzuordnung nach Training des unsupervised Machine Learningmodells kMeans (B).",
             height=175)


    st.markdown("""
        <style>
        div[data-testid="stSlider"] {
            background-color: #F0F0F0 !important;  /* Grauer Hintergrund  #F0F0F0 oder #E5E5E5.*/
            color: red !important;
            padding: 8px;  /* Abstand für bessere Sichtbarkeit */
            border-radius: 10px;  /* Abgerundete Ecken */
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Slider: 
    # Interaktive Auswahl für Anzahl der Cluster, die das Modell finden soll
    anzahl_clusters = st.slider("Wähle Anzahl der Cluster für K-Means", min_value=2, max_value=10, value=3)

    # Training des Modells mit über den slider gewählten Anzahl der Cluster
    kmeans = KMeans(n_clusters = anzahl_clusters, random_state = 42)  
    df_scaled["Cluster"] = kmeans.fit_predict(df_scaled[['Faelle', 'Tage', 'Tage_je_Fall', 'Pflicht_alle', 'freiwillig', 'male']])

    # Visualisierung mit ICD-Kategorie (A)
    st.write("**A - Diagnosen**")
    fig_icd_kategorie = px.scatter(df_scaled, x="Tage_je_Fall", y="Faelle", color="ICD_Kategorie",
                             hover_data={'ICD': True, 'Cluster': True,'Jahr': False, 'Faelle': False, 'Krankenhaus': True, 'Pflicht_alle': False},
                                #title="📊 Musteranalyse nach ICD-Kategorie",
                                labels={"Tage_je_Fall": "Tage pro Fall", "Faelle": "Fallzahlen"})
    st.plotly_chart(fig_icd_kategorie)

    ############# 2. Fig  ##########################

    st.text_area("", "Es fällt auf, dass die meisten Fälle Diagnosen des Atmungssystems hatten. Diese hatten eine vergleichsweise kurze Krankheitsdauer.",
             height=100)



    # Visualisierung mit Farbe für Cluster (B)
    st.write("**B - Cluster**")
    fig_cluster = px.scatter(df_scaled, x="Tage_je_Fall", y="Faelle", color=df_scaled["Cluster"].astype(str), 
                             hover_data={'ICD': True, 'Cluster': True, 'Jahr': False, 'Faelle': False, 'Krankenhaus': True, 'Pflicht_alle': False},
                            #title="🤖 Mustererkennung mit K-Means Clustering",
                            labels={"Tage_je_Fall": "Tage pro Fall (normalisiert)", "Faelle": "Fallzahlen (normalisiert)"})
    st.plotly_chart(fig_cluster)



    '''
    # Visualisierung mit ICD-Kategorie (A)
    st.write("**A - Diagnosen**")
    fig_icd_kategorie = px.scatter(df_scaled, x="Tage_je_Fall", y="Faelle", color="ICD_Kategorie",
                             hover_data={'ICD': True, 'Cluster': True,'Jahr': False, 'Faelle': False, 'Krankenhaus': True, 'Pflicht_alle': False},
                                #title="📊 Musteranalyse nach ICD-Kategorie",
                                labels={"Tage_je_Fall": "Tage pro Fall (normalisiert)", "Faelle": "Fallzahlen (normalisiert)"})
    st.plotly_chart(fig_icd_kategorie)
    '''
    ############## Tabelle ############################################
    # 🎚️ **Filter für ICD-Kategorien**


    st.subheader(f"📊 Detaillierte normalisierte Daten der ICD-Kategorie")#{icd_filter}
    st.markdown("""
    <style>
    div[data-testid="stWidgetLabel"] {
        color: red !important;  /* Ändert die Schriftfarbe */
        font-weight: bold !important;  /* Macht den Text fett */
    }
    </style>
    """, unsafe_allow_html=True)

    icd_filter = st.selectbox("Wähle eine ICD-Kategorie", df_scaled["ICD_Kategorie"].unique())

    # 🔍 **Gefilterte Korrelationsmatrix**
    df_scaled_filtered = df_scaled[df_scaled["ICD_Kategorie"] == icd_filter]
    #df_numeric_filtered = df_scaled_filtered.select_dtypes(include=['number'])
    

    # Tabellenansicht der Daten    
    st.dataframe(df_scaled_filtered)

