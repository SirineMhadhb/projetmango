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
    window.editAbonne = function(id) {
        $.get(`/get_abonne/${id}`, function(response) {
            if (response.error) {
                alert(response.error);
            } else {
                $('#nom').val(response.nom);
                $('#prenom').val(response.prenom);
                $('#adresse').val(response.adresse);
                $('#date_inscription').val(response.date_inscription);
                
                // Update the form action to edit
                $('#abonneForm').off('submit').on('submit', function(e) {
                    e.preventDefault();
                    updateAbonne(id);
                });

                $('#addAbonneModal').modal('show');
            }
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
});
