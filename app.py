from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from flask import request, redirect, url_for, flash

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/mediatheque"
app.secret_key = 'votre_cle_secrète'
mongo = PyMongo(app)







# Route d'accueil
@app.route('/')
def index():
    documents = mongo.db.documents.find()
    documents_list = [
        {
            "id": str(doc["_id"]),  
            "auteur": doc["auteur"],
            "genre": doc["genre"],
            "date_publication": doc["date_publication"],
            "disponibilite": doc["disponibilite"]
        } for doc in documents
    ]
    return render_template('login.html', documents=documents_list)

@app.route('/dashboard')
def dashboard():
    emprunts = get_emprunts(mongo)  # Utilisez la fonction définie
    total_emprunts = len(emprunts)
    total_abonnes = mongo.db.abonnes.count_documents({})
    total_documents = mongo.db.documents.count_documents({})
    total_genres = mongo.db.genres.count_documents({})

    # Calcul de la disponibilité des documents
    documents_disponibles = mongo.db.documents.count_documents({'disponibilite': 'Disponible'})
    documents_non_disponibles = mongo.db.documents.count_documents({'disponibilite': 'Indisponible'})
   
    # Passer les données au template
    return render_template('dashboard.html', 
                           emprunts=emprunts,
                           total_emprunts=total_emprunts,
                           total_abonnes=total_abonnes,
                           total_documents=total_documents,
                           total_genres=total_genres,
                           documents_disponibles=documents_disponibles,
                           documents_non_disponibles=documents_non_disponibles,
                          )

@app.route('/abonne')
def get_abonnes():
    abonnés = mongo.db.abonnes.find()
    abonnes_list = [
        {
            "id": str(abonne["_id"]),  
            "nom": abonne["nom"],
            "prenom": abonne["prenom"],
            "adresse": abonne["adresse"],
            "date_inscription": abonne["date_inscription"]
        } for abonne in abonnés
    ]
    return render_template('abonne_list.html', abonnés=abonnes_list)


@app.route('/getabonne')
def get_abonness():
    abonnés = mongo.db.abonnes.find()
    abonnes_list = [
        {
            "id": str(abonne["_id"]),  
            "nom": abonne["nom"],
            "prenom": abonne["prenom"],
            "adresse": abonne["adresse"],
            "date_inscription": abonne["date_inscription"]
        } for abonne in abonnés
    ]
    return jsonify({"abonnes": abonnes_list})

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
    # Validate if the id is a valid ObjectId
    if not ObjectId.is_valid(id):
        return jsonify({"error": "ID invalide"}), 400
    
    try:
        abonne_id = ObjectId(id)
        abonne = mongo.db.abonnes.find_one({"_id": abonne_id})
        if abonne:
            abonne["_id"] = str(abonne["_id"])  # Convertir ObjectId en chaîne
            return jsonify(abonne), 200
        else:
            return jsonify({"error": "Abonné non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur: {str(e)}"}), 500
    

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
        
        # Supprimer les emprunts associés à cet abonné
        mongo.db.emprunts.delete_many({"abonne_id": str(abonne_id)})
        
        # Supprimer l'abonné
        mongo.db.abonnes.delete_one({"_id": abonne_id})
        
        return jsonify({"message": "Abonné et ses emprunts associés supprimés avec succès!"})
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression de l'abonné: {e}"}), 500

@app.route('/delete_document/<id>', methods=['DELETE'])
def delete_document(id):
    try:
        document_id = ObjectId(id)
        
        # Supprimer les emprunts associés à ce document
        mongo.db.emprunts.delete_many({"document_id": str(document_id)})
        
        # Supprimer le document
        mongo.db.documents.delete_one({"_id": document_id})
        
        return jsonify({"message": "Document et ses emprunts associés supprimés avec succès!"})
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression du document: {e}"}), 500


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

