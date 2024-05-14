
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width , initial-scale=1.0">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="../styles/BARS.css">
    <link rel="stylesheet" href="../styles/ajout.css">
    <script src="../javascript/BARS.js"></script>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
        integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap">
    <title>Voir Encadrement</title>
</head>

<body>
    <nav>
        <div class="sidebar">
            <div class="logo-container">

                <span>
                    <img src="../images/FINALWHITE.png" alt="logo" class="logo-image">
                </span>
                <span class="bars-icon">
                    <img src="../images/Company PProfile.png" class='logo-icon'>
                </span>
            </div>

            <ul class="nav-links">
                <button class="button-links" id="button-link">
                    <li class="links">
                        <a class="link_other" href="../html/accueil.html">
                            <img src="../images/Vector.png" class='icon'>
                            <span class="link_name">Acceuil</span>
                        </a>
                    </li>
                </button>
                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="#">
                            <img src="../images/Search.png" class='icon'>
                            <span class="link_name"> Recherche</span>
                            <i class="fa-solid fa-angle-down" id="toggleSubMenu"></i>
                        </a>
                        <div class="sub_sub_menu">

                            <ul class="sub_menu">
                                <li class="sous-choice"> <i class="fa-solid fa-caret-right"></i><a class="liste_am"
                                        href="../html/chercheurs.html"> Chercheurs</a></li>
                                <li class="sous-choice"><i class="fa-solid fa-caret-right"></i><a class="liste_am"
                                        href="../html/publication.html">Publications</a></li>
                                <li class="sous-choice"><i class="fa-solid fa-caret-right"></i><a class="liste_am"
                                        href="../html/chercheurs.html">Encadrements </a></li>
                                <li class="sous-choice"><i class="fa-solid fa-caret-right"></i><a class="liste_am"
                                        href="../html/chercheurs.html">Projets</a></li>
                            </ul>
                        </div>
                    </li>
                </button>

                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="#">
                            <img src="../images/news.png" class='icon'>
                            <span class="link_name"> Publications </span>
                            <i class="fa-solid fa-angle-down" id="toggleSubMenuu"></i>
                        </a>
                        <div class="sub_sub_menu">
                            <ul class="sub_menu">
                                <li class="sous-choice2"> <i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/Ajtpubcher.html">Ajouter une
                                        publication</a>
                                </li>
                                <li class="sous-choice2"> <i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/Ajtconf-revue.html">Ajouter une
                                        conf-journal</a>
                                </li>
                                <li class="sous-choice2"><i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/listedepublication.html">Liste des publications</a>
                                </li>
                            </ul>
                        </div>
                    </li>
                </button>
                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="#">

                            <img src="../images/encadrement.png" class='icon'>
                            <span class="link_name"> Encadrements</span>
                            <i class="fa-solid fa-angle-down" id="toggleSubMenuuu"></i>
                        </a>
                        <div class="sub_sub_menu">
                            <ul class="sub_menu">
                                <li class="sous-choice2"> <i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/Ajtencadrementcher.html">Ajouter un Encadrement</a>
                                </li>
                                <li class="sous-choice2"><i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/listedeencadrement.html">Liste des Encadrements</a>
                                </li>
                            </ul>
                        </div>
                    </li>
                </button>
                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="#">
                            <img src="../images/list.png" class='icon'>
                            <span class="link_name"> Projets </span>
                            <i class="fa-solid fa-angle-down" id="toggleSubMenuuuu"></i>
                        </a>
                        <div class="sub_sub_menu">
                            <ul class="sub_menu">
                                <li class="sous-choice"><i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/Ajtprojetcher.html"> Ajouter un
                                        Projet </a></li>
                                <li class="sous-choice"><i class="fa-solid fa-caret-right"></i><a class="liste2"
                                        href="../html/listedeprojet.html">Liste des Projets</a></li>
                            </ul>
                        </div>
                    </li>
                </button>
                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="../html/statistiques.html">
                            <img src="../images/Icons.png" class='icon'>
                            <span class="link_name"> statistique </span>
                        </a>
                    </li>
                </button>

                <button class="button-links">
                    <li class="links">
                        <a class="link_other" href="#">
                            <img src="../images/Historique.png" class='icon'>
                            <span class="link_name"> Historique </span>
                        </a>
                    </li>
                </button>
                <button class="button-links">

                    <li class="links">
                        <a class="link_other" href="#">
                            <img src="../images/Logout.png" class='icon'>
                            <span class="link_name "> Déconnecter </span>
                        </a>
                    </li>
            </ul>
            </button>
        </div>
    </nav>
    <div class="top-bar-right">
        <div class="aide">
            <button><img src="../images/help.png" alt="aide"></button>
        </div>
        <div class="settings">
            <button><img src="../images/paramerte.png" alt="Paramètres"></button>
        </div>
        <div class="notification">
            <button>
                <img src="../images/notification.png" alt="Notifications">
            </button>
        </div>
        <div class="profile">
            <img src="../images/Profile.png" alt="Profil">
        </div>
    </div>

    <button class="left-button" onclick="goBack()"><img src="../images/Left1.png"></button>

    <div class="pub">
        <div class="pub-title">
            <p>Encadrement</p>
        </div>
        <div class="pub-content">
            <div class="pub-container" id="originalInfo">
                <div class="left-pub-info">
                    <p>Titre :</p>
                    <p>Type :</p>
                    <p>Date de debut d’encadrement :</p>
                    <p>Date de fin d’encadrement :</p>
                    <p>Etudiant1:</p>
                    <p>Etudiant2:</p>
                    <p>chercheur 1:</p>
                    <p>Role chercheur 1 :</p>
                    <p>chercheur 2:</p>
                    <p>Role chercheur 2 :</p>
                </div>
                <div class="right-pub-info">
                    <p id="intitule">l’intellegence artificielle</p>
