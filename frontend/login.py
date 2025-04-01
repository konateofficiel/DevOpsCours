import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000"

st.title("To-Do List - Connexion & Inscription")

# Barre latérale pour la navigation
menu = st.sidebar.selectbox("Menu", ["Connexion", "Inscription"])

# ✅ Connexion utilisateur
if menu == "Connexion":
    st.subheader("Se connecter")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        response = requests.post(f"{API_URL}/login", json={"email": email, "mot_de_passe": password})
        
        if response.status_code == 200:
            data = response.json()  # Récupération de la réponse JSON
            utilisateur = data["utilisateur"]  # Récupération de l'utilisateur
            
            # Stockage des informations de l'utilisateur dans session_state
            st.session_state["utilisateur_id"] = utilisateur["id"]
            st.session_state["nom"] = utilisateur["nom"]
            st.session_state["email"] = utilisateur["email"]
            
            # Afficher un message de bienvenue
            st.success(f"Bienvenue, {utilisateur['nom']} !")

            st.switch_page("pages/app.py")
            
        else:
            st.error("Identifiants incorrects")

# ✅ Inscription utilisateur
elif menu == "Inscription":
    st.subheader("Créer un compte")
    nom = st.text_input("Nom")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("S'inscrire"):
        response = requests.post(f"{API_URL}/utilisateurs/", json={"nom": nom, "email": email, "mot_de_passe": password})
        
        if response.status_code == 200:
            st.success("Inscription réussie. Vous pouvez maintenant vous connecter.")
        else:
            st.error("Erreur lors de l'inscription, veuillez réessayer.")
