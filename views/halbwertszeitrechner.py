import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


    # Eingabeformular für Halbwertszeit und Masse
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
        # Masse in Gramm umrechnen
        masse_g = masse * (1000.0 if masse_einheit == "kg" else 1.0)

        # Zeitachse in derselben Einheit wie die Halbwertszeit (0 bis 10 Halbwertszeiten)
        t_end = hvz * 10
        t = np.linspace(0, t_end, 500)

        # Zerfall: M(t) = M0 * (1/2)^(t / T_half)
        mass_t = masse_g * 0.5 ** (t / hvz)

        # Plot erstellen
        fig, ax = plt.subplots()
        ax.plot(t, mass_t, label="Masse")
        ax.set_xlabel(f"Zeit ({hvz_einheit})")
        ax.set_ylabel("Masse (g)")
        ax.set_title("Zerfall der Masse über die Zeit")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

        # Tabelle erzeugen
        df = pd.DataFrame({
            f"Zeit ({hvz_einheit})": t,
            "Masse (g)": mass_t
        })

        st.write(f"Anfangsmasse: {masse} {masse_einheit} ({masse_g:.6g} g)")
        st.write("Tabelle der Masse über die Zeit:")
        st.dataframe(df)