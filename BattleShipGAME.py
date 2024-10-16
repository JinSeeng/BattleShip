import random
import json
import os

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
    """Demande au joueur de placer un bateau sur la grille"""
    while True:
        orientation = input("Orientation (H pour horizontal, V pour vertical) : ").upper()
        if orientation in ['H', 'V']:
            break
        print("Votre choix est invalide. Réessayez.")

    while True:
        colonne = input("Colonne (A-J) : ").upper()
        if colonne in 'ABCDEFGHIJ':
            break
        print("Votre choix est invalide. Réessayez.")

    while True:
        ligne = input("Ligne (1-10) : ")
        if ligne.isdigit() and 1 <= int(ligne) <= 10:
            break
        print("Votre choix est invalide. Réessayez.")

    return orientation, colonne, ligne

def verifier_position_valide(grille, orientation, ligne, colonne, taille_bateau):
    """Vérifie si le bateau peut être placé à la position donnée sans chevauchement ou dépassement"""
    ligne_index, colonne_index = convertir_coordonnees(colonne, ligne)

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

def demander_tir():
    """Demande au joueur une case à attaquer"""
    while True:
        colonne = input("Colonne à attaquer (A-J) : ").upper()
        if colonne in 'ABCDEFGHIJ':
            break
        print("Votre choix est invalide. Réessayez.")

    while True:
        ligne = input("Ligne à attaquer (1-10) : ")
        if ligne.isdigit() and 1 <= int(ligne) <= 10:
            break
        print("Votre choix est invalide. Réessayez.")

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
    while grille_tirs[ligne_index][colonne_index] in ['T', 'C']:
        print("Vous avez déjà tiré sur cette case.")
        ligne_index, colonne_index = demander_tir()

    return verifier_tir(grille_adversaire, grille_tirs, ligne_index, colonne_index)

def placer_bateau_aleatoire(grille, taille):
    """Place un bateau de taille donnée aléatoirement sur la grille."""
    orientation = random.choice(["H", "V"])  # H = horizontal, V = vertical
    if orientation == "H":
        ligne = random.randint(0, 9)
        col_debut = random.randint(0, 10 - taille)
        for i in range(taille):
            if grille[ligne][col_debut + i] != ' ':
                return placer_bateau_aleatoire(grille, taille)
        for i in range(taille):
            grille[ligne][col_debut + i] = 'X'
    else:
        col = random.randint(0, 9)
        ligne_debut = random.randint(0, 10 - taille)
        for i in range(taille):
            if grille[ligne_debut + i][col] != ' ':
                return placer_bateau_aleatoire(grille, taille)
        for i in range(taille):
            grille[ligne_debut + i][col] = 'X'

def placer_bateaux_automatique(grille):
    """Place tous les bateaux de l'IA automatiquement sur la grille."""
    tailles_bateaux = [5, 4, 3, 3, 2]  # Les tailles des bateaux à placer
    for taille in tailles_bateaux:
        placer_bateau_aleatoire(grille, taille)

def sauvegarder_partie(grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2):
    """Sauvegarde l'état actuel du jeu dans un fichier JSON"""
    etat_partie = {
        "grille_joueur1": grille_joueur1,
        "grille_joueur2": grille_joueur2,
        "grille_tirs_joueur1": grille_tirs_joueur1,
        "grille_tirs_joueur2": grille_tirs_joueur2
    }
    with open("sauvegarde.json", "w") as fichier:
        json.dump(etat_partie, fichier)

def charger_partie():
    """Charge l'état du jeu depuis un fichier JSON"""
    if os.path.exists("sauvegarde.json"):
        with open("sauvegarde.json", "r") as fichier:
            return json.load(fichier)
    else:
        print("Aucune sauvegarde trouvée.")
        return None

