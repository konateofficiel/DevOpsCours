# tasks.py - Gestion des tâches
import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.title("Gestion des tâches")

if "token" not in st.session_state:
    st.warning("Veuillez vous connecter.")
    st.switch_page("login.py")

# Ajout de tâche
st.header("Ajouter une tâche")
titre = st.text_input("Titre")
description = st.text_area("Description")
date_echeance = st.date_input("Date d'échéance")

if st.button("Ajouter"):
    data = {
        "titre": titre,
        "description": description,
        "date_echeance": str(date_echeance),
    }
    response = requests.post(f"{API_URL}/taches/", json=data, headers=get_headers())
    if response.status_code == 200:
        st.success("Tâche ajoutée avec succès")
    else:
        st.error("Erreur lors de l'ajout")

# Liste des tâches
st.header("Mes tâches")
response = requests.get(f"{API_URL}/taches", headers=get_headers())
if response.status_code == 200:
    for tache in response.json():
        st.write(f"**{tache['titre']}** - {tache['description']} - {tache['date_echeance']}")
        if st.button(f"Supprimer {tache['id']}"):
            requests.delete(f"{API_URL}/tache/{tache['id']}", headers=get_headers())
            st.rerun()
else:
    st.error("Erreur de récupération des tâches")


