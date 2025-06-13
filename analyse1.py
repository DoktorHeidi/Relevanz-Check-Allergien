def app():
    
    import streamlit as st
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.express as px
    st.title("Analyse der Krankenkassendaten aus den pdf-Dateien.")
    # 📁 CSV-Datei laden
    csv_file = "pdf_csv_daten/Krankenkassen_alle_Zahlen_okay_plus-Kategorie.csv"
    df_KK_alle = pd.read_csv(csv_file) # df_KK (= dataframe_KrankenKassen)
    df_KK = df_KK_alle.drop(columns=["freiwillig"])

    st.title("🔍 Analyse 1")

    
    #st.markdown("Interaktive Analyse der Arbeitsunfähigkeits-Fallzahlen nach Kategorie des Diagnoseschlüssels.")
    #st.markdown('<p style="font-size:30px;">Interaktive Analyse der Arbeitsunfähigkeits-Fallzahlen nach Kategorie des Diagnoseschlüssels.</p>', unsafe_allow_html=True)

    # 🎚️ **Filter für ICD-Kategorien**
    icd_filter = st.selectbox("Wähle eine ICD-Kategorie", df_KK["ICD_Kategorie"].unique())

    # 🔍 **Gefilterte Korrelationsmatrix**
    df_filtered = df_KK[df_KK["ICD_Kategorie"] == icd_filter]
    df_numeric_filtered = df_filtered.select_dtypes(include=['number'])
    corr_matrix_filtered = df_numeric_filtered.corr()

    st.subheader(f"📊 Korrelationen zwischen Variablen für {icd_filter}")


    col1, col2, col3 = st.columns([1, 4, 2])  # Mittelspalte größer, Seiten kleiner
    with col2:  # Diagramm in der mittleren Spalte
        fig, ax = plt.subplots(figsize=(4, 3))  # Kleinere Größe
        sns.heatmap(corr_matrix_filtered, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 5}, ax=ax)
        st.pyplot(fig)


    ############ erster Barplot #################################################################################
    # 📊 **Histogramm für Pflichtversicherte**
    st.subheader("📊 Histogramm der Fälle nach Jahr und Geschlecht (männlich (male=1) oder weiblich (male=0))\nPflichtversicherte mit Rentnern")


    col1, col2, col3 = st.columns([2, 4, 2])  # Mittelspalte größer, Seiten kleiner
    with col2:  # Diagramm in der mittleren Spalte
        sns.reset_defaults()
        df_filtered_1 = df_KK.loc[(df_KK["Pflicht_alle"] == 1)]
        fig_hist, ax_hist = plt.subplots(figsize=(3, 2)) #, dpi=70)verändert nichts
        sns.histplot(data=df_filtered_1, x='Jahr', weights='Faelle', hue='male', multiple='dodge',binwidth=1, ax=ax_hist)


        ax_hist.set_xlabel("Jahr", fontsize=9)
        ax_hist.set_ylabel("Anzahl der Fälle", fontsize=9)
        ax.legend(fontsize=7)  # Ändert die Schriftgröße der Legende leider nicht
        #legend = ax_hist.legend(fontsize=7)

        ax_hist.tick_params(axis='x', labelsize=8, pad=2)  # X-Achse
        ax_hist.tick_params(axis='y', labelsize=8, pad=2)  # Y-Achse

        #ax_hist.set_title("Histogramm der Fälle nach Jahr und Geschlecht\nPflichtversicherte mit Rentnern", fontsize=8)
        st.pyplot(fig_hist)

        
    '''
        # 📊 **Histogramm für Pflichtversicherte**
        st.subheader("📊 Histogramm der Fälle nach Jahr & Geschlecht")
        df_filtered_1 = df_KK.loc[(df_KK["Pflicht_alle"] == 1)]
        fig_hist, ax_hist = plt.subplots(figsize=(3, 2), dpi=100)
        sns.histplot(data=df_filtered_1, x='Jahr', weights='Faelle', hue='male', multiple='dodge', binwidth=1, ax=ax_hist)
        ax_hist.set_xlabel("Jahr")
        ax_hist.set_ylabel("Anzahl der Fälle")
        ax_hist.set_title("Histogramm der Fälle nach Jahr und Geschlecht\n nur Angaben von Pflichtversicherten mit Rentnern")
        st.pyplot(fig_hist)

    '''

    ########## zweiter und dritter Barplot (diesmal mit allen Daten ohne Filter #######################)

    # 🏗️ **Zwei Histogramme nebeneinander**
    st.subheader("📊 Anzahl Fälle vs. Tage pro Fall nach Jahr und Geschlecht (männlich (male=1) oder weiblich (male=0))\naus allen Angaben")

    fig_hist2, axes_hist2 = plt.subplots(1, 2, figsize=(12, 4))

    ###### zweiter ######################
    sns.histplot(data=df_KK, x="Jahr", weights="Faelle", hue="male", multiple="dodge", binwidth=1, ax=axes_hist2[0])
    axes_hist2[0].set_title("Fälle")

    ###### dritter ######################
    sns.histplot(data=df_KK, x="Jahr", weights="Tage_je_Fall", hue="male", multiple="dodge", binwidth=1, ax=axes_hist2[1])
    axes_hist2[1].set_title("Tage je Fall")
    st.pyplot(fig_hist2)

    st.markdown(" ")  # Fügt eine Leerzeile für mehr Abstand hinzu
    ###### scatterplot #######################################################################

    # 📑 **ICD-Kategorie Scatter-Plot**
    st.subheader("📊 Interaktiver Scatter-Plot mit ICD-Kategorie\nversetzt dargestellt:\nOhne Krankenhausaufenthalt (= 0; Jahre: 2011-2017) und mit (=1; Jahre: 2012-2020)")

       # Textbereich mit Beschreibung
    st.text_area("Beschreibung und Schlussfolgerung", "Dargestellt ist nachfolgend die Anzahl der Fälle verschiedener Gruppen nach Jahr.\n"
             "Die Gruppen wurden aus den einzelnen Angaben zu den Jahren, ob mit Krankenhausaufenthalt (1) oder ohne (0), ob männlich (1) oder weiblich (0), "
             "ob Pflichtversichert mit (1) oder ohne Einbezug von Rentnern (0) gebildet.\n"
             "Die farbliche Markierung kennzeichnet die Diagnosestellung nach ICD-Schlüssel.\n\nAuffällig ist die Prävalenz der Atemwegserkrankungen, wobei durchgehend mehr Frauen als Männer betroffen sind."
             "Eine ebenfalls sehr häufige Diagnosestellung betrifft Skelett- und Muskelerkrankungen. Hier sind durchweg häufiger Männer als Frauen betroffen.\n"
    ,
             height=175)


    # Daten leicht versetzt
    df_KK["Jahr_offset"] = df_KK["Jahr"] + df_KK["Krankenhaus"] * 0.2  # Offset um 0.2 für Krankenhaus=1
    

    fig_icd = px.scatter(df_KK, x='Jahr_offset', y='Faelle', color='ICD_Kategorie',
                     hover_data={'ICD': True, 'Jahr_offset': False,'Jahr': True, 'Faelle': False, 'Krankenhaus': True, 'Pflicht_alle': True, 'male': True})

    # Legenden-Schriftgröße anpassen
    fig_icd.update_layout(
        legend=dict(font=dict(size=14))  # Ändert die Schriftgröße der Legende
    )

    # Punktgröße anpassen
    fig_icd.update_traces(marker=dict(size=10))  # Ändert die Punktgröße
    fig_icd.update_layout(height=600)  # Erhöht die Höhe des Plots
    st.plotly_chart(fig_icd)

    # 📑 **ICD-Kategorie Scatter-Plot**
    #st.subheader("📊 Interaktiver Scatter-Plot mit ICD-Kategorie")

    #fig_icd = px.scatter(df_KK, x='Jahr', y='Fälle', color='ICD_Kategorie',
    #                    hover_data={'ICD': True, 'Jahr': False, 'Faelle': False, 'Krankenhaus': True, 'Pflicht_alle': False})
    #st.plotly_chart(fig_icd)

