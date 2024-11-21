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
            "id": str(doc["_id"]),  # Convert ObjectId en chaîne
            "titre": doc["titre"],
            "auteur": doc["auteur"],
            "genre": doc["genre"],
            "date_publication": doc["date_publication"],
            "disponibilite": doc["disponibilite"]
        } for doc in documents
    ]
    return render_template('abonne.html', documents=documents_list)

# Routes pour les abonnés
@app.route('/abonne')
def get_abonnes():
    abonnés = mongo.db.abonnes.find()
    abonnes_list = [
        {
            "id": str(abonne["_id"]),  # Convert ObjectId en chaîne
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
    try:
        mongo.db.abonnes.insert_one(data)
        return jsonify({"message": "Abonné ajouté avec succès!"}), 201
    except Exception as e:
        app.logger.error(f"Error adding abonne: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/get_abonne/<id>', methods=['GET'])
def get_abonne(id):
    try:
        abonne_id = ObjectId(id)
        abonne = mongo.db.abonnes.find_one({"_id": abonne_id})
        if abonne:
            abonne["_id"] = str(abonne["_id"])  # Convertir l'ObjectId en chaîne avant de le retourner
            return jsonify(abonne), 200
        else:
            return jsonify({"error": "Abonné non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": "Erreur lors de la récupération de l'abonné"}), 500

@app.route('/update_abonne/<id>', methods=['PUT'])
def update_abonne(id):
    data = request.json
    try:
        abonne_id = ObjectId(id)
        mongo.db.abonnes.update_one({"_id": abonne_id}, {"$set": data})
        return jsonify({"message": "Abonné mis à jour avec succès!"})
    except Exception as e:
        return jsonify({"error": "Erreur lors de la mise à jour de l'abonné"}), 500

@app.route('/delete_abonne/<id>', methods=['DELETE'])
def delete_abonne(id):
    try:
        abonne_id = ObjectId(id)
        mongo.db.abonnes.delete_one({"_id": abonne_id})
        return jsonify({"message": "Abonné supprimé avec succès!"})
    except Exception as e:
        return jsonify({"error": "Erreur lors de la suppression de l'abonné"}), 500

# Routes pour les documents
@app.route('/documents')
def get_documents():
    documents = mongo.db.documents.find()
    documents_list = [
        {
            "id": str(doc["_id"]),
            "titre": doc["titre"],
            "auteur": doc["auteur"],
            "genre": doc["genre"],
            "date_publication": doc["date_publication"],
            "disponibilite": doc["disponibilite"]
        } for doc in documents
    ]
    return render_template('document_list.html', documents=documents_list)

@app.route('/add_document', methods=['POST'])
def add_document():
    data = request.json
    try:
        mongo.db.documents.insert_one(data)
        return jsonify({"message": "Document ajouté avec succès!"}), 201
    except Exception as e:
        app.logger.error(f"Error adding document: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/get_document/<id>', methods=['GET'])
def get_document(id):
    try:
        document_id = ObjectId(id)
        document = mongo.db.documents.find_one({"_id": document_id})
        if document:
            document["_id"] = str(document["_id"])
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": "Erreur lors de la récupération du document"}), 500

@app.route('/update_document/<id>', methods=['PUT'])
def update_document(id):
    data = request.json
    try:
        document_id = ObjectId(id)
        mongo.db.documents.update_one({"_id": document_id}, {"$set": data})
        return jsonify({"message": "Document mis à jour avec succès!"})
    except Exception as e:
        return jsonify({"error": "Erreur lors de la mise à jour du document"}), 500

@app.route('/delete_document/<id>', methods=['DELETE'])
def delete_document(id):
    try:
        document_id = ObjectId(id)
        mongo.db.documents.delete_one({"_id": document_id})
        return jsonify({"message": "Document supprimé avec succès!"})
    except Exception as e:
        return jsonify({"error": "Erreur lors de la suppression du document"}), 500

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
            return jsonify({"error": "Emprunt non trouvé"}), 404
    except Exception:
        return jsonify({"error": "Erreur lors de la récupération de l'emprunt"}), 500

@app.route('/update_emprunt/<emprunt_id>', methods=['PUT'])
def update_emprunt(emprunt_id):
    try:
        data = request.json
        mongo.db.emprunts.update_one({"_id": ObjectId(emprunt_id)}, {"$set": data})
        return jsonify({"message": "Emprunt mis à jour avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Erreur lors de la mise à jour de l'emprunt"}), 500

@app.route('/delete_emprunt/<emprunt_id>', methods=['DELETE'])
def delete_emprunt(emprunt_id):
    try:
        mongo.db.emprunts.delete_one({"_id": ObjectId(emprunt_id)})
        return jsonify({"message": "Emprunt supprimé avec succès!"}), 200
    except Exception:
        return jsonify({"error": "Erreur lors de la suppression de l'emprunt"}), 500

if __name__ == '__main__':
    app.run(debug=True)
