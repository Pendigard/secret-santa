// 1. La liste des joueurs (votre "base de données")
const listeJoueurs = [
    "Alice",
    "Alexia",
    "Bob",
    "Charlie",
    "David",
    "Éloïse",
    "Félix",
    "George",
    "Hélène",
    "Ingrid",
    "Jean-Luc"
    // Ajoutez tous les noms de votre Secret Santa ici
];

// 2. La fonction d'auto-suggestion
function suggererJoueurs() {
    // a. Récupérer les éléments HTML
    const input = document.getElementById('searchInput');
    const container = document.getElementById('suggestionsContainer');
    
    // b. Récupérer la valeur tapée par l'utilisateur, en minuscules pour la comparaison
    const valeurTapee = input.value.toLowerCase();
    
    // c. Vider le conteneur pour enlever les anciennes suggestions
    container.innerHTML = ''; 

    // Si le champ est vide, ne rien afficher
    if (valeurTapee.length === 0) {
        return;
    }

    // d. Filtrer la liste des joueurs
    const suggestionsFiltrees = listeJoueurs.filter(joueur => 
        // Vérifie si le nom du joueur (en minuscules) COMMENCE par ce qui est tapé
        joueur.toLowerCase().startsWith(valeurTapee)
    );

    // e. Afficher les suggestions filtrées
    suggestionsFiltrees.forEach(joueur => {
        // Créer un nouvel élément (un div, par exemple) pour chaque suggestion
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = joueur;
        
        // Ajouter un événement de clic pour remplir le champ de saisie si l'utilisateur clique dessus
        suggestionItem.onclick = function() {
            input.value = joueur;
            container.innerHTML = ''; // Cacher les suggestions après le clic
        };

        // Ajouter l'élément au conteneur de suggestions
        container.appendChild(suggestionItem);
    });
}