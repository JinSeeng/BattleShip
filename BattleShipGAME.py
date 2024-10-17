import random
import json
import os

# Statistiques des joueurs (victoires/défaites)
statistiques_joueurs = {}

# Initialisation de la grille pour les deux joueurs
def initialiser_grille():
    """Crée une grille de 10x10 vide pour le jeu"""
    return [[' ' for _ in range(10)] for _ in range(10)]

def afficher_grille(grille):
    """Affiche la grille de jeu avec les coordonnées"""
    print("   A B C D E F G H I J")
    print("  +" + "-+" * 10)
    for i, ligne in enumerate(grille):
        print(f"{i+1:2}|{'|'.join(ligne)}|")
        print("  +" + "-+" * 10)

def convertir_coordonnees(lettre, chiffre):
    """Convertit les coordonnées (lettre et chiffre) en indices pour la grille"""
    lettres_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
    return int(chiffre) - 1, lettres_to_index[lettre.upper()]

def demander_position_bateau(nom_bateau, taille_bateau):
    """Demande au joueur de placer un bateau sur la grille avec gestion des erreurs"""
    print(f"Où voulez-vous placer votre {nom_bateau} ({taille_bateau} cases) ?")
    orientation = input("Orientation (H pour horizontal, V pour vertical) : ").upper()
    while orientation not in ['H', 'V']:
        print("Orientation invalide. Entrez H pour horizontal ou V pour vertical.")
        orientation = input("Orientation (H pour horizontal, V pour vertical) : ").upper()

    colonne = input("Colonne (A-J) : ").upper()
    while colonne not in 'ABCDEFGHIJ':
        print("Colonne invalide. Entrez une lettre entre A et J.")
        colonne = input("Colonne (A-J) : ").upper()

    ligne = input("Ligne (1-10) : ")
    while not ligne.isdigit() or not 1 <= int(ligne) <= 10:
        print("Ligne invalide. Entrez un nombre entre 1 et 10.")
        ligne = input("Ligne (1-10) : ")

    return orientation, colonne, ligne

def verifier_position_valide(grille, orientation, ligne, colonne, taille_bateau):
    """Vérifie si le bateau peut être placé à la position donnée sans chevauchement ou dépassement"""
    ligne_index, colonne_index = convertir_coordonnees(colonne, ligne)

    # Vérification des limites de la grille
    if orientation == 'H':
        if colonne_index + taille_bateau > 10:
            return False
        for i in range(taille_bateau):
            if grille[ligne_index][colonne_index + i] != ' ':
                return False
    elif orientation == 'V':
        if ligne_index + taille_bateau > 10:
            return False
        for i in range(taille_bateau):
            if grille[ligne_index + i][colonne_index] != ' ':
                return False
    return True

def placer_bateau(grille, nom_bateau, taille_bateau):
    """Place un bateau sur la grille si la position est valide"""
    orientation, colonne, ligne = demander_position_bateau(nom_bateau, taille_bateau)
    while not verifier_position_valide(grille, orientation, ligne, colonne, taille_bateau):
        print("Position non valide. Réessayez.")
        orientation, colonne, ligne = demander_position_bateau(nom_bateau, taille_bateau)

    ligne_index, colonne_index = convertir_coordonnees(colonne, ligne)

    if orientation == 'H':
        for i in range(taille_bateau):
            grille[ligne_index][colonne_index + i] = 'X'
    else:  # Vertical
        for i in range(taille_bateau):
            grille[ligne_index + i][colonne_index] = 'X'

def placer_tous_les_bateaux(grille):
    """Place les cinq bateaux sur la grille"""
    bateaux = {
        'Porte-avions': 5,
        'Croiseur': 4,
        'Contre-torpilleur': 3,
        'Sous-marin': 3,
        'Torpilleur': 2
    }

    for nom_bateau, taille_bateau in bateaux.items():
        placer_bateau(grille, nom_bateau, taille_bateau)
        afficher_grille(grille)

def placement_automatique_ia(grille):
    """Place automatiquement les bateaux pour l'IA"""
    bateaux = {
        'Porte-avions': 5,
        'Croiseur': 4,
        'Contre-torpilleur': 3,
        'Sous-marin': 3,
        'Torpilleur': 2
    }
    for nom_bateau, taille_bateau in bateaux.items():
        orientation = random.choice(['H', 'V'])
        ligne = random.randint(1, 10)
        colonne = random.choice('ABCDEFGHIJ')
        while not verifier_position_valide(grille, orientation, ligne, colonne, taille_bateau):
            orientation = random.choice(['H', 'V'])
            ligne = random.randint(1, 10)
            colonne = random.choice('ABCDEFGHIJ')
        placer_bateau(grille, nom_bateau, taille_bateau)

