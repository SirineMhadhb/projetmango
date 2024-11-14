from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from models import Abonne, Document, Emprunt, init_app

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialiser la connexion MongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mediatheque")

@app.route('/')
def Homme():
    documents = mongo.db.documents.find()
    return "hello"
         #render_template('index.html', documents=documents)


@app.route('/add_abonne', methods=['GET', 'POST'])
def add_abonne():
    if request.method == 'POST':
        try:
            # Utiliser request.json pour obtenir les données JSON envoyées en POST
            data = request.json
            nom = data.get('nom')
            prenom = data.get('prenom')
            adresse = data.get('adresse')
            date_inscription = data.get('date_inscription')

            # Imprimer les données pour déboguer
            print(f"Received data: nom={nom}, prenom={prenom}, adresse={adresse}, date_inscription={date_inscription}")
            
            # Vérifier si tous les champs nécessaires sont fournis
            if not nom or not prenom or not adresse or not date_inscription:
                return jsonify({"error": "Missing required fields"}), 400
            
            # Créer un nouvel Abonne et l'enregistrer dans MongoDB
            abonne = Abonne(nom, prenom, adresse, date_inscription)
            abonne.save()  # Sauvegarder les données dans MongoDB
            return jsonify({"message": "Abonne ajouté avec succès!"}), 201
        except Exception as e:
            print(f"Error during form processing: {str(e)}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    return render_template('add_abonne.html')
@app.route('/add_document', methods=['GET', 'POST'])
def add_document():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        date_publication = request.form['date_publication']
        disponibilite = request.form.get('disponibilite') == 'on'
        
        # Créer et sauvegarder le document
        document = Document(titre, auteur, genre, date_publication, disponibilite)
        document.save()
        
        return redirect(url_for('index'))
    
    genres = ['Classique', 'Science-fiction', 'Fantastique', 'Roman', 'Histoire']
    return render_template('add_document.html', genres=genres)

@app.route('/add_emprunt', methods=['POST'])
def add_emprunt():
    if request.method == 'POST':
        abonne_id = request.json.get('abonne_id')
        document_id = request.json.get('document_id')
        date_emprunt = request.json.get('date_emprunt')
        date_retour = request.json.get('date_retour')
        
        if not abonne_id or not document_id or not date_emprunt or not date_retour:
            return jsonify({"error": "Tous les champs sont requis"}), 400
        
        # Créer et sauvegarder l'emprunt
        emprunt = Emprunt(abonne_id, document_id, date_emprunt, date_retour)
        emprunt.save()
        
        return jsonify({"message": "Emprunt ajouté avec succès!"}), 201

@app.route('/emprunts', methods=['GET'])
def get_emprunts():
    emprunts = mongo.db.emprunts.find()
    emprunts_list = []
    for emprunt in emprunts:
        emprunts_list.append({
            "abonne_id": emprunt["abonne_id"],
            "document_id": emprunt["document_id"],
            "date_emprunt": emprunt["date_emprunt"],
            "date_retour": emprunt["date_retour"]
        })
    return jsonify(emprunts_list)

@app.route('/test_insert_abonne')
def test_insert_abonne():
    try:
        abonne_data = {
            "nom": "Test",
            "prenom": "Test",
            "adresse": "Test Address",
            "date_inscription": "2024-11-14"
        }
        mongo.db.abonnes.insert_one(abonne_data)
        return "Test Abonne inserted successfully!"
    except Exception as e:
        return f"Error inserting Abonne: {str(e)}"

# Méthode save() pour l'Abonne
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
        
        try:
            mongo.db.abonnes.insert_one(abonne_data)
            print(f"Abonne data inserted: {abonne_data}")
        except Exception as e:
            print(f"Error saving Abonne: {e}")
            raise

def add_document():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        date_publication = request.form['date_publication']
        disponibilite = request.form.get('disponibilite') == 'on'
        
        # Créer et sauvegarder le document
        document = Document(titre, auteur, genre, date_publication, disponibilite)
        document.save()
        
        return redirect(url_for('index'))
    
    # Définir les genres sous forme de tableau
    genres = ['Classique', 'Science-fiction', 'Fantastique', 'Roman', 'Histoire']
    
    # Passer le tableau des genres au template
    return render_template('add_document.html', genres=genres)


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

        try:
            mongo.db.emprunts.insert_one(emprunt_data)
            print(f"Emprunt inserted: {emprunt_data}")
        except Exception as e:
            print(f"Error saving Emprunt: {e}")
            raise


if __name__ == '__main__':
    app.run(debug=True)
