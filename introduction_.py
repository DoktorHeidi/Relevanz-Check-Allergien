import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
from PIL import Image # dafür pip install pillow, falls noch nicht geschehen...

# Seitenkonfiguration nur EINMAL setzen
#st.set_page_config(page_title="Bildplatzierungs-App", layout="wide")

def app():
    st.markdown("### Willkommen zu meinem Projekt")
    st.subheader(" Ich habe mich mit der spannenenden Frage beschäftigt, ob die Prävalenz von Allergien möglicherweise mit der von bestimmten Volkskrankheiten assoziiert ist.")
    #st.write("Für eine kurze Einführung nutze die Pfeile ..." )

    #datum = datetime.today().strftime('%d.%m.%Y')
    datum = "update 22.03.2026"
    #name = "Heidi"


    
    st.markdown("""
        <style>
            .card {
                background-color: white;#f0f2f6;
                padding: 20px;
                border-radius: 10px;
                #border-left: 5px solid #ff4b4b;
                margin-bottom: 10px;
            }

        </style>
    """, unsafe_allow_html=True)


    #st.title("Dashboard mit weißen Containern")

    #col1, col2 = st.columns(2)

    #with col1:
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("Bild-Allergien_2.jpg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    #with col2:
    
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Laut ECARF leidet fast jeder dritte Mensch in Europa an einer Allergie. ")
    st.write(" ")
    st.subheader("Durch eine richtige Behandlung könnte")
    st.subheader("ein wirtschaftlicher Schaden von ")
    st.write(" ")
    st.title("100 Milliarden Euro")
    st.write("")
    st.subheader("vermieden werden.")

    st.write(" https://www.ecarf.org/presse/neues-zum-start-der-pollensaison-2023/")
    #st.title("Das entspricht rund 0.7% BIP")
    #st.write("")

    st.markdown('</div>', unsafe_allow_html=True)

        


#__________________________________________________

if __name__ == "__main__":
    app()
