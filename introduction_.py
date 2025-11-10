import streamlit as st
from datetime import datetime
from PIL import Image # dafür pip install pillow, falls noch nicht geschehen...

# Seitenkonfiguration nur EINMAL setzen
# st.set_page_config(page_title="Bildplatzierungs-App", layout="wide")

def app():
    st.markdown("### Es wird spannend: was uns Daten zur Arbeitsunfähigkeit verraten ...")
    st.write(" In diesem Projekt habe ich mich mit der Frage beschäftigt, ob die Prävalenz von Allergien möglicherweise mit der von bestimmten Volkskrankheiten assoziiert ist.")
    st.write("Für eine kurze Einführung zur Thematik nutze die Pfeile (⬅️ ➡️) oder gehe direkt über die sidebar zur Timeline, wenn dich meine Herangehensweise interessiert und dann zu den Analysen.")
    st.write("Kleiner Tipp: Am spannendsten wird es in Analyse 3 😉, über die sidebar kannst du auch direkt dorthin springen.")
    #datum = datetime.today().strftime('%d.%m.%Y')
    datum = "update 3. November 2025"
    #name = "Heidi"


    # Session State für Navigation
    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 0

    # Inhalte für die Slideshow: Bild oder Text

    slides = [
        {
            "type": "image",
            "title": "Was ist aus den Medien bekannt?",
            "content": "Allergien_Pollen_Feinstaub.png",
            "caption": "Feinstaub & Pollen"
        },

        {
            "type": "text",
            "title": "Welche Schadstoffe in der Luft sind von größerer Bedeutung für die Gesundheit?",
            "content": """
    - Feinstaub (nach Größe in µm)
        - PM10: Inhalierbarer Feinstaub ➔ lagert sich in den oberen Atemwegen ab
        - PM2,5: Lungengängiger Feinstaub ➔ kleinere Partikel dringen tiefer in die Lunge ein
        - PM0,1: Ultrafeinstaub ➔ kleinste Partikel, die sogar in den Blutkreislauf gelangen können

    - Stickstoffdioxid (NO₂): ätzendes Reizgas
    
    - Ozon (O₃): starkes Oxidationsmittel, reizend und entzündungsfördernd

            """,
            "caption": " "
        },

        {
            "type": "text",
            "title": "Hauptverursacher von Emissionen",
            "content": """
    - Verkehr
    - Industrie
    - Landwirtschaft

            """,
            "caption": " "
        },
        {
            "type": "image",
            "title": "Leichter Rückgang der Emissionen in Deutschland in den letzten Jahren?",
            "content": "Emissionen.png",
            "caption": "Darstellung ohne CO2 - destatis - Statistisches Bundesamt"
        },



        {
            "type": "text",
            "title": "Einfluss auf Luftqualität und Gesundheit",
            "content": "Emissionen verschlechtern die Luftqualität\n"
            "➔  gesundheitliche Probleme - insbesondere bei Allergikern",
            "caption": " "
        },
        {
            "type": "text",
            "title": "Pollen als Verursacher von Beschwerden",
            "content": """
    - Saisonabhängigkeit:   Die Pollenbelastung variiert regional und saisonal
    - Hauptpollenarten:       Birke, Gräser, Ambrosia

    - Klimaänderung:            Längere Pollensaisons durch steigende Temperaturen
    - Effekte:                              Schadstoffe können Menge und Aggressivität von Pollen verstärken
                                                    ➔  Zunahme von Allergien und Asthmaanfällen
            """,
            "caption": " "
        },
        {
            "type": "text",
            "title": "Daten und Studienlage",
            "content": """
    - Datenquellen: Umweltämter, Wetterdienste, Gesundheitsberichte.

    - Studien: zeigen Korrelation zwischen Schadstoffkonzentration und Häufigkeit von Allergien.
       ➔ Steigende Emissionen und Pollenkonzentrationen können das Allergierisiko erhöhen.
            """,
            "caption": " "
        },
        {
            "type": "text",
            "title": "Annahme",
            "content": """Emissionen und Pollen haben\n
             signifikanten Einfluss auf Entstehung und Verschärfung allergischer Erkrankungen.
             ➔ Präventive Maßnahmen durch präzisere Vorhersagen?
            """,
            "caption": " "
        },
        {
            "type": "text",
            "title": "Weiter geht es ...",
            "content": """... über die Navigationsleiste 🌍 Navigation \n\n  mit   📊  Relevanz-Check von Allergien \n \n  mit   ⚪ Timeline \n\n ← ← ←
            """,
            "caption": "  "
        }
    ]
    ##########################################################################################
    # Inhalte für Bildershow beendet
    ##########################################################################################

    # Funktion zum Wechseln der Slides
    def next_slide():
        st.session_state["slide_index"] = (st.session_state["slide_index"] + 1) % len(slides)

    def prev_slide():
        st.session_state["slide_index"] = (st.session_state["slide_index"] - 1) % len(slides)


    # Linie oben
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True) # grüne Linie

    # Feste Höhe für Inhalt
    st.container()

    col1, col2, col3 = st.columns([1, 10, 1])

    with col1:
        st.button("⬅️", on_click=prev_slide)

    with col2:

        # Bild oder Text anzeigen mit fester Höhe
        if slides[st.session_state["slide_index"]]["type"] == "image":

            st.subheader(slides[st.session_state["slide_index"]]["title"])
            image = Image.open(slides[st.session_state["slide_index"]]["content"])
        
            # Bestimme das Verhältnis des Bildes
            width, height = image.size
            
            if height > width:
                container_width = False
            else:
                container_width = True

            st.image(slides[st.session_state["slide_index"]]["content"], caption=slides[st.session_state["slide_index"]]["caption"], use_container_width=container_width)
        else:
            # Inject custom CSS, um den Hintergrund des Textareas zu ändern
            st.markdown(
                """
                <style>
                /* Hintergrundfarbe für alle Textareas auf weiß */
                textarea {
                    background-color: white !important;
                    font-size: 20px !important;
                    color: black !important;
                    padding-top: 2px !important; /* Verringert den oberen Abstand */

                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.subheader(slides[st.session_state["slide_index"]]["title"])
            st.text_area(label= " ", value=slides[st.session_state["slide_index"]]["content"], height=250) # label=slides[st.session_state["slide_index"]]["title"],

    with col3:
        st.button("➡️", on_click=next_slide)
        

    # Linie unten
    st.markdown("""<hr style="border: 3px solid #4CAF50;">""", unsafe_allow_html=True)

    # Punkte zur Anzeige der aktuellen Box
    dots = ["⚫" if i == st.session_state["slide_index"] else "⚪" for i in range(len(slides))]
    st.markdown(f"<p style='text-align: center; font-size: 8px;'>{' '.join(dots)}</p>", unsafe_allow_html=True)

    #############

    #st.success("Abschlussprojekt von **Heidi** im Rahmen der Weiterbildung am dsi (Berlin) 🌿")

    #button_timeline = st.button("Timeline")

if __name__ == "__main__":
    app()
