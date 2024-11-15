from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/mediatheque"
mongo = PyMongo(app)

# Route d'accueil
@app.route('/')
def index():
    documents = mongo.db.documents.find()
    documents_list = [
        {
            "titre": doc["titre"],
            "auteur": doc["auteur"],
            "genre": doc["genre"],
            "date_publication": doc["date_publication"],
            "disponibilite": doc["disponibilite"]
        } for doc in documents
    ]
    return render_template('index.html', documents=documents_list)

# Routes pour les abonnés

@app.route('/abonne')
def get_abonnes():
    abonnés = mongo.db.abonnes.find()
    abonnes_list = [
        {
            "nom": abonne["nom"],
            "prenom": abonne["prenom"],
            "adresse": abonne["adresse"],
            "date_inscription": abonne["date_inscription"]
        } for abonne in abonnés
    ]
    return render_template('abonne_list.html', abonnés=abonnes_list)

@app.route('/add_abonne', methods=['POST'])
def add_abonne():
    data = request.json
    nom = data.get('nom')
    prenom = data.get('prenom')
    adresse = data.get('adresse')
    date_inscription = data.get('date_inscription')

    if not all([nom, prenom, adresse, date_inscription]):
        return jsonify({"error": "Missing required fields"}), 400
    
    abonne_data = {
        "nom": nom,
        "prenom": prenom,
        "adresse": adresse,
        "date_inscription": date_inscription
    }
    mongo.db.abonnes.insert_one(abonne_data)
    return jsonify({"message": "Abonné ajouté avec succès!"}), 201

@app.route('/get_abonne/<abonne_id>', methods=['GET'])
def get_abonne(abonne_id):
    try:
        abonne = mongo.db.abonnes.find_one({"_id": ObjectId(abonne_id)})
        if abonne:
            abonne["_id"] = str(abonne["_id"])
            return jsonify(abonne), 200
        else:
            return jsonify({"error": "Abonné not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400


@app.route('/update_abonne/<abonne_id>', methods=['PUT'])
def update_abonne(abonne_id):
    try:
        data = request.json
        mongo.db.abonnes.update_one({"_id": ObjectId(abonne_id)}, {"$set": data})
        return jsonify({"message": "Abonné mis à jour avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/delete_abonne/<abonne_id>', methods=['DELETE'])
def delete_abonne(abonne_id):
    try:
        mongo.db.abonnes.delete_one({"_id": ObjectId(abonne_id)})
        return jsonify({"message": "Abonné supprimé avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

# Routes pour les documents
@app.route('/add_document', methods=['POST'])
def add_document():
    data = request.json
    titre = data.get('titre')
    auteur = data.get('auteur')
    genre = data.get('genre')
    date_publication = data.get('date_publication')
    disponibilite = data.get('disponibilite')

    if not all([titre, auteur, genre, date_publication, disponibilite]):
        return jsonify({"error": "Missing required fields"}), 400
    
    document_data = {
        "titre": titre,
        "auteur": auteur,
        "genre": genre,
        "date_publication": date_publication,
        "disponibilite": disponibilite
    }
    mongo.db.documents.insert_one(document_data)
    return jsonify({"message": "Document ajouté avec succès!"}), 201

@app.route('/get_document/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = mongo.db.documents.find_one({"_id": ObjectId(document_id)})
        if document:
            document["_id"] = str(document["_id"])
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/update_document/<document_id>', methods=['PUT'])
def update_document(document_id):
    try:
        data = request.json
        mongo.db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": data})
        return jsonify({"message": "Document mis à jour avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/delete_document/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        mongo.db.documents.delete_one({"_id": ObjectId(document_id)})
        return jsonify({"message": "Document supprimé avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400



# Routes pour les emprunts
@app.route('/add_emprunt', methods=['POST'])
def add_emprunt():
    data = request.json
    abonne_id = data.get('abonne_id')
    document_id = data.get('document_id')
    date_emprunt = data.get('date_emprunt')
    date_retour = data.get('date_retour')

    if not all([abonne_id, document_id, date_emprunt, date_retour]):
        return jsonify({"error": "Missing required fields"}), 400
    
    emprunt_data = {
        "abonne_id": abonne_id,
        "document_id": document_id,
        "date_emprunt": date_emprunt,
        "date_retour": date_retour
    }
    mongo.db.emprunts.insert_one(emprunt_data)
    return jsonify({"message": "Emprunt ajouté avec succès!"}), 201

@app.route('/get_emprunt/<emprunt_id>', methods=['GET'])
def get_emprunt(emprunt_id):
    try:
        emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(emprunt_id)})
        if emprunt:
            emprunt["_id"] = str(emprunt["_id"])
            return jsonify(emprunt), 200
        else:
            return jsonify({"error": "Emprunt not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/update_emprunt/<emprunt_id>', methods=['PUT'])
def update_emprunt(emprunt_id):
    try:
        data = request.json
        mongo.db.emprunts.update_one({"_id": ObjectId(emprunt_id)}, {"$set": data})
        return jsonify({"message": "Emprunt mis à jour avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route('/delete_emprunt/<emprunt_id>', methods=['DELETE'])
def delete_emprunt(emprunt_id):
    try:
        mongo.db.emprunts.delete_one({"_id": ObjectId(emprunt_id)})
        return jsonify({"message": "Emprunt supprimé avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
