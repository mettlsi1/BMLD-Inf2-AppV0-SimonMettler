import streamlit as st

st.title("Halbwertszeit-Rechner")


# Eingabeformular für Halbwertszeit
with st.form("halbwertszeit_form"):
    hvz = st.number_input("Halbwertszeit eingeben:", min_value=0.0, step=0.1, format="%.6f")
    einheit = st.selectbox("Einheit:", ["Jahre", "Tage", "Stunden", "Sekunden"])
    submit = st.form_submit_button("Absenden")

if submit:
    multipliers = {"Jahre": 1, "Tage": 1/365, "Stunden": 1/(365*24), "Sekunden": 1/(365*24*3600)}
    hvz_jahre = hvz * multipliers[einheit]
    st.write(f"Eingegebene Halbwertszeit: {hvz} {einheit}  —  ({hvz_jahre:.6g} Jahre)")

    # Eingabeformular für Halbwertszeit und Masse
with st.form("halbwertszeit_form"):
    hvz = st.number_input("Halbwertszeit eingeben:", min_value=0.0, step=0.1, format="%.6f")
    hvz_einheit = st.selectbox("Einheit der Halbwertszeit:", ["Jahre", "Tage", "Stunden", "Sekunden"])
    masse = st.number_input("Anfangsmasse eingeben:", min_value=0.0, step=0.1, format="%.6f")
    masse_einheit = st.selectbox("Einheit der Masse:", ["g", "kg"])
    submit = st.form_submit_button("Absenden")

if submit:
    # Masse in Gramm umrechnen
    masse_g = masse * (1000.0 if masse_einheit == "kg" else 1.0)
    st.write(f"Eingegebene Halbwertszeit: {hvz} {hvz_einheit}")
    st.write(f"Anfangsmasse: {masse} {masse_einheit} ({masse_g:.6g} g)")