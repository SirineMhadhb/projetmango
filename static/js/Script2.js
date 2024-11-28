// Fonction pour afficher une modal spécifique
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

// Fonction pour fermer une modal spécifique
function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Charger les emprunts
function loadEmprunts() {
    $.get("/get_emprunts", function(data) {
        let empruntsTable = $("#emprunts-table tbody");
        empruntsTable.empty();
        data.forEach(function(emprunt) {
            let row = `<tr>
                <td>${emprunt._id}</td>
                <td>${emprunt.abonne_id}</td>
                <td>${emprunt.document_id}</td>
                <td>${emprunt.date_emprunt}</td>
                <td>${emprunt.date_retour}</td>
                <td>
                    <button class="edit-button" onclick="editEmprunt('${emprunt._id}')">Modifier</button>
                    <button class="delete-button" onclick="deleteEmprunt('${emprunt._id}')">Supprimer</button>
                </td>
            </tr>`;
            empruntsTable.append(row);
        });
    });
}

// Ajouter un emprunt
$("#add-emprunt-form").submit(function(event) {
    event.preventDefault();

    let empruntData = {
        abonne_id: $("#abonne_id").val(),
        document_id: $("#document_id").val(),
        date_emprunt: $("#date_emprunt").val(),
        date_retour: $("#date_retour").val()
    };

    $.ajax({
        url: "/add_emprunt",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(empruntData),
        success: function(response) {
            alert(response.message);
            loadEmprunts(); // Recharge les emprunts après ajout
            closeModal('addEmpruntModal'); // Ferme la popup
            $("#add-emprunt-form")[0].reset(); // Réinitialiser le formulaire
        },
        error: function(error) {
            alert("Erreur lors de l'ajout de l'emprunt!");
        }
    });
});

// Modifier un emprunt
function editEmprunt(empruntId) {
    $.get(`/get_emprunt_by_id/${empruntId}`, function(data) {
        // Remplir le formulaire avec les données existantes
        $("#edit-emprunt-id").val(data._id);
        $("#edit-abonne_id").val(data.abonne_id);
        $("#edit-document_id").val(data.document_id);
        $("#edit-date_emprunt").val(data.date_emprunt);
        $("#edit-date_retour").val(data.date_retour);

        // Afficher la modal de modification
        openModal('editEmpruntModal');
    });
}

$("#edit-emprunt-form").submit(function(event) {
    event.preventDefault();

    let empruntData = {
        _id: $("#edit-emprunt-id").val(),
        abonne_id: $("#edit-abonne_id").val(),
        document_id: $("#edit-document_id").val(),
        date_emprunt: $("#edit-date_emprunt").val(),
        date_retour: $("#edit-date_retour").val()
    };

    $.ajax({
        url: "/update_emprunt",
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify(empruntData),
        success: function(response) {
            alert(response.message);
            loadEmprunts(); // Recharge les emprunts après modification
            closeModal('editEmpruntModal'); // Ferme la popup
        },
        error: function(error) {
            alert("Erreur lors de la modification de l'emprunt!");
        }
    });
});

// Supprimer un emprunt
function deleteEmprunt(empruntId) {
    if (confirm("Êtes-vous sûr de vouloir supprimer cet emprunt ?")) {
        $.ajax({
            url: `/delete_emprunt/${empruntId}`,
            method: "DELETE",
            success: function(response) {
                alert(response.message);
                loadEmprunts(); // Recharge les emprunts après suppression
            },
            error: function(error) {
                alert("Erreur lors de la suppression de l'emprunt!");
            }
        });
    }
}

// Initialiser les emprunts au chargement de la page
$(document).ready(function() {
    loadEmprunts();
});
