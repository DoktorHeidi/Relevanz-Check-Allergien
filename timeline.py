import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit_plotly_events as spe
from streamlit_plotly_events import plotly_events
#from main_2 import draw_sidebar_()

import webbrowser


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit_plotly_events as spe
from streamlit_plotly_events import plotly_events



def app():
    st.title("Relevanz-Check von Allergien")

    # Schritte mit Labels, Beschreibungen und Links
    steps = [
        ("🔍 Recherche", "Datenquellen analysieren", "https://www.bundesgesundheitsministerium.de/themen/krankenversicherung/zahlen-und-fakten-zur-krankenversicherung/geschaeftsergebnisse.html"),
        ("📥 PDF-Download", "Automatisierter Download von PDFs", "https://www.example.com/pdf-download"),
        ("📄 Textextraktion", "Text aus PDFs extrahieren", "https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/Statistiken/GKV/Geschaeftsergebnisse/Faelle_Tage_nach_Diagnosen_2017.pdf"),
        ("📊 DataFrame", "Daten in DataFrame speichern", "https://www.example.com/dataframe"),
        ("🏗️ Umgestaltung", "Daten umstrukturieren", "https://www.example.com/umgestaltung"),
        ("📈 Analyse", "Daten analysieren", "https://www.example.com/analyse"),
        ("⚖️ Normalisierung", "Daten bereinigen", "https://www.example.com/normalisierung"),
        ("🤖 ML - Muster", "Muster erkennen", "https://www.example.com/machine-learning")
    ]

    # Farben für die Symbole
    colors = [
        "#FDFF00", # Zitronengelb
        "#A9A9A9",  # Grün-Grau
        
        "#CDE4CE",  # Sanftes Pastellgrün
        "#A8D5BA",  # Zartes Mintgrün
        "#84C7A8",  # Helles Salbeigrün
        "#5FBF95",  # Frisches Smaragdgrün
        "#1E735C",  # Lebendiges Blattgrün
        "#FF7700"   # Akzentfarbe: Orange
    ]

    # Erstelle die Plotly-Figur
    fig = go.Figure(
        layout={
            'height': 200,
            'font': {'size': 12}
        }
    )



    # Pfeilspitze simulieren mit einem Marker am Endpunkt
    fig.add_trace(go.Scatter(
        x=[len(steps)],
        y=[0.6],
        mode="markers",
        marker=dict(size=20, color="#D8F3DC", symbol="triangle-right"),
        showlegend=False
    ))

    # Links als Symbole auf dem Pfeil
    for i, (emoji, label, link) in enumerate(steps):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0.6],
            mode="markers",
            marker=dict(size=40, color=colors[i % len(colors)]),
            text=f'<a href="{link}" target="_blank">{label}</a>',
            textfont=dict(size=20),
            hoverinfo="text"
        ))

    # Layout anpassen
    #fig.update_layout(
    #   title="Interaktiver Zeitstrahl mit einem langen Pfeil",
    #  xaxis=dict(showgrid=False, zeroline=False, tickmode="array", tickvals=list(range(len(steps))), ticktext=[emoji for emoji, _, _ in #steps]),
    #  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #  showlegend=False
    #)

    fig.update_layout(
        title="Timeline (Heidi)",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=list(range(len(steps))),
            ticktext=[emoji for emoji, _, _ in steps],
            tickangle=40  # Dreht die Beschriftungen um 45 Grad
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        showlegend=False
    )
    st.title("Timeline - Heidi")
    st.subheader("Idee:    💡 Relevanz-Check von Allergien!")
    st.subheader("Daten:   📜 Fallzahlen aus Krankenkassen- und Krankenhausstatistiken mit Diagnoseschlüsseln")

    st.markdown("**Frage**: Welche Relevanz haben Allergien bei der Meldung zur Arbeitsunfähigkeit?\n"
            "Lassen sich Muster erkennen, die einen Hinweis darauf geben könnten, dass auch primär nicht als Allergie eingestufte Krankheiten eigentlich doch mit Allergien in Verbindung gebracht werden könnten?")

    ## Erstellung timeline
    # Erstelle eine Zeile mit zwei Spalten: linke Textbox und Plot
    col1, col2 = st.columns([1, 4])

    with col1:
        # Textbox mit Glühbirne-Emoji
        st.markdown("\n")  # Alternativ: st.text("🔆")
        st.image("Recherche.png")
        st.write("")
        

        
    with col2:
        # Erstelle die Plotly-Figur
        fig = go.Figure(
            layout={
                'height': 200,
                'font': {'size': 12}
            }
        )

        # Pfeilspitze simulieren mit einem Marker am Endpunkt
        fig.add_trace(go.Scatter(
            x=[len(steps)],
            y=[0.6],
            mode="markers",
            marker=dict(size=40, color="#D8F3DC", symbol="triangle-right"),
            showlegend=False
        ))

        # Links als Symbole auf dem Pfeil
        for i, (emoji, label, link) in enumerate(steps):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[0.6],
                mode="markers",
                marker=dict(size=40, color=colors[i % len(colors)]),
                text=f'<a href="{link}" target="_blank">{label}</a>',
                textfont=dict(size=20),
                hoverinfo="text"
            ))

        # Layout anpassen
        fig.update_layout(
            #title="... mit Fallzahlen aus Krankenkassen- und Krankenhausstatistiken",
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                tickmode="array",
                tickvals=list(range(len(steps))),
                ticktext=[emoji for emoji, _, _ in steps],
                tickangle=40  # Dreht die Beschriftungen um 40 Grad
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            showlegend=False
        )

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, key="textfeld")

        # Links als Variablen speichern

        link1 = "https://www.bundesgesundheitsministerium.de/themen/krankenversicherung/zahlen-und-fakten-zur-krankenversicherung/geschaeftsergebnisse.html"
        link2 = "https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/Statistiken/GKV/Geschaeftsergebnisse/Faelle_Tage_nach_Diagnosen_2017.pdf"

        # HTML + CSS für versteckte Links mit Hover-Effekt
        hover_link_css = """
        <style>
        .link {
            text-decoration: none;
            font-size: 12px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            background-color: #f0f0f0;
            color: black;
            
            margin-right: 40px;
        }
        .link:hover {
            color: blue; /* Farbe ändert sich beim Hover */
        }
        </style>
        """

        st.markdown(hover_link_css, unsafe_allow_html=True)

        # Zwei interaktive Links ohne sichtbaren URL-Text
                
        st.markdown(f'<a class="link" href="{link1}" target="_blank">🔍 Recherche</a>', unsafe_allow_html=True)

        st.markdown(f'<a class="link" href="{link2}" target="_blank">📊 Download</a>', unsafe_allow_html=True)

        st.write("Hier sind die Original-Daten verlinkt.")


    #nach automatisiertem Download und Umwandlung von pdf-Dateien in einen Dataframe:

    # Textbereich mit Beschreibung

    '''"Analyse 1: Überblick": analyse1,
    "Analyse 2: Mustererkennung": analyse2,
    "Analyse 3: ausgewählte Korrelationen": analyse_extra'''
    
    st.text_area("Anspruch dieses Projektteils",         
            "Die hier analysierten Daten waren nur in Form von pdf-Dateien auf der Homepage des Bundesgesundheitsministeriums zugänglich.\n"
            "Diese wurden von mir über Webscraping automatisiert heruntergeladen.\n"
            "Da die enthaltenen Tabellen nicht einheitlich formatiert waren, galt es eine Methode zu finden, nur relevante Teile zu extrahieren.\n"
                        
            "Zur Vorbereitung der Daten gehörte nach Erstellung eines Dataframes eine weitere Umgestaltung und Erweiterung mit übergeordneten ICD-Kategorien.\n\n"
            
            "Die Analyse wurde in drei Schritten vorgenommen:\n"
            "- Analyse 1 wurde zur Übersicht der Daten durchgeführt.\n"
            "- Analyse 2 wurde mit standardisierten Daten durchgeführt, um mit kMeans Muster erkennen zu können.\n"
            
            "- Analyse 3 wurde mit gefilterten Daten gearbeitet, wobei hier auch die Transponierung mancher Spalten nötig war.\n"
            "Ziel der dritten Analyse war es herauszufinden, ob die Anzahl der Fälle bestimmter Diagnose-Schlüssel mit Assoziation zu Allergien \nmit anderen mit Assoziation zu Herz-Kreislauf-, Rheuma- und Atemwegserkrankungen korrelieren. Zudem wurde Multiple Sklerose als Autoimmunerkrankung in die Auswahl mit aufgenommen, die sich grundsätzlich von Allergien unterscheiden.\n"
            " Zum Schluss besteht die Möglichkeit der freien Auswahl von Diagnose-Schlüsseln zur Korrelation."
            ,
            height=300)
        

    

if __name__ == "__main__":
    app()
