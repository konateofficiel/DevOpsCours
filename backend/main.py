from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List, Optional
import os

from models import Tache, Utilisateur
from database import get_db, Base, engine
from schema import TacheCreate, TacheResponse, UtilisateurCreate, UtilisateurResponse, LoginRequest

app = FastAPI()


# Création des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# 🔐 Gestion du hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ========================== UTILISATEURS ========================== #

@app.post("/utilisateurs/", response_model=UtilisateurResponse)
def create_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    db_user = db.query(Utilisateur).filter(Utilisateur.email == utilisateur.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="L'email est déjà utilisé.")

    # Hashage du mot de passe
    hashed_password = pwd_context.hash(utilisateur.mot_de_passe)

    db_utilisateur = Utilisateur(
        nom=utilisateur.nom,
        email=utilisateur.email,
        mot_de_passe=hashed_password,
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur


@app.get("/utilisateurs/{utilisateur_id}", response_model=UtilisateurResponse)
def get_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur


@app.get("/utilisateurs/", response_model=List[UtilisateurResponse])
def get_all_utilisateurs(db: Session = Depends(get_db)):
    return db.query(Utilisateur).all()


@app.delete("/utilisateurs/{utilisateur_id}", response_model=UtilisateurResponse)
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.delete(utilisateur)
    db.commit()
    return utilisateur

@app.post("/login/")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == login_data.email).first()
    
    if not utilisateur or not pwd_context.verify(login_data.mot_de_passe, utilisateur.mot_de_passe):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    return {"message": "Connexion réussie", "utilisateur": utilisateur}




# ========================== TÂCHES ========================== #

@app.post("/taches/", response_model=TacheResponse)
def create_tache(tache: TacheCreate, db: Session = Depends(get_db)):
    db_tache = Tache(
        titre=tache.titre,
        description=tache.description,
        date_echeance=tache.date_echeance,
        utilisateur_id=tache.utilisateur_id,
        statut="à faire"
    )
    db.add(db_tache)
    db.commit()
    db.refresh(db_tache)
    return db_tache


@app.get("/taches/{utilisateur_id}", response_model=List[TacheResponse])
def get_taches(utilisateur_id: int, db: Session = Depends(get_db)):
    return db.query(Tache).filter(Tache.utilisateur_id == utilisateur_id).all()


@app.get("/tache/{tache_id}", response_model=TacheResponse)
def get_tache(tache_id: int, db: Session = Depends(get_db)):
    tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return tache


@app.put("/tache/{tache_id}", response_model=TacheResponse)
def update_tache_status(tache_id: int, statut: str, db: Session = Depends(get_db)):
    db_tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db_tache.statut = statut
    db.commit()
    db.refresh(db_tache)
    return db_tache


@app.delete("/tache/{tache_id}", response_model=TacheResponse)
def delete_tache(tache_id: int, db: Session = Depends(get_db)):
    db_tache = db.query(Tache).filter(Tache.id == tache_id).first()
    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    db.delete(db_tache)
    db.commit()
    return db_tache


# 🚀 Lancer FastAPI avec Uvicorn
if __name__ == "__main__":
    os.system("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

