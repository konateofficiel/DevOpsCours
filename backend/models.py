from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import database


class Utilisateur(database.Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)

    taches = relationship("Tache", back_populates="utilisateur")


class Tache(database.Base):
    __tablename__ = "taches"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    description = Column(String)
    statut = Column(Enum('à faire', 'en cours', 'terminée', name='statut_enum'))
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_echeance = Column(DateTime, nullable=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))
    parent_tache_id = Column(Integer, ForeignKey('taches.id'), nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="taches")
    parent_tache = relationship("Tache", remote_side=[id])
    sous_taches = relationship("Tache", back_populates="parent_tache")
