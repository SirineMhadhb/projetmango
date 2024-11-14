from flask_pymongo import PyMongo

mongo = PyMongo()

# Modèle pour Abonné
class Abonne:
    def __init__(self, nom, prenom, adresse, date_inscription):
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.date_inscription = date_inscription
    
    def save(self):
        abonne_data = {
            "nom": self.nom,
            "prenom": self.prenom,
            "adresse": self.adresse,
            "date_inscription": self.date_inscription
        }
        mongo.db.abonnes.insert_one(abonne_data)

# Modèle pour Document
class Document:
    def __init__(self, titre, auteur, genre, date_publication, disponibilite):
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.date_publication = date_publication
        self.disponibilite = disponibilite
    
    def save(self):
        document_data = {
            "titre": self.titre,
            "auteur": self.auteur,
            "genre": self.genre,
            "date_publication": self.date_publication,
            "disponibilite": self.disponibilite
        }
        mongo.db.documents.insert_one(document_data)

# Modèle pour Emprunt
class Emprunt:
    def __init__(self, abonne_id, document_id, date_emprunt, date_retour):
        self.abonne_id = abonne_id
        self.document_id = document_id
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour
    
    def save(self):
        emprunt_data = {
            "abonne_id": self.abonne_id,
            "document_id": self.document_id,
            "date_emprunt": self.date_emprunt,
            "date_retour": self.date_retour
        }
        mongo.db.emprunts.insert_one(emprunt_data)

# Initialisation de l'application
def init_app(app):
    mongo.init_app(app)
