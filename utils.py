# Die App kann im integrierten Terminal von main_2 mit "streamlit run main_2" gestartet werden.


import streamlit as st

# Sidebar Funktion mit einer zentralen Kontrollvariable
def draw_sidebar():
    with st.sidebar:
        st.title("🌍 Navigation")

        # Definiere eine zentrale Session-State-Variable für die Auswahl
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = None  # Anfangszustand

        # Manuelle Auswahlmöglichkeiten außerhalb der `radio`-Buttons
        option = st.selectbox("Kategorie wählen", [
            "Relevanz-Check von Allergien", 
            "Airbuddy HealthWatch"
            ])

        # Automatische Regulierung: Auswahl der Buttons wird auf Basis der `option`-Wahl zurückgesetzt
        if option == "Relevanz-Check von Allergien":
            st.session_state.selected_page = "Relevanz-Check von Allergien"
        elif option == "Airbuddy HealthWatch":
            st.session_state.selected_page = "Airbuddy HealthWatch"
        else:
            st.session_state.selected_page = "Relevanz-Check von Allergien"  # Falls Nichts gewählt wird

        # Dynamische `radio`-Buttons erscheinen nur für die aktivierte Kategorie
        main_select, health_select = None, None
        if st.session_state.selected_page == "Relevanz-Check von Allergien":
            main_select = st.radio("Wähle eine Seite", [
                "Einführung",
                "Timeline", 
                "Analyse 1: Überblick",
                "Analyse 2: Mustererkennung",
                "Analyse 3: ausgewählte & interaktive Korrelationen"
            ], key="main_select")

        elif st.session_state.selected_page == "Airbuddy HealthWatch":
            health_select = st.radio("Wähle eine Analyse", [
                "BUDDY", 
                "Luftqualität", 
                "Pollen", 
                "Bilanz", 
                "Gewitter",
                "Sahara", 
                "Urlaub", 
                "ICD", 
                "Real"
            ], key="health_select")

        st.markdown("---")
        st.write("🌿 **Presented by Heidi (Relevanz-Check) &  Linda (HealthWatch)** 🌿\n\n")
        st.image("dsi_Bild.png")

    return main_select, health_select



import introduction_
import timeline
import analyse1
import analyse2
import analyse_extra
import dummy
#import klima

# Zuordnung der Menüpunkte der sidebar zu den Dateien
pages_1 = {
    "Einführung": introduction_,
    "Timeline": timeline,
    "Analyse 1: Überblick": analyse1,
    "Analyse 2: Mustererkennung": analyse2,
    "Analyse 3: ausgewählte & interaktive Korrelationen": analyse_extra
}

# leider stehen aus Gründen des Urheberrechts Lindas Dateien nicht zur Verfügung. Deshalb hier nur eine dummy-Seite
pages_2 = {
    "BUDDY": dummy,
    "Luftqualität": dummy,
    "Pollen": dummy,
    "Bilanz": dummy,
    "Gewitter": dummy,
    "Sahara": dummy,
    "Urlaub": dummy,
    "ICD": dummy,
    "Real": dummy
}

# Funktion zum Anzeigen der Seiten
def show_page(module):
    if hasattr(module, "app") and callable(module.app):
        module.app()
    else:
        st.write("Diese Seite ist nicht implementiert.")

    