@app.route('/ajouter_document', methods=['POST'])
def ajouter_document():
    data = request.json
    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    document = data.get("document")
    if not document:
        return jsonify({"error": "Le champ 'document' est requis"}), 400

    # Si vous avez un _id dans le document, il faut le convertir en chaîne
    if "_id" in document:
        document["_id"] = str(document["_id"])

    print("Document à insérer:", document)  # Affiche le document avant insertion

    try:
        result = mongo.db.documents.insert_one(document)
        # Convertir _id en chaîne dans la réponse avant de renvoyer
        document["_id"] = str(result.inserted_id)  # Convertir l'ID généré en chaîne
        return jsonify({"message": "Document ajouté avec succès", "document": document}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'ajout du document: {str(e)}"}), 500

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
    



@app.route('/get_documents_disponibles')
def get_documents_disponibles():
    documents = mongo.db.documents.find({"disponibilite": "oui"})  
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
    return jsonify({"documents": documents_list})

# # Route pour récupérer tous les emprunts
# @app.route('/emprunts', methods=['GET'])
# def get_emprunts():
#     emprunts = mongo.db.emprunts.find()
#     emprunts_list = [
#         {
#             "id": str(emprunt["_id"]),
#             "abonne_id": emprunt["abonne_id"],
#             "document_id": emprunt["document_id"],
#             "date_emprunt": emprunt["date_emprunt"],
#             "date_retour": emprunt["date_retour"]
#         } for emprunt in emprunts
#     ]
#     return render_template('emprunt_list.html', emprunts=emprunts_list), 200

# Route pour ajouter un emprunt


from datetime import datetime

def update_status_retard():
    # Récupérer les emprunts où la date de retour est dépassée et le statut n'est pas encore "retard"
    emprunts = mongo.db.emprunts.find({
        "status": {"$ne": "retard"}
    })

    for emprunt in emprunts:
        try:
            # Convertir date_retour en objet datetime
            date_retour = datetime.strptime(emprunt["date_retour"], "%Y-%m-%d")
            
            # Vérifier si la date est dépassée
            if date_retour < datetime.now():
                # Mettre à jour le statut en "retard"
                mongo.db.emprunts.update_one(
                    {"_id": emprunt["_id"]},
                    {"$set": {"status": "retard"}}
                )
        except ValueError:
            print(f"Erreur de format pour la date de retour: {emprunt['date_retour']}")

@app.route('/emprunts')
def get_emprunts():
    # Met à jour les statuts si nécessaire
    update_status_retard()

    emprunts = mongo.db.emprunts.find()
    emprunt_list = []

    for emprunt in emprunts:
        abonne_id = emprunt.get("abonne_id")
        document_id = emprunt.get("document_id")

        # Vérification de la validité des IDs
        abonne = mongo.db.abonnes.find_one({"_id": ObjectId(abonne_id)}) if ObjectId.is_valid(abonne_id) else None
        document = mongo.db.documents.find_one({"_id": ObjectId(document_id)}) if ObjectId.is_valid(document_id) else None

        # Ajouter l'emprunt à la liste
        emprunt_list.append({
            "id": str(emprunt["_id"]),
            "abonne_nom": f"{abonne['nom']} {abonne['prenom']}" if abonne else "Abonné introuvable",
            "document_titre": document["titre"] if document else "Document introuvable",
            "date_emprunt": emprunt["date_emprunt"],
            "date_retour": emprunt["date_retour"],
            "status": emprunt.get("status", "Status not available")
        })

    return render_template('emprunt_list.html', emprunts=emprunt_list)
@app.route('/emprunt/<emprunt_id>')
def get_emprunt(emprunt_id):
    try:
        # Fetch the emprunt by its ID
        emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(emprunt_id)})
        
        # Check if emprunt exists
        if emprunt:
            # Get the abonne and document details
            abonne_id = emprunt.get("abonne_id")
            document_id = emprunt.get("document_id")
            
            # Retrieve the associated abonne
            abonne = mongo.db.abonnes.find_one({"_id": ObjectId(abonne_id)}) if ObjectId.is_valid(abonne_id) else None
            
            # Retrieve the associated document
            document = mongo.db.documents.find_one({"_id": ObjectId(document_id)}) if ObjectId.is_valid(document_id) else None
            
            # Return the emprunt details along with the associated abonne and document information
            return jsonify({
                "abonne_nom": f"{abonne['nom']} {abonne['prenom']}" if abonne else "Abonné introuvable",
                "document_titre": document['titre'] if document else "Document introuvable",
                "date_emprunt": emprunt['date_emprunt'],
                "date_retour": emprunt['date_retour'],
                "status": emprunt['status'],  # Adding the 'status' field
                "abonne_id": abonne_id,
                "document_id": document_id
            })
        else:
            # If the emprunt is not found, return an error message
            return jsonify({"message": "Emprunt non trouvé"}), 404
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"Erreur: {str(e)}"}), 500

from flask import request, redirect, url_for, flash

@app.route('/update_emprunt/<emprunt_id>', methods=['PUT'])
def update_emprunt(emprunt_id):
    data = request.get_json()
    emprunt_data = data.get("emprunt")

    abonne_id = emprunt_data.get("abonne_id")
    document_id = emprunt_data.get("document_id")
    date_emprunt = emprunt_data.get("date_emprunt")
    date_retour = emprunt_data.get("date_retour")
    status = emprunt_data.get("status")  # Ajouter le champ status

    # Mise à jour de l'emprunt dans la base de données
    result = mongo.db.emprunts.update_one(
        {"_id": ObjectId(emprunt_id)},
        {"$set": {
            "abonne_id": abonne_id,
            "document_id": document_id,
            "date_emprunt": date_emprunt,
            "date_retour": date_retour,
            "status": status  # Mettre à jour le statut
        }}
    )
    
    if result.matched_count > 0:
        return jsonify({"message": "Emprunt mis à jour avec succès!"})
    else:
        return jsonify({"message": "Emprunt non trouvé"}), 404


# Route pour ajouter un emprunt
from bson import ObjectId
@app.route('/ajouter_emprunt', methods=['POST'])
def add_emprunt():
    data = request.json['emprunt']
    
    # Vérifier les IDs valides
    if not ObjectId.is_valid(data.get("abonne_id", "")) or not ObjectId.is_valid(data.get("document_id", "")):
        return jsonify({"error": "ID invalide pour l'abonné ou le document"}), 400

    # Ajouter le statut par défaut "emprunté"
    data["status"] = "emprunté"

    try:
        mongo.db.emprunts.insert_one(data)
        return jsonify({"message": "Emprunt ajouté avec succès!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erreur : {str(e)}"}), 500

# Route pour supprimer un emprunt
# @app.route('/delete_emprunt/<id>', methods=['POST'])
# def delete_emprunt(id):
#     # Delete the emprunt by its ID
#     mongo.db.emprunts.delete_one({"_id": ObjectId(id)})

#     flash("Emprunt deleted successfully", "success")
#     return redirect(url_for('get_emprunts'))  # Redirect to the list of emprunts

@app.route('/delete_emprunt/<id>', methods=['DELETE'])
def delete_emprunt(id):
    try:
        id = ObjectId(id)
        result = mongo.db.emprunts.delete_one({"_id": id})
        if result.deleted_count > 0:
            return jsonify({"message": "Emprunt deleted successfully"})
        else:
            return jsonify({"message": "No emprunt found to delete"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression de l'emprunt: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)