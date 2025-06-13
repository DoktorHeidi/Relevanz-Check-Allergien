import streamlit as st
# diese Seite benutzen, um im integrierten Terminal mit streamlit run main_2.py die Seite zu starten ...

# Seiten-Config
st.set_page_config(
    page_title="Willkommen!",
    layout="wide"
)



import utils



# Sidebar initialisieren
main_select, health_select = utils.draw_sidebar()

# Auswahl prüfen und entsprechende Seite laden
if main_select in utils.pages_1:
    utils.show_page(utils.pages_1[main_select])
elif health_select in utils.pages_2:
    utils.show_page(utils.pages_2[health_select])
else:
    st.write("In der Navigation kommst du weiter!")

#if __name__ == "__main__":
 #   st.write("App gestartet!")
