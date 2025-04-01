from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ✅ Schéma pour la création d'un utilisateur
class UtilisateurCreate(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str


# ✅ Schéma pour la réponse utilisateur (sans mot de passe)
class UtilisateurResponse(BaseModel):
    id: int
    nom: str
    email: EmailStr

    class Config:
        from_attributes = True


# ✅ Schéma pour la création d'une tâche
class TacheCreate(BaseModel):
    titre: str
    description: str
    date_echeance: Optional[datetime] = None
    utilisateur_id: int


# ✅ Schéma pour la réponse d'une tâche
class TacheResponse(BaseModel):
    id: int
    titre: str
    description: str
    statut: str
    date_creation: datetime
    date_echeance: Optional[datetime] = None
    utilisateur_id: int

    class Config:
        from_attributes = True


# ✅ Schéma pour la requête de connexion
class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str

