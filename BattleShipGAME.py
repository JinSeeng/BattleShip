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

def sauvegarder_partie(grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2, fichier="sauvegarde.json"):
    """Sauvegarde l'état actuel de la partie dans un fichier"""
    etat_partie = {
        "grille_joueur1": grille_joueur1,
        "grille_joueur2": grille_joueur2,
        "grille_tirs_joueur1": grille_tirs_joueur1,
        "grille_tirs_joueur2": grille_tirs_joueur2,
    }
    with open(fichier, "w") as f:
        json.dump(etat_partie, f)
    print(f"Partie sauvegardée dans {fichier}")

def charger_partie(fichier="sauvegarde.json"):
    """Charge une partie depuis un fichier de sauvegarde"""
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            etat_partie = json.load(f)
            return (
                etat_partie["grille_joueur1"],
                etat_partie["grille_joueur2"],
                etat_partie["grille_tirs_joueur1"],
                etat_partie["grille_tirs_joueur2"],
            )
    else:
        print(f"Le fichier {fichier} n'existe pas.")
        return None, None, None, None

def choisir_adversaire():
    """Permet de choisir de jouer contre l'IA ou un autre joueur avec gestion des erreurs"""
    choix = input("Voulez-vous jouer contre un autre joueur (1) ou contre l'IA (2) ? ")
    while choix not in ['1', '2']:
        print("Choix invalide. Entrez 1 pour un autre joueur ou 2 pour l'IA.")
        choix = input("Voulez-vous jouer contre un autre joueur (1) ou contre l'IA (2) ? ")
    return choix

def choisir_difficulte_ia():
    """Permet de choisir la difficulté de l'IA avec gestion des erreurs"""
    choix = input("Choisissez la difficulté de l'IA - facile (1) ou difficile (2) : ")
    while choix not in ['1', '2']:
        print("Choix invalide. Entrez 1 pour facile ou 2 pour difficile.")
        choix = input("Choisissez la difficulté de l'IA - facile (1) ou difficile (2) : ")
    return choix

def demarrer_jeu():
    """Démarre le jeu de bataille navale avec tous les choix et configurations nécessaires"""
    # Initialisation des grilles pour les deux joueurs
    grille_joueur1 = initialiser_grille()
    grille_joueur2 = initialiser_grille()
    grille_tirs_joueur1 = initialiser_grille()
    grille_tirs_joueur2 = initialiser_grille()

    print("Bienvenue dans le jeu de bataille navale !")

    # Choix de l'adversaire
    adversaire = choisir_adversaire()

    if adversaire == '1':
        print("Vous jouez contre un autre joueur.")
        print("Joueur 1, placez vos bateaux :")
        placer_tous_les_bateaux(grille_joueur1)
        print("Joueur 2, placez vos bateaux :")
        placer_tous_les_bateaux(grille_joueur2)
    else:
        print("Vous jouez contre l'IA.")
        difficulte_ia = choisir_difficulte_ia()
        print("Joueur, placez vos bateaux :")
        placer_tous_les_bateaux(grille_joueur1)
        print("Placement automatique des bateaux de l'IA...")
        placement_automatique_ia(grille_joueur2)

    # Boucle du jeu
    jeu_termine = False
    tour_joueur1 = True  # Le joueur 1 commence toujours

    while not jeu_termine:
        if tour_joueur1:
            print("Tour du joueur 1")
            afficher_grille(grille_tirs_joueur1)
            touche = jouer_tour(grille_joueur2, grille_tirs_joueur1)
        else:
            if adversaire == '1':
                print("Tour du joueur 2")
                afficher_grille(grille_tirs_joueur2)
                touche = jouer_tour(grille_joueur1, grille_tirs_joueur2)
            else:
                print("Tour de l'IA")
                if difficulte_ia == '1':
                    ligne, colonne = ia_facile(grille_joueur1, grille_tirs_joueur2)
                else:
                    ligne, colonne = ia_intelligente(grille_joueur1, grille_tirs_joueur2)
                touche = verifier_tir(grille_joueur1, grille_tirs_joueur2, ligne, colonne)
                afficher_grille(grille_tirs_joueur2)

        # Vérification de la fin du jeu
        if all(cell != 'X' for row in grille_joueur2 for cell in row):
            print("Le joueur 1 a gagné !")
            jeu_termine = True
        elif all(cell != 'X' for row in grille_joueur1 for cell in row):
            print("Le joueur 2 a gagné !" if adversaire == '1' else "L'IA a gagné !")
            jeu_termine = True

        # Changement de tour
        tour_joueur1 = not tour_joueur1

if __name__ == "__main__":
    demarrer_jeu()
