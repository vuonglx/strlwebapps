import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  

import yaml
from yaml.loader import SafeLoader

# --- USER AUTHENTICATION ---

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Ensure the location is one of the allowed values
authenticator.login()


if st.session_state['authentication_status']:
    
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    # --- PAGE SETUP ---
    # authenticator.logout()
    # authenticator.logout("Logout", "sidebar")
    # # --- PAGE SETUP ---
    about_page = st.Page(
        "views/about_me.py",
        title="About Me",
        icon=":material/account_circle:",
        default=True,
    )
    project_1_page = st.Page(
        "views/sales_dashboard.py",
        title="Sales Dashboard",
        icon=":material/bar_chart:",
    )
    project_2_page = st.Page(
        "views/chatbot.py",
        title="Chat Bot",
        icon=":material/smart_toy:",
    )


    # --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
    # pg = st.navigation(pages=[about_page, project_1_page, project_2_page])
    # Show "Info" for admin role only
    # --- NAVIGATION SETUP [WITH SECTIONS]---
    # if roles contain 'admin', show "Info" section
    if 'admin' in st.session_state['roles']:
        pg = st.navigation(
            {
                "Info": [about_page],
                "Projects": [project_1_page, project_2_page],
            }
        )
    else:
        pg = st.navigation(
            {   
                "Projects": [project_1_page, project_2_page],
            }
        )

    # # --- SHARED ON ALL PAGES ---
    st.logo("assets/logo.png")
    
    
    # if st.sidebar.button('Reset Password'):
    if st.session_state['authentication_status']:
        try:
            if authenticator.reset_password(st.session_state['username'],'sidebar'):
                st.success('Password modified successfully')
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    authenticator.logout('Logout','sidebar')
    st.sidebar.markdown("Updated with ❤️ by Vuong ")
    # # --- RUN NAVIGATION ---
    pg.run()

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

