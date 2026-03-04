import streamlit as st

st.title("Halbwertszeit-Rechner")

# Eingabefeld für Halbwertszeit
halbwertszeit = st.number_input("Halbwertszeit eingeben (in Jahren):", min_value=0.0, step=0.1)

st.write(f"Eingegebene Halbwertszeit: {halbwertszeit}")


# Eingabeformular für Halbwertszeit
with st.form("halbwertszeit_form"):
    hvz = st.number_input("Halbwertszeit eingeben:", min_value=0.0, step=0.1, format="%.6f")
    einheit = st.selectbox("Einheit:", ["Jahre", "Tage", "Stunden", "Sekunden"])
    submit = st.form_submit_button("Absenden")

if submit:
    multipliers = {"Jahre": 1, "Tage": 1/365, "Stunden": 1/(365*24), "Sekunden": 1/(365*24*3600)}
    hvz_jahre = hvz * multipliers[einheit]
    st.write(f"Eingegebene Halbwertszeit: {hvz} {einheit}  —  ({hvz_jahre:.6g} Jahre)")