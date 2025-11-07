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
            "Projekt 2"
            ])

        # Automatische Regulierung: Auswahl der Buttons wird auf Basis der `option`-Wahl zurückgesetzt
        if option == "Relevanz-Check von Allergien":
            st.session_state.selected_page = "Relevanz-Check von Allergien"
        elif option == "Projekt 2":
            st.session_state.selected_page = "Projekt 2"
        else:
            st.session_state.selected_page = "Relevanz-Check von Allergien"  # Falls Nichts gewählt wird

        # Dynamische `radio`-Buttons erscheinen nur für die aktivierte Kategorie
        main_select, project_select = None, None
        if st.session_state.selected_page == "Relevanz-Check von Allergien":
            main_select = st.radio("Wähle eine Seite", [
                "Einführung",
                "Timeline", 
                "Analyse 1: Überblick",
                "Analyse 2: Mustererkennung",
                "Analyse 3: ausgewählte und interaktive Korrelationen"
            ], key="main_select") #Zuordnung zu den Seiten erfolgt weiter unten

        elif st.session_state.selected_page == "Projekt 2":
            project_select = st.radio("Wähle eine Analyse", [
                "a", 
                "b", 
                "c", 
                "d", 
                "e",
                "f", 
                "g", 
                "h", 
                "i"
            ], key="projct_select")

        st.markdown("---")
        st.write("🌿 **Presented by** 🌿\n\n")
        st.image("mein_Logo.png")

    return main_select, project_select



import introduction_
import timeline
import analyse1
import analyse2
import analyse_extra
import dummy


# Zuordnung der Menüpunkte der sidebar (siehe Code weiter oben) zu den Dateien
pages_1 = {
    "Einführung": introduction_,
    "Timeline": timeline,
    "Analyse 1: Überblick": analyse1,
    "Analyse 2: Mustererkennung": analyse2,
    "Analyse 3: ausgewählte und interaktive Korrelationen": analyse_extra
}

# Platzhalter für weiteres Projekt
pages_2 = {
    "a": dummy,
    "b": dummy,
    "c": dummy,
    "d": dummy,
    "e": dummy,
    "f": dummy,
    "g": dummy,
    "h": dummy,
    "i": dummy
}

# Funktion zum Anzeigen der Seiten
def show_page(module):
    if hasattr(module, "app") and callable(module.app):
        module.app()
    else:
        st.write("Diese Seite ist noch nicht implementiert.")

    