def demander_tir():
    """Demande au joueur une case à attaquer avec gestion des erreurs"""
    colonne = input("Colonne à attaquer (A-J) : ").upper()
    while colonne not in 'ABCDEFGHIJ':
        print("Colonne invalide. Entrez une lettre entre A et J.")
        colonne = input("Colonne à attaquer (A-J) : ").upper()

    ligne = input("Ligne à attaquer (1-10) : ")
    while not ligne.isdigit() or not 1 <= int(ligne) <= 10:
        print("Ligne invalide. Entrez un nombre entre 1 et 10.")
        ligne = input("Ligne à attaquer (1-10) : ")

    return convertir_coordonnees(colonne, ligne)

def verifier_tir(grille_adversaire, grille_tirs, ligne_index, colonne_index):
    """Vérifie si le tir est un touché ou un coulé, et met à jour la grille de tirs"""
    if grille_tirs[ligne_index][colonne_index] in ['T', 'C']:
        print("Vous avez déjà tiré sur cette case.")
        return False

    if grille_adversaire[ligne_index][colonne_index] == 'X':
        print("Touché !")
        grille_adversaire[ligne_index][colonne_index] = 'T'
        grille_tirs[ligne_index][colonne_index] = 'T'
        return True
    else:
        print("Coulé.")
        grille_tirs[ligne_index][colonne_index] = 'C'
        return False

def jouer_tour(grille_adversaire, grille_tirs):
    """Permet à un joueur de jouer un tour et d'attaquer"""
    ligne_index, colonne_index = demander_tir()
    while grille_tirs[ligne_index][colonne_index] in ['T', 'M']:
        print("Vous avez déjà tiré sur cette case.")
        ligne_index, colonne_index = demander_tir()

    return verifier_tir(grille_adversaire, grille_tirs, ligne_index, colonne_index)

# Fonction pour IA intelligente (niveau difficile)
def ia_intelligente(grille_adversaire, grille_tirs):
    """IA attaquant intelligemment selon les tirs précédents."""
    for i in range(10):
        for j in range(10):
            if grille_tirs[i][j] == 'T':
                if i > 0 and grille_tirs[i-1][j] == ' ':  # Case au-dessus
                    return i-1, j
                if i < 9 and grille_tirs[i+1][j] == ' ':  # Case en dessous
                    return i+1, j
                if j > 0 and grille_tirs[i][j-1] == ' ':  # Case à gauche
                    return i, j-1
                if j < 9 and grille_tirs[i][j+1] == ' ':  # Case à droite
                    return i, j+1
    return ia_facile(grille_adversaire, grille_tirs)

# Fonction pour IA facile (niveau facile)
def ia_facile(grille_adversaire, grille_tirs):
    """IA attaquant aléatoirement"""
    ligne, colonne = random.randint(0, 9), random.randint(0, 9)
    while grille_tirs[ligne][colonne] in ['T', 'C']:
        ligne, colonne = random.randint(0, 9), random.randint(0, 9)
    return ligne, colonne

def sauvegarder_partie(grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2, fichier_sauvegarde='sauvegarde.json'):
    """Sauvegarde l'état actuel de la partie dans un fichier JSON"""
    etat_partie = {
        'grille_joueur1': grille_joueur1,
        'grille_joueur2': grille_joueur2,
        'grille_tirs_joueur1': grille_tirs_joueur1,
        'grille_tirs_joueur2': grille_tirs_joueur2
    }
    with open(fichier_sauvegarde, 'w') as f:
        json.dump(etat_partie, f)
    print("Partie sauvegardée.")

def charger_partie(fichier_sauvegarde='sauvegarde.json'):
    """Charge une partie sauvegardée à partir d'un fichier JSON"""
    if not os.path.exists(fichier_sauvegarde):
        print("Aucune partie sauvegardée n'a été trouvée.")
        return None, None, None, None

    with open(fichier_sauvegarde, 'r') as f:
        etat_partie = json.load(f)

    return (etat_partie['grille_joueur1'],
            etat_partie['grille_joueur2'],
            etat_partie['grille_tirs_joueur1'],
            etat_partie['grille_tirs_joueur2'])

def mise_a_jour_statistiques(nom_gagnant, nom_perdant):
    """Mise à jour des statistiques de victoires et défaites pour chaque joueur"""
    if nom_gagnant not in statistiques_joueurs:
        statistiques_joueurs[nom_gagnant] = {'victoires': 0, 'defaites': 0}
    if nom_perdant not in statistiques_joueurs:
        statistiques_joueurs[nom_perdant] = {'victoires': 0, 'defaites': 0}

    statistiques_joueurs[nom_gagnant]['victoires'] += 1
    statistiques_joueurs[nom_perdant]['defaites'] += 1

    # Sauvegarder les statistiques dans un fichier JSON
    with open('statistiques_joueurs.json', 'w') as f:
        json.dump(statistiques_joueurs, f)

