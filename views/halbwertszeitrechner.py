import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Halbwertszeit-Rechner")

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
        masse_g = masse * (1000.0 if masse_einheit == "kg" else 1.0)

        t_end = hvz * 10
        t = np.linspace(0, t_end, 500)
        mass_t = masse_g * 0.5 ** (t / hvz)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(t, mass_t, label="Masse")
        ax.set_xlabel(f"Zeit ({hvz_einheit})")
        ax.set_ylabel("Masse (g)")
        ax.set_title("Zerfall der Masse über die Zeit")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Intelligente Zeitabstände bestimmen basierend auf Halbwertszeit
        time_intervals = []
        labels = []

        if hvz_einheit == "Sekunden":
            time_intervals = [0, 1, 5, 10, 30, 60, 300, 600, 3600]
            labels = ["0s", "1s", "5s", "10s", "30s", "1min", "5min", "10min", "1h"]
        elif hvz_einheit == "Stunden":
            time_intervals = [0, 0.5, 1, 2, 6, 12, 24, 48, 96]
            labels = ["0h", "30min", "1h", "2h", "6h", "12h", "1d", "2d", "4d"]
        elif hvz_einheit == "Tage":
            time_intervals = [0, 1, 7, 14, 30, 60, 90, 180, 365]
            labels = ["0d", "1d", "1w", "2w", "1mo", "2mo", "3mo", "6mo", "1y"]
        elif hvz_einheit == "Jahre":
            time_intervals = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
            labels = ["0y", "1y", "10y", "100y", "1ky", "10ky", "100ky", "1My", "10My"]

        # Tabelle erstellen
        table_data = []
        for t_val, label in zip(time_intervals, labels):
            remaining_mass_g = masse_g * 0.5 ** (t_val / hvz)
            remaining_mass_original = remaining_mass_g / (1000.0 if masse_einheit == "kg" else 1.0)
            percentage = (remaining_mass_g / masse_g) * 100

            table_data.append({
                "Zeit": label,
                f"Masse ({masse_einheit})": f"{remaining_mass_original:.6g}",
                "Masse (g)": f"{remaining_mass_g:.6g}",
                "% der Anfangsmasse": f"{percentage:.2f}%"
            })

        df = pd.DataFrame(table_data)

        st.markdown("### Ergebnis-Tabelle")
        st.dataframe(df, use_container_width=True)

        st.write(f"**Anfangsmasse:** {masse} {masse_einheit} ({masse_g:.6g} g)")