import pandas as pd
import streamlit as st
from utils.data_manager import DataManager

# --- importieren und initialisieren des DataManagers ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_App_HWZR"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in


# --- user data laden, falls noch nicht vorhanden neue erstellen --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
    'data.csv',                     # The file on switch drive where the data is stored
    initial_value=pd.DataFrame()    # Initial value if the file does not exist
)

st.set_page_config(page_title="Halbwertszeitrechner", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/halbwertszeitrechner.py", title="Halbwertszeit-Rechner", icon="☢️")

pg = st.navigation([pg_home, pg_second])
pg.run()
