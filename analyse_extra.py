import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import seaborn as sns
import matplotlib.pyplot as plt


def app():
    st.title("Analyse der Krankenkassendaten:")


    # 📁 CSV-Datei laden
    csv_file = "pdf_csv_daten/Krankenkassen_alle_Zahlen_okay_plus-Kategorie.csv"
    df = pd.read_csv(csv_file)


    # Einteilung in  Gruppen
    df["Gruppe"] = df.groupby(["Jahr", "Pflicht_alle", "freiwillig", "Krankenhaus", "male"]).ngroup()
    
    ## ICD-Werte in Spalten schreiben für Faelle, um die Korrelation der ICD miteinander zu ermöglichen
    df_icd_faelle = df.groupby(["Gruppe", "ICD"])["Faelle"].sum().unstack(fill_value=0).reset_index()   

    # dataframe df_groups erstellen, um Gruppendetails mit Gruppennummer zu speichern
    df_groups = df[["Gruppe", "Jahr", "Pflicht_alle", "freiwillig", "Krankenhaus", "male"]].drop_duplicates()

    # Gruppendetails aus df_groups wieder hinzufügen (durch left join on Gruppe)
    df_faelle = df_icd_faelle.merge(df_groups, on="Gruppe", how="left")

    # Erstellung einer überschaubaren Korrelationsmatrix. 
    # Hierzu Auwahl interessanter Diagnose-Schlüssel, die möglicherweise in einem Zusammenhang stehen.
    icd_allergie = [
        "J30",  # Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub)
        "L20",  # Atopische Dermatitis (Neurodermitis)
        "T78",  # Sonstige nicht näher bezeichnete allergische Reaktionen
        "J45",  # Asthma bronchiale (häufig allergisch bedingt)
        "K52",  # Allergische Erkrankungen des Verdauungstrakts
        "L23"   # Allergische Kontaktdermatitis
                #"Z91"   # Weitere persönliche Allergie-Anamnesen nicht im Datensatz
                # "Z88",  # Arzneimittelallergien in der Anamnese nicht im Datensatz
        ]
    icd_rheuma = [
            "M79",  # Rheumatismus, nicht näher bezeichnet
            "M06",  # Chronische Polyarthritis (inkl. rheumatoide Arthritis)
            "M12",  # Sonstige arthritische Erkrankungen, oft entzündlich
            "L40",  # Psoriasis-Arthropathie (entzündliches Rheuma durch Schuppenflechte)
            "L93",  # Lupus erythematodes (entzündliche Autoimmunerkrankung)
            "L94"  # Sonstige kollagene Erkrankungen (z. B. Sklerodermie)
        ]
    icd_herz = [
            "I10",  # Essenzielle Hypertonie (Bluthochdruck)
            "I20",  # Angina pectoris
            "I21",  # Akuter Myokardinfarkt (Herzinfarkt)
            "I25",  # Chronische ischämische Herzkrankheit
            "I50",  # Herzinsuffizienz (Herzschwäche)
            "I63",  # Hirninfarkt (Schlaganfall)
            "I70"   # Arteriosklerose (Gefäßverkalkung)
        ]
    icd_atem = [    
            "J20",  # Akute Bronchitis
            "J22",  # Akute Infektion der unteren Atemwege
            "J40",  # Bronchitis, nicht näher bezeichnet
            "J44"   # Chronisch obstruktive Lungenerkrankung (COPD)     
        ] 
        # nicht passend:
        #   "J09",  # Grippe durch nachgewiesene Vogelgrippe-Viren
        #   "J10",  # Grippe durch sonstige #Influenzaviren
        #   "J12",  # Viruspneumonie
        #   "J15",  # Bakterielle Pneumonie
        #   "J18",  # Pneumonie, Erreger nicht näher bezeichnet
        #   "J47",  # Bronchiektasen, 
        #   "J60",  # Pneumokoniose durch Kohlenstaub #   
        #   "J70",  # Lungenerkrankungen durch äußere Einflüsse

    # Alle ICD-Listen in einer einzigen Liste zusammenführen
    icd_gesamt = icd_allergie + icd_rheuma + icd_herz + icd_atem

    # Zusätzlich ein eigener dataframe, der die ICD-Schlüssel den Diagnosen zuordnet,
    # um bei der Visualisierung darauf zugreifen zu können
    # Listen mit ICD-Schlüsseln und Diagnosen
    icd = [
        "J30", "L20", "T78", "J45", "K52", "L23", "M79", "M06", "M12", "L40", "L93", "L94", "I10", "I20", "I21", "I25", "I50", "I63", "I70", "J20", "J22", "J40", "J44"
    ]

    diagnosen = [
        "Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub)",
        "Atopische Dermatitis (Neurodermitis)",
        "Andere unerwünschte Wirkungen, andernorts nicht klassifiziert",
        "Asthma bronchiale (häufig allergisch bedingt)",
        "Allergische Erkrankungen des Verdauungstrakts",
        "Allergische Kontaktdermatitis",
        "Rheumatismus, nicht näher bezeichnet",
        "Andere rheumatoide Arthritis",
        "Andere entzündliche Polyarthropathien",
        "Psoriasis (Schuppenflechte)",
        "Lupus erythematodes",
        "Sonstige lokal begrenzte Sklerodermie",
        "Essenzielle Hypertonie (Bluthochdruck)",
        "Angina pectoris",
        "Akuter Myokardinfarkt (Herzinfarkt)",
        "Chronische ischämische Herzkrankheit",
        "Herzinsuffizienz (Herzschwäche)",
        "Zerebraler Infarkt (Schlaganfall)",
        "Arteriosklerose",
        "Akute Bronchitis",
        "Akute Infektion der unteren Atemwege",
        "Bronchitis, nicht näher bezeichnet",
        "Sonstige chronisch obstruktive Lungenerkrankung"
    ]
    
    # DataFrame direkt mit Spaltennamen erstellen
    df_diagnosen = pd.DataFrame(list(zip(icd, diagnosen)), columns=["ICD", "Diagnose"])
    

    # DataFrame mit den ausgewählten Spalten NICHT normierter Daten
    df_auswahl = df_icd_faelle[icd_gesamt + ["Gruppe"]]  # df_auswahl mit 24 Spalten (ICD-Schlüssel) und 34 Zeilen (Daten aus 24 Gruppen)

    #  1. Korrelationsmatrix mit NICHT normierten Daten
    corr_matrix_auswahl_nicht_normalisiert = df_auswahl.drop(columns=["Gruppe"]).corr()


    # Visualisierung der Matrix
    st.subheader(f"Korrelationsmatrix nach Diagnosen zu Allergie, Herz-Kreislauf, Rheuma und Atemwegen")
    st.subheader(f"der NICHT normalisierten Krankenkassendaten nach Diagnosen (ICD-Schlüssel) \n (zwischen 2011 bis 2020; Stand: Mai 2025; ohne Gewähr)")
    fig, ax = plt.subplots(figsize=(26, 12))  # ✅ Explizite Figur erstellen
    sns.heatmap(corr_matrix_auswahl_nicht_normalisiert, annot=True, cmap="Spectral", linewidths=0.4, ax=ax, annot_kws={"fontsize": 20})


    #ax.set_title("1. Korrelationsmatrix der NICHT normalisierten Krankenkassendaten nach Diagnosen (ICD-Schlüssel) \n (zwischen 2011 bis 2020; Stand: Mai 2025; ohne Gewähr)")

    ax.set_xlabel("X-Achse", fontsize=20)
    ax.set_ylabel("Y-Achse", fontsize=20)

    # Achsenbeschriftungen größer & waagerecht setzen
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=20, rotation=0)  # X-Achse waagerecht
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=20, rotation=0)  # Y-Achse waagerecht

    cbar = ax.collections[0].colorbar  # Zugriff auf die Farbskala
    cbar.ax.set_ylabel("Korrelation", fontsize=20)  # Legenden-Titel größer machen
    cbar.ax.tick_params(labelsize=20)  # Schriftgröße der Werte in der Legende ändern
    
    plt.tight_layout()
    st.pyplot(fig)

    st.write(df_diagnosen, height= 100)

    # grüne Linie
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True)

    #########################
    # lineare Regression an einem ausgewählten Beispiel

    import plotly.graph_objects as go
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # CSV-Datei laden
    @st.cache_data
    def load_data():
        df = pd.read_csv("pdf_csv_daten/Krankenkassen_alle_Zahlen_okay_plus-Kategorie.csv")
        return df

    df = load_data()

    #_______________________________________________
    st.header("Exemplarisch zwei interessante Korrelationen\nLineare Regressionen")
    col1, col2 = st.columns([4, 5])  # Proportionen der Spalten für exemplarisch ausgewählte
    with col1:
        selected_icd_x = "J30"
        selected_icd_y = "M79"


        # Daten filtern
        df_filtered = df[df["ICD"].isin([selected_icd_x, selected_icd_y])]
        X = df_filtered[df_filtered["ICD"] == selected_icd_x]["Faelle"].values.reshape(-1, 1)
        Y = df_filtered[df_filtered["ICD"] == selected_icd_y]["Faelle"].values.reshape(-1, 1)

        # Lineare Regression mit sklearn
        model = LinearRegression()
        model.fit(X, Y)
        Y_pred = model.predict(X)

        # Interaktive Visualisierung mit Plotly in col1
        #st.write(f"{selected_icd_x} - Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub)  \nvs. {selected_icd_y} - Rheumatismus, nicht näher bezeichnet")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(), mode="markers", name="Datenpunkte", marker=dict(color="blue")))
        fig.add_trace(go.Scatter(x=X.flatten(), y=Y_pred.flatten(), mode="lines", name="Regression", line=dict(color="red")))


        fig.update_layout(title=f"{selected_icd_x} - Allergische Rhinitis  vs.  {selected_icd_y} - Rheumatismus",
                        xaxis_title=f"Fallzahlen {selected_icd_x}",
                        yaxis_title=f"Fallzahlen {selected_icd_y}",
                        showlegend=False)  # wird schon in der 2.Spalte angezeigt

        st.plotly_chart(fig)

        # Zeige Steigung und Achsenabschnitt
        #st.write("**Regressionsergebnisse**")
        #st.write(f"Steigung: {model.coef_[0][0]:.4f}")
        #st.write(f"Achsenabschnitt: {model.intercept_[0]:.4f}")

        st.write(f"**Regressionsergebnisse {selected_icd_x} vs. {selected_icd_y}**  \nSteigung: {model.coef_[0][0]:.4f}  |  Achsenabschnitt: {model.intercept_[0]:.4f}")
        

    with col2:
        selected_icd_x = "J45"
        selected_icd_y = "L23"
        
        # Daten filtern
        df_filtered = df[df["ICD"].isin([selected_icd_x, selected_icd_y])]
        X = df_filtered[df_filtered["ICD"] == selected_icd_x]["Faelle"].values.reshape(-1, 1)
        Y = df_filtered[df_filtered["ICD"] == selected_icd_y]["Faelle"].values.reshape(-1, 1)

        # Lineare Regression mit sklearn
        model = LinearRegression()
        model.fit(X, Y)
        Y_pred = model.predict(X)

        # Interaktive Visualisierung mit Plotly in col2
        #st.write(f"{selected_icd_x} - Asthma bronchiale (häufig allergisch bedingt) vs. {selected_icd_y} - Allergische Kontaktdermatitis")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(), mode="markers", name="Datenpunkte", marker=dict(color="blue")))
        fig.add_trace(go.Scatter(x=X.flatten(), y=Y_pred.flatten(), mode="lines", name="Regression", line=dict(color="red")))

        fig.update_layout(title=f"{selected_icd_x} - Asthma bronchiale  vs.  {selected_icd_y} - Allergische Kontaktdermatitis",
                        xaxis_title=f"Fallzahlen {selected_icd_x}",
                        yaxis_title=f"Fallzahlen {selected_icd_y}",
                        showlegend=True)

        st.plotly_chart(fig, key="fig1")

        # Zeige Steigung und Achsenabschnitt
        #st.write("**Regressionsergebnisse**")
        #st.write(f"Steigung: {model.coef_[0][0]:.4f}")
        #st.write(f"Achsenabschnitt: {model.intercept_[0]:.4f}")

        st.write(f"**Regressionsergebnisse {selected_icd_x} vs. {selected_icd_y}**  \nSteigung: {model.coef_[0][0]:.4f}  |  Achsenabschnitt: {model.intercept_[0]:.4f}")


    # 2. grüne Linie als Abtrennung
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True)


     ################# Interessante ##########################################################
    # "I10" - Essenzielle Hypertonie (Bluthochdruck) vs."I20" - Angina pectoris
    # "J30" - Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub) vs. "M79" - Rheumatismus, nicht näher bezeichnet
    # "J30" - Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub) vs. "K52" - Allergische Erkrankungen des Verdauungstrakts
    # "L20" - Atopische Dermatitis (Neurodermitis) vs. "J22" - Akute Infektion der unteren Atemwege
    # "J20" - Akute Bronchitis vs. "I50" - Herzinsuffizienz (Herzschwäche)
    #########################################################################################


    st.subheader("Was soll korreliert werden?") #erste Auswahl

    # Dictionary für die Selectbox, damit auch die Diagnose dabeisteht (für df_diagnosen siehe ganz oben)
    auswahl_mapping = {f"{row['ICD']} - {row['Diagnose']}": row['ICD'] for _, row in df_diagnosen.iterrows()}

    col1, col2, col3 = st.columns([4,4,1])
    with col1:
        selected_x = st.selectbox("Wähle ICD für X-Achse", list(auswahl_mapping.keys()), key="select1a")
        selected_icd_x = auswahl_mapping[selected_x]  # Automatisch nur den ICD-Code speichern

    with col2:
        selected_y = st.selectbox("Wähle ICD für Y-Achse", list(auswahl_mapping.keys()), key="select1b")
        selected_icd_y = auswahl_mapping[selected_y]  # Automatisch nur den ICD-Code speichern

    st.write(f"**Gewählte ICD-Codes:** X = {selected_icd_x}, Y = {selected_icd_y}")


    # Daten filtern
    df_filtered = df[df["ICD"].isin([selected_icd_x, selected_icd_y])]
    X = df_filtered[df_filtered["ICD"] == selected_icd_x]["Faelle"].values.reshape(-1, 1)
    Y = df_filtered[df_filtered["ICD"] == selected_icd_y]["Faelle"].values.reshape(-1, 1)

    # Lineare Regression mit sklearn
    model = LinearRegression()
    model.fit(X, Y)
    Y_pred = model.predict(X)

    # Interaktive Visualisierung mit Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(), mode="markers", name="Datenpunkte", marker=dict(color="blue")))
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y_pred.flatten(), mode="lines", name="Regression", line=dict(color="red")))

    fig.update_layout(title=f"{selected_x}  vs. {selected_y}",
                    xaxis_title=f"Fallzahlen {selected_icd_x}",
                    yaxis_title=f"Fallzahlen {selected_icd_y}",
                    showlegend=True)

    st.plotly_chart(fig, key="fig2")

        # Zeige Steigung und Achsenabschnitt
        #st.write("**Regressionsergebnisse**")
        #st.write(f"Steigung: {model.coef_[0][0]:.4f}")
        #st.write(f"Achsenabschnitt: {model.intercept_[0]:.4f}")

    st.write(f"**Regressionsergebnisse {selected_icd_x} vs. {selected_icd_y}**  \nSteigung: {model.coef_[0][0]:.4f}  |  Achsenabschnitt: {model.intercept_[0]:.4f}")

    # Tabellenansicht der gefilterten Daten
    #st.subheader("Gefilterte Daten")
    #st.dataframe(df_filtered)


    # 3. grüne Linie als Abtrennung
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True)
    ######################################################################################################
    st.subheader("Noch eine weitere Korrelation?")   # für eine zweite Auswahl

    # Dictionary für die Selectbox, damit auch die Diagnose dabeisteht (für df_diagnosen siehe ganz oben)
    auswahl_mapping = {f"{row['ICD']} - {row['Diagnose']}": row['ICD'] for _, row in df_diagnosen.iterrows()}

    col1, col2, col3 = st.columns([4,4,1])
    with col1:
        selected_x = st.selectbox("Wähle ICD für X-Achse", list(auswahl_mapping.keys()), key="select2a")
        selected_icd_x = auswahl_mapping[selected_x]  # Automatisch nur den ICD-Code speichern

    with col2:
        selected_y = st.selectbox("Wähle ICD für Y-Achse", list(auswahl_mapping.keys()), key="select2b")
        selected_icd_y = auswahl_mapping[selected_y]  # Automatisch nur den ICD-Code speichern

    st.write(f"**Gewählte ICD-Codes:** X = {selected_icd_x}, Y = {selected_icd_y}")


    # Daten filtern
    df_filtered = df[df["ICD"].isin([selected_icd_x, selected_icd_y])]
    X = df_filtered[df_filtered["ICD"] == selected_icd_x]["Faelle"].values.reshape(-1, 1)
    Y = df_filtered[df_filtered["ICD"] == selected_icd_y]["Faelle"].values.reshape(-1, 1)

    # Lineare Regression mit sklearn
    model = LinearRegression()
    model.fit(X, Y)
    Y_pred = model.predict(X)

    # Interaktive Visualisierung mit Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(), mode="markers", name="Datenpunkte", marker=dict(color="blue")))
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y_pred.flatten(), mode="lines", name="Regression", line=dict(color="red")))

    fig.update_layout(title=f"{selected_x}  vs. {selected_y}",
                    xaxis_title=f"Fallzahlen {selected_icd_x}",
                    yaxis_title=f"Fallzahlen {selected_icd_y}",
                    showlegend=True)

    st.plotly_chart(fig)

        # Zeige Steigung und Achsenabschnitt
        #st.write("**Regressionsergebnisse**")
        #st.write(f"Steigung: {model.coef_[0][0]:.4f}")
        #st.write(f"Achsenabschnitt: {model.intercept_[0]:.4f}")

    st.write(f"**Regressionsergebnisse {selected_icd_x} vs. {selected_icd_y}**  \nSteigung: {model.coef_[0][0]:.4f}  |  Achsenabschnitt: {model.intercept_[0]:.4f}")

    # Tabellenansicht der gefilterten Daten
    #st.subheader("Gefilterte Daten")
    #st.dataframe(df_filtered)

    # 4. grüne Linie als Abtrennung
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True)
    ######################################################################################################
    st.write("Die vorliegende erste Analyse der vom Statistischen Bundesamt veröffentlichten Daten der Krankenkassen zur Arbeitsunfähigkeit kann erste Hinweise auf mögliche Assoziationen verschiedener Diagnosen geben. Da diese allerdings vorwiegend zu Übungs- und Präsentationszwecken erstellt wurde, kann keine Gewähr für die Richtigkeit der dargestellten Ergebnisse übernommen werden. Eine überarbeitete Version könnte allerdings richtungsweisend für weitere Forschungen sein (Heidi Kaulfürst-Soboll, Mai 2025).")
    ######################################################################################################
    
    '''
    # einfachere Version, die nur ICD ohne Beschreibung verwendet


    # ICD-Kategorien auswählen
    icd_option_x = ['J30', 'L20', 'T78', 'J45', 'K52', 'L23', 'M79', 'M06', 'M12', 'L40',
       'L93', 'L94', 'I10', 'I20', 'I21', 'I25', 'I50', 'I63', 'I70', 'J20',
       'J22', 'J40', 'J44']
    icd_option_y = ['J30', 'L20', 'T78', 'J45', 'K52', 'L23', 'M79', 'M06', 'M12', 'L40',
       'L93', 'L94', 'I10', 'I20', 'I21', 'I25', 'I50', 'I63', 'I70', 'J20',
       'J22', 'J40', 'J44']

    st.sidebar.header("Einstellungen")
    selected_icd_x = st.sidebar.selectbox("Wähle ICD für X-Achse", icd_option_x)
    selected_icd_y = st.sidebar.selectbox("Wähle ICD für Y-Achse", icd_option_y)

    
    # Daten filtern
    df_filtered = df[df["ICD"].isin([selected_icd_x, selected_icd_y])]
    X = df_filtered[df_filtered["ICD"] == selected_icd_x]["Faelle"].values.reshape(-1, 1)
    Y = df_filtered[df_filtered["ICD"] == selected_icd_y]["Faelle"].values.reshape(-1, 1)

    # Lineare Regression mit sklearn
    model = LinearRegression()
    model.fit(X, Y)
    Y_pred = model.predict(X)

    # Interaktive Visualisierung mit Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(), mode="markers", name="Datenpunkte", marker=dict(color="blue")))
    fig.add_trace(go.Scatter(x=X.flatten(), y=Y_pred.flatten(), mode="lines", name="Regression", line=dict(color="red")))

    fig.update_layout(title=f"{selected_icd_x} vs. {selected_icd_y}", 
                    xaxis_title=f"Fallzahlen {selected_icd_x}",
                    yaxis_title=f"Fallzahlen {selected_icd_y}",
                    showlegend=True)

    st.plotly_chart(fig)

    # Zeige Steigung und Achsenabschnitt
    st.write("**Regressionsergebnisse**")
    st.write(f"Steigung: {model.coef_[0][0]:.4f}")
    st.write(f"Achsenabschnitt: {model.intercept_[0]:.4f}")

    # Tabellenansicht der gefilterten Daten
    #st.subheader("Gefilterte Daten")
    #st.dataframe(df_filtered)

    # ----------------------------------------------

    # "I10" - Essenzielle Hypertonie (Bluthochdruck) vs."I20" - Angina pectoris
    # "J30" - Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub) vs. "M79" - Rheumatismus, nicht näher bezeichnet
    # "J30" - Allergische Rhinitis (z. B. Heuschnupfen, Hausstaub) vs. "K52" - Allergische Erkrankungen des Verdauungstrakts
    # "L20" - Atopische Dermatitis (Neurodermitis) vs. "J22" - Akute Infektion der unteren Atemwege
    # "J20" - Akute Bronchitis vs. "I50" - Herzinsuffizienz (Herzschwäche)

'''