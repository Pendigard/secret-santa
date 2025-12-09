

function suggererJoueurs() {
    const input = document.getElementById('searchInput');
    const container = document.getElementById('suggestionsContainer');
    
    const valeurTapee = input.value.toLowerCase();
    
    container.innerHTML = ''; 

    if (valeurTapee.length === 0) {
        return;
    }

    // listeJoueurs vient désormais de players.map(p => p.username)
    const suggestionsFiltrees = listeJoueurs.filter(joueur =>
        joueur.toLowerCase().startsWith(valeurTapee)
    );

    suggestionsFiltrees.forEach(joueur => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = joueur;

        suggestionItem.onclick = function() {
            input.value = joueur;
            container.innerHTML = '';
        };

        container.appendChild(suggestionItem);
    });
}

document.getElementById("secretSantaForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("searchInput").value.trim();
    const errorMessage = document.getElementById("errorMessage");

    errorMessage.style.display = "none";
    errorMessage.textContent = "";

    if (!username) {
        errorMessage.textContent = "Veuillez entrer un prénom.";
        errorMessage.style.display = "block";
        return;
    }

    // Chercher le joueur dans la liste
    const player = players.find(
        p => p[0].toLowerCase() === username.toLowerCase()
    );

    if (player) {
        // Redirection directe : plus besoin d'appeler le serveur
        window.location.href = `/player/${player[1]}`;
    } else {
        errorMessage.textContent = "Ce nom n'existe pas dans la liste des participants.";
        errorMessage.style.display = "block";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const el = document.getElementById('texte-arcenciel');
    if (!el) return;

    const text = el.textContent;
    el.textContent = ''; // On vide

    [...text].forEach((char, index) => {
        const span = document.createElement('span');

        if (char === " ") {
            // Préserver les espaces
            span.innerHTML = "&nbsp;";
        } else {
            span.textContent = char;
        }

        span.style.animationDelay = `${index * 0.1}s`;
        el.appendChild(span);
    });
});