import streamlit as st

st.title("Halbwertszeit-Rechner")

# Eingabefeld für Halbwertszeit
halbwertszeit = st.number_input("Halbwertszeit eingeben (in Jahren):", min_value=0.0, step=0.1)

st.write(f"Eingegebene Halbwertszeit: {halbwertszeit}")