def jeu_bataille_navale(mode_ia=None):
    """Jeu principal de bataille navale avec deux joueurs ou contre IA"""
    grille_joueur1 = initialiser_grille()
    grille_joueur2 = initialiser_grille()
    grille_tirs_joueur1 = initialiser_grille()
    grille_tirs_joueur2 = initialiser_grille()

    # Essayer de charger une partie sauvegardée
    etat_partie = charger_partie()
    if etat_partie:
        grille_joueur1 = etat_partie["grille_joueur1"]
        grille_joueur2 = etat_partie["grille_joueur2"]
        grille_tirs_joueur1 = etat_partie["grille_tirs_joueur1"]
        grille_tirs_joueur2 = etat_partie["grille_tirs_joueur2"]

    print("Placement des bateaux pour le joueur 1 :")
    placer_tous_les_bateaux(grille_joueur1)

    if mode_ia:
        if mode_ia == 'facile':
            print("Placement des bateaux pour l'IA (facile) :")
            placer_bateaux_automatique(grille_joueur2)
        elif mode_ia == 'difficile':
            print("Placement des bateaux pour l'IA (difficile) :")
            placer_bateaux_automatique(grille_joueur2)
    else:
        print("Placement des bateaux pour le joueur 2 :")
        placer_tous_les_bateaux(grille_joueur2)

    # Boucle de jeu principale
    tour = 0
    while True:
        print(f"\n--- Tour {tour + 1} ---")
        print("Grille des tirs du joueur 1 :")
        afficher_grille(grille_tirs_joueur1)

        if mode_ia:
            if tour % 2 == 0:  # Tour du joueur
                print("Tour du joueur 1.")
                jouer_tour(grille_joueur2, grille_tirs_joueur1)
            else:  # Tour de l'IA
                print("Tour de l'IA.")
                ligne_index, colonne_index = random.randint(0, 9), random.randint(0, 9)
                while grille_tirs_joueur2[ligne_index][colonne_index] in ['T', 'C']:
                    ligne_index, colonne_index = random.randint(0, 9), random.randint(0, 9)
                verifier_tir(grille_joueur1, grille_tirs_joueur2, ligne_index, colonne_index)
        else:
            print("Tour du joueur 1.")
            jouer_tour(grille_joueur2, grille_tirs_joueur1)

        # Vérification des bateaux coulés et condition de victoire
        if all(cell != 'X' for row in grille_joueur2 for cell in row):
            print("Le joueur 1 a gagné !")
            break

        print("Grille des tirs du joueur 2 :")
        afficher_grille(grille_tirs_joueur2)

        if mode_ia:
            if tour % 2 == 0:  # Tour de l'IA
                print("Tour de l'IA.")
                ligne_index, colonne_index = random.randint(0, 9), random.randint(0, 9)
                while grille_tirs_joueur1[ligne_index][colonne_index] in ['T', 'C']:
                    ligne_index, colonne_index = random.randint(0, 9), random.randint(0, 9)
                verifier_tir(grille_joueur1, grille_tirs_joueur1, ligne_index, colonne_index)
            else:  # Tour du joueur
                print("Tour du joueur 2.")
                jouer_tour(grille_joueur1, grille_tirs_joueur2)
        else:
            print("Tour du joueur 2.")
            jouer_tour(grille_joueur1, grille_tirs_joueur2)

        # Vérification des bateaux coulés et condition de victoire
        if all(cell != 'X' for row in grille_joueur1 for cell in row):
            print("Le joueur 2 a gagné !")
            break

        # Incrémentation du tour
        tour += 1

    # Sauvegarder l'état final de la partie
    sauvegarder_partie(grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2)

# Exemple de démarrage du jeu
if __name__ == "__main__":
    while True:
        mode_jeu = input("Mode de jeu (1 pour contre un joueur, 2 pour contre IA) : ")
        if mode_jeu == '1':
            jeu_bataille_navale()
            break
        elif mode_jeu == '2':
            while True:
                mode_ia = input("Difficulté de l'IA (facile/difficile) : ").lower()
                if mode_ia in ['facile', 'difficile']:
                    jeu_bataille_navale(mode_ia)
                    break
                print("Votre choix est invalide. Réessayez.")
            break
        else:
            print("Votre choix est invalide. Réessayez.")
