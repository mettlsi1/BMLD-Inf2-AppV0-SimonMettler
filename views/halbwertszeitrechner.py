import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_manager import DataManager

data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_HWZR")

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

        # Tabelle mit 20 Einträgen in 5%-Abständen (100%, 95%, 90%, ..., 5%)
        table_data = []
        zeit_col = f"Zeit ({hvz_einheit})"
        for percentage in range(100, -5, -5):
            # M(t) = M0 * 0.5^(t/T) => 0.5^(t/T) = percentage/100 => t = T * log(percentage/100) / log(0.5)
            if percentage > 0:
                t_val = hvz * np.log(percentage / 100.0) / np.log(0.5)
                t_display = f"{t_val:.6g}"
            else:
                t_display = "∞"

            remaining_mass_g = masse_g * (percentage / 100.0)
            remaining_mass_original = remaining_mass_g / (1000.0 if masse_einheit == "kg" else 1.0)

            table_data.append({
                zeit_col: t_display,
                f"Masse ({masse_einheit})": f"{remaining_mass_original:.6g}",
                "Masse (g)": f"{remaining_mass_g:.6g}",
                "% der Anfangsmasse": f"{percentage}%"
            })

        df = pd.DataFrame(table_data)

        st.markdown("### Ergebnis-Tabelle")
        st.dataframe(df, use_container_width=True)

        st.write(f"**Anfangsmasse:** {masse} {masse_einheit} ({masse_g:.6g} g)")


        # --- history update session state ---
        result = {
            "Halbwertszeit": hvz,
            "Einheit HWZ": hvz_einheit,
            "Anfangsmasse": masse,
            "Einheit Masse": masse_einheit,
            "Anfangsmasse (g)": masse_g,
            "Berechnungszeit": str(pd.Timestamp.now()),  # optional: Datum/Uhrzeit
        }

 # --- Daten auf DataManager speichern ---
        data_manager.save_user_data(st.session_state['data_df'], 'data.csv')

        st.session_state['data_df'] = pd.concat(
        [st.session_state['data_df'], pd.DataFrame([result])],
        ignore_index=True
        )
       
st.markdown("### Verlauf / Session-Historie")
st.dataframe(st.session_state['data_df'], width='stretch')

# --- Grafik der gespeicherten Daten ---
if not st.session_state['data_df'].empty:
    st.markdown("### Grafik der Halbwertszeit-Berechnungen")
    
    # Daten vorbereiten (Einheiten berücksichtigen – Annahme: alles in g und Jahren für Einfachheit)
    plot_df = st.session_state['data_df'].copy()
    # Einheiten normalisieren (z. B. Tage zu Jahren umrechnen, kg zu g)
    plot_df['Halbwertszeit_norm'] = plot_df.apply(
        lambda row: row['Halbwertszeit'] if row['Einheit HWZ'] == 'Jahre' 
        else row['Halbwertszeit'] / 365 if row['Einheit HWZ'] == 'Tage' 
        else row['Halbwertszeit'] / (365 * 24) if row['Einheit HWZ'] == 'Stunden' 
        else row['Halbwertszeit'] / (365 * 24 * 3600), axis=1
    )
    
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(
        plot_df['Halbwertszeit_norm'], 
        plot_df['Anfangsmasse (g)'], 
        c=plot_df['Einheit HWZ'].astype('category').cat.codes,  # Farbkodierung nach Einheit
        cmap='viridis', 
        alpha=0.7
    )
    ax.set_xlabel("Halbwertszeit (Jahre)")
    ax.set_ylabel("Anfangsmasse (g)")
    ax.set_title("Scatterplot: Halbwertszeit vs. Anfangsmasse")
    ax.grid(True)
    
    # Legende für Farben
    handles, labels = scatter.legend_elements(prop="colors", alpha=0.7)
    ax.legend(handles, plot_df['Einheit HWZ'].unique(), title="Einheit HWZ")
    
    st.pyplot(fig)
else:
    st.info("Noch keine Daten vorhanden – führe eine Berechnung durch, um die Grafik zu sehen.")