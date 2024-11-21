$(document).ready(function() {
    // Charger la liste des documents
    function loadDocuments() {
        $.get('/documents', function(response) {
            const documents = response.documents;
            const documentRows = documents.map(doc => `
                <tr>
                    <td>${doc.titre}</td>
                    <td>${doc.auteur}</td>
                    <td>${doc.genre}</td>
                    <td>${doc.date_publication}</td>
                    <td>${doc.disponibilite}</td>
                    <td>
                        <button class="btn btn-info" onclick="viewDocument('${doc.id}')">Voir</button>
                        <button class="btn btn-warning" onclick="editDocument('${doc.id}')">Modifier</button>
                        <button class="btn btn-danger" onclick="deleteDocument('${doc.id}')">Supprimer</button>
                    </td>
                </tr>
            `);
            $('#documentsList').html(documentRows.join(''));
        });
    }

    // Ajouter un Document
    function addDocument() {
        const data = {
            titre: $('#titre').val(),
            auteur: $('#auteur').val(),
            genre: $('#genre').val(),
            date_publication: $('#date_publication').val(),
            disponibilite: $('#disponibilite').val()
        };

        $.ajax({
            url: '/add_document',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                alert(response.message);
                loadDocuments(); // Recharger la liste des documents
                $('#addDocumentModal').modal('hide');
            },
            error: function(xhr, status, error) {
                alert('Erreur lors de l\'ajout du document');
            }
        });
    }

    // Voir un Document
    window.viewDocument = function(id) {
        $.get(`/get_document/${id}`, function(response) {
            alert(`Titre: ${response.titre}, Auteur: ${response.auteur}, Genre: ${response.genre}`);
        });
    };

    // Modifier un Document
    window.editDocument = function(id) {
        $.get(`/get_document/${id}`, function(response) {
            $('#titre').val(response.titre);
            $('#auteur').val(response.auteur);
            $('#genre').val(response.genre);
            $('#date_publication').val(response.date_publication);
            $('#disponibilite').val(response.disponibilite);
            $('#documentForm').off('submit').on('submit', function(e) {
                e.preventDefault();
                updateDocument(id);
            });
            $('#addDocumentModal').modal('show');
        });
    };

    // Mettre à jour un Document
    function updateDocument(id) {
        const data = {
            titre: $('#titre').val(),
            auteur: $('#auteur').val(),
            genre: $('#genre').val(),
            date_publication: $('#date_publication').val(),
            disponibilite: $('#disponibilite').val()
        };

        $.ajax({
            url: `/update_document/${id}`,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                alert(response.message);
                loadDocuments();
                $('#addDocumentModal').modal('hide');
            },
            error: function(xhr, status, error) {
                alert('Erreur lors de la mise à jour du document');
            }
        });
    }

    // Supprimer un Document
    window.deleteDocument = function(id) {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce document?')) {
            $.ajax({
                url: `/delete_document/${id}`,
                type: 'DELETE',
                success: function(response) {
                    alert(response.message);
                    loadDocuments();
                },
                error: function(xhr, status, error) {
                    alert('Erreur lors de la suppression du document');
                }
            });
        }
    };

    // Charger les documents au démarrage
    loadDocuments();
});
