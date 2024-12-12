$(document).ready(function() {
    // Open "Add Abonné" modal
    $('#addAbonneModal').on('show.bs.modal', function() {
        $('#abonneForm')[0].reset();
        $('#abonneForm').off('submit').on('submit', function(e) {
            e.preventDefault();
            addAbonne();
        });
    });

    // Add an Abonné
    function addAbonne() {
        const data = {
            nom: $('#nom').val(),
            prenom: $('#prenom').val(),
            adresse: $('#adresse').val(),
            date_inscription: $('#date_inscription').val()
        };

        $.ajax({
            url: '/add_abonne',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                alert(response.message);
                location.reload(); // Reload the page to reflect changes
                $('#addAbonneModal').modal('hide');
            },
            error: function(xhr, status, error) {
                alert('Erreur lors de l\'ajout de l\'abonné');
            }
        });
    }

    // View an Abonné
    window.viewAbonne = function(id) {
        $.get(`/get_abonne/${id}`, function(response) {
            if (response.error) {
                alert(response.error);
            } else {
                alert(`Nom: ${response.nom}, Prénom: ${response.prenom}, Adresse: ${response.adresse}`);
            }
        });
    };



  // Edit an Abonné
  window.editAbonne = function (id) {
    console.log("Chargement des données pour l'abonné ID:", id);

    $.get(`/get_abonne/${id}`, function (response) {
        console.log("Réponse du serveur :", response);

        if (response.error) {
            alert(response.error);
        } else {
            // Remplir les champs du formulaire avec les données reçues
            $('#abonneId').val(response.id); // Stocker l'ID dans un champ caché
            $('#nom').val(response.nom);
            $('#prenom').val(response.prenom);
            $('#adresse').val(response.adresse);
            $('#date_inscription').val(response.date_inscription);

            // Afficher la modale
            $('#ModifierAbonneModal').modal('show');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Erreur AJAX :", textStatus, errorThrown);
        alert("Erreur lors de la récupération des données.");
    });
};




    // Update an Abonné
    function updateAbonne(id) {
        const data = {
            nom: $('#nom').val(),
            prenom: $('#prenom').val(),
            adresse: $('#adresse').val(),
            date_inscription: $('#date_inscription').val()
        };

        $.ajax({
            url: `/update_abonne/${id}`,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                alert(response.message);
                location.reload(); // Reload the page to reflect changes
                $('#addAbonneModal').modal('hide');
            },
            error: function(xhr, status, error) {
                alert('Erreur lors de la mise à jour de l\'abonné');
            }
        });
    }

    // Delete an Abonné
    window.deleteAbonne = function(id) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cet abonné?')) {
            $.ajax({
                url: `/delete_abonne/${id}`,
                type: 'DELETE',
                success: function(response) {
                    alert(response.message);
                    location.reload(); // Reload the page to reflect changes
                },
                error: function(xhr, status, error) {
                    alert('Erreur lors de la suppression de l\'abonné');
                }
            });
        }
    };

  
    window.editAbonne = function(id) {
        $.get(`/get_abonne/${id}`, function(response) {
            if (response.error) {
                alert(response.error);
            } else {
                $('#abonneId').val(id); // Stocker l'ID dans un champ caché
                $('#nom').val(response.nom);
                $('#prenom').val(response.prenom);
                $('#adresse').val(response.adresse);
                $('#date_inscription').val(response.date_inscription);
    
                $('#ModifierAbonneModal').modal('show'); // Afficher la modale
            }
        });
    };
 // Ajouter cette ligne pour rendre la fonction globale
window.showHistorique = function(abonneId) {
    // Effectuer une requête AJAX pour récupérer l'historique des emprunts
    $.get(`/historique_emprunts/${abonneId}`, function(data) {
        if (data.historique_emprunts && data.historique_emprunts.length > 0) {
            // Vider la liste avant d'ajouter les nouveaux éléments
            $('#historiqueList').empty();
            alert("Historique de l'abonné avec ID: " + abonneId);

            // Parcourir les emprunts et les ajouter à la liste
            data.historique_emprunts.forEach(function(emprunt) {
                const empruntItem = `
                    <li>
                        <strong>Titre :</strong> ${emprunt.titre_document} <br>
                        <strong>Date d'emprunt :</strong> ${emprunt.date_emprunt} <br>
                        <strong>Date de retour :</strong> ${emprunt.date_retour} <br>
                        <strong>Status :</strong> ${emprunt.status} <br>
                    </li>
                `;
                $('#historiqueList').append(empruntItem);
            });

            // Afficher la modale avec l'historique
            $('#historiqueModal').modal('show');
        } else {
            alert("Aucun emprunt trouvé pour cet abonné.");
        }
    }).fail(function(xhr, status, error) {
        console.error("Erreur AJAX :", status, error);
        alert("Erreur lors de la récupération de l'historique. Veuillez réessayer plus tard.");
    });
};


});