<p id="type">PFE</p>
<p id="annee_debut">2019</p>
<p id="annee_fin">2021</p>
<p id="nom_etudiant1">Medabis</p>
<p id="nom_etudiant2">Amina</p>
<p id="chercheur1">Medabis Amina</p>
<p id="role_chercheur1">encadreur</p>
<p id="chercheur2">---</p>
<p id="role_chercheur2">---</p>
                </div>
            </div>
        </div>

    </div>
    <script src=" https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="../javascript/ajout.js"></script>
    <script>
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer l'ID de l'encadrement de la session
    const encadrementId = sessionStorage.getItem('id_encadrement');

    // Faire une requête AJAX pour récupérer les détails de l'encadrement
    fetch(`http://127.0.0.1:8000/api/encadrements/${encadrementId}/`)
        .then(response => response.json())
        .then(data => {
            // Mettre à jour les éléments HTML avec les données récupérées
            document.getElementById('intitule').textContent = data.intitule;
            document.getElementById('type').textContent = data.type_encadrement;
            document.getElementById('annee_debut').textContent = data.annee_debut;
            document.getElementById('annee_fin').textContent = data.annee_fin;
            document.getElementById('nom_etudiant1').textContent = data.nom_prenom_etd1;
            document.getElementById('nom_etudiant2').textContent = data.nom_prenom_etd2;

            // Vérifier si des chercheurs sont disponibles
            if (data.chercheurs.length > 0) {
                // Mettre à jour les données pour le premier chercheur
                document.getElementById('chercheur1').textContent = `${data.chercheurs[0].nom_chercheur} ${data.chercheurs[0].prenom_chercheur}`;
                document.getElementById('role_chercheur1').textContent = data.role_chercheur;

                // Vérifier s'il y a un deuxième chercheur
                if (data.chercheurs.length > 1) {
                    // Mettre à jour les données pour le deuxième chercheur
                    document.getElementById('chercheur2').textContent = `${data.chercheurs[1].nom_chercheur} ${data.chercheurs[1].prenom_chercheur}`;
                    document.getElementById('role_chercheur2').textContent = data.role_chercheur2;
                } else {
                    // Aucun deuxième chercheur trouvé, afficher un message par défaut
                    document.getElementById('chercheur2').textContent = '---';
                    document.getElementById('role_chercheur2').textContent = '---';
                }
            } else {
                // Aucun chercheur trouvé, afficher un message par défaut
                document.getElementById('chercheur1').textContent = '---';
                document.getElementById('role_chercheur1').textContent = '---';
                document.getElementById('chercheur2').textContent = '---';
                document.getElementById('role_chercheur2').textContent = '---';
            }
        })
        .catch(error => console.error('Une erreur s\'est produite : ', error));
});
</script>

</body>

</html>
