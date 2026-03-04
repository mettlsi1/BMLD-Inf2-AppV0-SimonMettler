import streamlit as st
import numpy as np
import pandas as pd         
import matplotlib.pyplot as plt

st.title("Halbwertszeit-Rechner")

with st.form("halbwertszeit_form"):
    hvz = st.number_input("Halbwertszeit eingeben:", min_value=0.0, step=0.1, format="%.6f")
    hvz_einheit = st.selectbox("Einheit der Halbwertszeit:", ["Jahre", "Tage", "Stunden", "Sekunden"])
    masse = st.number_input("Anfangsmasse eingeben:", min_value=0.0, step=0.1, format="%.6f")
    masse_einheit = st.selectbox("Einheit der Masse:", ["g", "kg"])
    submit = st.form_submit_button("Absenden")

if submit:
    if hvz <= 0:
        st.error("Bitte eine Halbwertszeit größer als 0 eingeben.")
    else:
        # Anfangsmasse immer in Gramm berechnen
        masse_g = masse * (1000.0 if masse_einheit == "kg" else 1.0)

        # Zeitachse (0 … 5×T½) und Zerfall
        t_end = hvz * 5
        t = np.linspace(0, t_end, 20)           
        mass_t = masse_g * 0.5 ** (t / hvz)
        pct = mass_t / masse_g * 100                    

        # Plot
        fig, ax = plt.subplots()
        ax.plot(t, mass_t, label="Masse")
        ax.set_xlabel(f"Zeit ({hvz_einheit})")
        ax.set_ylabel("Masse (g)")
        ax.set_title("Zerfall der Masse über die Zeit")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Tabelle mit Prozent und beiden Masseeinheiten
        df = pd.DataFrame({
            f"Zeit ({hvz_einheit})": t,
            "Masse (g)": mass_t,
            "Masse (kg)": mass_t / 1000,
            "Verbleib (%)": pct
        })

        st.markdown("### Verbleibende Masse nach bestimmten Zeitabständen")
        st.dataframe(df.style.format({
            "Masse (g)": "{:.3f}",
            "Masse (kg)": "{:.6f}",
            "Verbleib (%)": "{:.2f}"
        }))

        st.write(f"Anfangsmasse: {masse} {masse_einheit} ({masse_g:.6g} g)")
