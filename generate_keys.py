import pickle
from pathlib import Path

import streamlit_authenticator as stauth

credentials = {
    "usernames": {
        "pparker": {
            "name": "Peter Parker",
            "password": "DuongLuu@81"
        },
        "rmiller": {
            "name": "Rebecca Miller",
            "password": "Kpmg@2024"
        }
    }
}

hashed_credentials = stauth.Hasher.hash_passwords(credentials)

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_credentials, file)