def afficher_statistiques():
    """Affiche le classement des joueurs en fonction des victoires/défaites"""
    print("Classement des joueurs :")
    classement = sorted(statistiques_joueurs.items(), key=lambda x: x[1]['victoires'], reverse=True)
    for joueur, stats in classement:
        print(f"{joueur} - {stats['victoires']} victoire(s), {stats['defaites']} défaite(s)")

def jeu_bataille_navale():
    """Lance une partie de bataille navale"""
    global statistiques_joueurs

    # Charger les statistiques des joueurs à partir du fichier JSON
    if os.path.exists('statistiques_joueurs.json'):
        with open('statistiques_joueurs.json', 'r') as f:
            statistiques_joueurs = json.load(f)

    print("Bienvenue dans la Bataille Navale !")
    nom_joueur1 = input("Nom du joueur 1 : ")
    choix_mode = input("Voulez-vous jouer contre un autre joueur (1) ou contre l'IA (2) ? ")
    if choix_mode == '1':
        nom_joueur2 = input("Nom du joueur 2 : ")
        mode_ia = False
    else:
        nom_joueur2 = "IA"
        difficulte_ia = input("Choisissez le niveau de difficulté de l'IA (facile/difficile) : ")
        mode_ia = True

    # Chargement ou nouvelle partie
    if input("Voulez-vous charger une partie sauvegardée ? (oui/non) ").lower() == 'oui':
        grilles = charger_partie()
        if grilles[0] is None:
            return
        grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2 = grilles
    else:
        # Initialiser les grilles
        grille_joueur1 = initialiser_grille()
        grille_joueur2 = initialiser_grille()
        grille_tirs_joueur1 = initialiser_grille()
        grille_tirs_joueur2 = initialiser_grille()

        # Placer les bateaux
        print(f"{nom_joueur1}, placez vos bateaux.")
        placer_tous_les_bateaux(grille_joueur1)
        print(f"{nom_joueur2}, placez vos bateaux.")
        if mode_ia:
            # Placement automatique des bateaux pour l'IA
            for nom_bateau, taille_bateau in {'Porte-avions': 5, 'Croiseur': 4, 'Contre-torpilleur': 3, 'Sous-marin': 3, 'Torpilleur': 2}.items():
                orientation = random.choice(['H', 'V'])
                ligne = random.randint(1, 10)
                colonne = random.choice('ABCDEFGHIJ')
                while not verifier_position_valide(grille_joueur2, orientation, ligne, colonne, taille_bateau):
                    orientation = random.choice(['H', 'V'])
                    ligne = random.randint(1, 10)
                    colonne = random.choice('ABCDEFGHIJ')
                placer_bateau(grille_joueur2, nom_bateau, taille_bateau)
        else:
            placer_tous_les_bateaux(grille_joueur2)

    # Boucle de jeu
    partie_terminee = False
    tour_joueur1 = True

    while not partie_terminee:
        if tour_joueur1:
            print(f"{nom_joueur1}, c'est votre tour.")
            afficher_grille(grille_tirs_joueur1)
            partie_terminee = jouer_tour(grille_joueur2, grille_tirs_joueur1)
        else:
            print(f"{nom_joueur2}, c'est votre tour.")
            if mode_ia:
                if difficulte_ia == 'facile':
                    ligne, colonne = ia_facile(grille_joueur1, grille_tirs_joueur2)
                else:
                    ligne, colonne = ia_intelligente(grille_joueur1, grille_tirs_joueur2)
                verifier_tir(grille_joueur1, grille_tirs_joueur2, ligne, colonne)
            else:
                afficher_grille(grille_tirs_joueur2)
                partie_terminee = jouer_tour(grille_joueur1, grille_tirs_joueur2)

        tour_joueur1 = not tour_joueur1

        # Vérification de la victoire
        if all(cell != 'X' for row in grille_joueur1 for cell in row):
            print(f"{nom_joueur2} a gagné !")
            mise_a_jour_statistiques(nom_joueur2, nom_joueur1)
            partie_terminee = True
        elif all(cell != 'X' for row in grille_joueur2 for cell in row):
            print(f"{nom_joueur1} a gagné !")
            mise_a_jour_statistiques(nom_joueur1, nom_joueur2)
            partie_terminee = True

    # Sauvegarde de la partie
    if input("Voulez-vous sauvegarder la partie avant de quitter ? (oui/non) ").lower() == 'oui':
        sauvegarder_partie(grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2)

    # Afficher les statistiques
    afficher_statistiques()

# Lancer le jeu
jeu_bataille_navale()