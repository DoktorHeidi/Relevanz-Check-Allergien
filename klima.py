# Klimadaten für ganz Deutschland
import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# 🌍 **URLs der Wetterdaten**
urls = {
    "precipitation": "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/precipitation/regional_averages_rr_year.txt",
    "temperature": "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/air_temperature_mean/regional_averages_tm_year.txt",
    "frost_days": "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/frost_days/regional_averages_tnas_year.txt",
    "tropical_nights": "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/air_temperature_mean/regional_averages_tm_year.txt"
}

# 📥 **Daten abrufen und in DataFrame speichern**
def load_weather_data():
    dfs = []
    for key, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(url, delimiter=";", skiprows=1)
            df = df[df['Jahr'].between(2011, 2024)]  # Nur relevante Jahre behalten
            df = df[['Jahr', 'Deutschland']]  # Spalten umbenennen
            df.rename(columns={'Deutschland': key}, inplace=True)
            dfs.append(df)
        else:
            st.warning(f"⚠️ Fehler beim Laden der Wetterdaten: {key}")

    # Alle DataFrames zusammenführen
    if dfs:
        weather_df = dfs[0]
        for df in dfs[1:]:
            weather_df = weather_df.merge(df, on='Jahr', how='inner')
        return weather_df
    else:
        return None

# 🌤️ **Streamlit Wetteranalyse-Seite**
def app():
    st.title("🌦️ Wetterdaten für Deutschland 🌤️")
    st.markdown("Ist die Anzahl der Fälle mit Arbeitsunfähigkeit mit dem Wetter assoziiert? Für aussagekräftige Korrelationen bedarf es detaillierterer Daten mit Tag- und Ortsangaben. Deshalb werde ich an dieser Stelle nicht weiter in die Tiefe gehen.")
    st.markdown("Die Wetterdaten werden **direkt von DWD geladen** für den interessanten Zeitraum.")
    st.markdown("Da die Daten der Krankenkassen bei dieser Analyse nur gesammelte Daten aus dem jeweiligen Jahr sind,\nsind an dieser Stelle nur die gemittelten Daten für das Jahr aus ganz Deutschland dargestellt.")
    # 🔄 **Daten abrufen**
    weather_df = load_weather_data()

    if weather_df is not None:
        # 🎚️ **Jahr-Filter**
        #jahr = st.slider("Wähle ein Jahr", int(weather_df["Jahr"].min()), int(weather_df["Jahr"].max()), int(weather_df["Jahr"].max()), key="jahr_slider")

        # 📊 **Liniendiagramm der Wetterdaten**
        st.subheader(f"📊 Wetterdaten für Deutschland")# im Jahr {jahr}")
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(weather_df['Jahr'], weather_df['temperature'], color='red', label="Temperatur")
        ax.plot(weather_df['Jahr'], weather_df['precipitation'], color='blue', label="Niederschlag")
        ax.plot(weather_df['Jahr'], weather_df['frost_days'], color='black', label="Frosttage")
        ax.plot(weather_df['Jahr'], weather_df['tropical_nights'], color='yellow', label="Tropische Nächte")

        ax.set_xlabel("Jahr")
        ax.set_ylabel("Werte")
        ax.set_title("📊 zurückliegen Wetterdaten für Deutschland zwischen 2011 bis 2024")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # 📑 **Tabellenansicht der Daten**

        st.subheader("📊 Detaillierte Wetterdaten")

        jahr = st.slider("Wähle ein Jahr", int(weather_df["Jahr"].min()), int(weather_df["Jahr"].max()), int(weather_df["Jahr"].max()), key="jahr_slider")

        st.dataframe(weather_df[weather_df["Jahr"] == jahr])

    else:
        st.error("⚠️ Fehler beim Abrufen der Wetterdaten! Bitte überprüfe die DWD-Links.")


    st.title("🌦️ zurückliegende Wetterdaten für Deutschland")
   

    # 🔄 **Daten abrufen**
    weather_df = load_weather_data()

    if weather_df is not None:
        # 🎚️ **Jahr-Filter**
        #jahr = st.slider("Wähle ein Jahr", int(weather_df["Jahr"].min()), int(weather_df["Jahr"].max()), int(weather_df["Jahr"].max()), key="jahr_slider2")

        # 📊 **Liniendiagramm der Wetterdaten**
        #st.subheader(f"📊 Wetterdaten für Deutschland im Jahr {jahr}")
        #fig, ax = plt.subplots(figsize=(10, 6))

        #ax.plot(weather_df['Jahr'], weather_df['temperature'], color='red', label="Temperatur")
        #ax.plot(weather_df['Jahr'], weather_df['precipitation'], color='blue', label="Niederschlag")
        #ax.plot(weather_df['Jahr'], weather_df['frost_days'], color='black', label="Frosttage")
        #ax.plot(weather_df['Jahr'], weather_df['tropical_nights'], color='yellow', label="Tropische Nächte")

        #ax.set_xlabel("Jahr")
        #ax.set_ylabel("Werte")
        #ax.set_title("📊 Wetterdaten für Deutschland")
        #ax.legend()
        #ax.grid(True)

        #st.pyplot(fig)

        # 📊 **Subplots für detaillierte Klima-Analyse**
        st.subheader("🔍 Detaillierte Klima-Analyse: Temperatur, Niederschlag & Frosttage")
        fig_subplots, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 9), sharex=True)

        # Temperatur (rote Linie)
        axes[0].plot(weather_df['Jahr'], weather_df['temperature'], color='red', label="Temperatur")
        axes[0].set_ylabel("Temperatur (°C)")
        axes[0].legend()
        axes[0].grid(True)

        # Niederschlag (blaue Linie)
        axes[1].plot(weather_df['Jahr'], weather_df['precipitation'], color='blue', label="Niederschlag")
        axes[1].set_ylabel("Niederschlag (mm)")
        axes[1].legend()
        axes[1].grid(True)

        # Frosttage & Tropische Nächte (schwarze & gelbe Linie)
        axes[2].plot(weather_df['Jahr'], weather_df['frost_days'], color='black', label="Frosttage")
        axes[2].plot(weather_df['Jahr'], weather_df['tropical_nights'], color='yellow', label="Tropische Nächte")
        axes[2].set_ylabel("Frosttage / Tropische Nächte")
        axes[2].legend()
        axes[2].grid(True)

        plt.xlabel("Jahr")
        plt.suptitle("📊 Klimatrends im Detail")
        plt.tight_layout()
        st.pyplot(fig_subplots)

        # 📑 **Tabellenansicht der Daten**
        st.subheader("📊 Detaillierte Wetterdaten")
        st.dataframe(weather_df[weather_df["Jahr"] == jahr])

    else:
        st.error("⚠️ Fehler beim Abrufen der Wetterdaten! Bitte überprüfe die DWD-Links.")


    # Abschnitt: Fazit
    st.header("Fazit")
    st.markdown("""
    Die Umweltbelastung durch Emissionen und Pollen hat einen signifikanten Einfluss auf die Entstehung und Verschärfung allergischer Erkrankungen. Durch Datenanalysen können präzisere Vorhersagen getroffen und präventive Maßnahmen entwickelt werden.
    """)

    st.title("Danke für Eure Aufmerksamkeit : )")
    #st.image("Ende.jpg")


   

