// Fonction pour afficher la popup pour ajouter ou modifier un abonné
function showPopup(action, abonneId = null) {
    const popup = document.getElementById('popup-modal');
    const title = document.getElementById('popup-title');
    const form = document.getElementById('abonne-form');

    if (action === 'edit' || action === 'view' || action === 'add') {
        if (action === 'add') {
            title.textContent = 'Ajouter un Abonné';
            form.reset();
        } else if (action === 'edit') {
            title.textContent = 'Modifier un Abonné';
            // Récupérer les données de l'abonné
            fetch(`/get_abonne/${abonneId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('nom').value = data.nom;
                    document.getElementById('prenom').value = data.prenom;
                    document.getElementById('adresse').value = data.adresse;
                    document.getElementById('date_inscription').value = data.date_inscription;
                });
        } else if (action === 'view') {
            title.textContent = 'Consulter un Abonné';
            // Récupérer les données de l'abonné
            fetch(`/get_abonne/${abonneId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('nom').value = data.nom;
                    document.getElementById('prenom').value = data.prenom;
                    document.getElementById('adresse').value = data.adresse;
                    document.getElementById('date_inscription').value = data.date_inscription;
                    document.querySelector('button[type="submit"]').style.display = 'none'; // Cacher le bouton 'Enregistrer'
                });
        }

        popup.style.display = 'block';
    }
}

// Fonction pour fermer la popup
function closePopup() {
    document.getElementById('popup-modal').style.display = 'none';
}

// Fonction pour supprimer un abonné
function deleteAbonne(abonneId) {
    fetch(`/delete_abonne/${abonneId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            loadAbonnes(); // Rafraîchir la liste après suppression
        } else {
            alert('Erreur lors de la suppression');
        }
    });
}

// Fonction pour charger la liste des abonnés
function loadAbonnes() {
    fetch('/abonne')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#abonne-list tbody');
            tbody.innerHTML = '';
            data.forEach(abonne => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${abonne.nom}</td>
                    <td>${abonne.prenom}</td>
                    <td>${abonne.adresse}</td>
                    <td>${abonne.date_inscription}</td>
                    <td>
                        <button onclick="showPopup('view', ${abonne.id})">Voir</button>
                        <button onclick="showPopup('edit', ${abonne.id})">Modifier</button>
                        <button onclick="deleteAbonne(${abonne.id})">Supprimer</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        });
}

// Enregistrer ou mettre à jour un abonné
document.getElementById('abonne-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const nom = document.getElementById('nom').value;
    const prenom = document.getElementById('prenom').value;
    const adresse = document.getElementById('adresse').value;
    const date_inscription = document.getElementById('date_inscription').value;

    const data = {
        nom: nom,
        prenom: prenom,
        adresse: adresse,
        date_inscription: date_inscription
    };

    const method = document.getElementById('popup-title').textContent === 'Ajouter un Abonné' ? 'POST' : 'PUT';
    const url = method === 'POST' ? '/add_abonne' : `/update_abonne/${abonneId}`;

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closePopup();
        loadAbonnes(); // Rafraîchir la liste après l'ajout ou la modification
    });
});

// Charger les abonnés au démarrage
loadAbonnes();
