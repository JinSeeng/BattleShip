import random

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
    """Demande au joueur de placer un bateau sur la grille"""
    print(f"Où voulez-vous placer votre {nom_bateau} ({taille_bateau} cases) ?")
    orientation = input("Orientation (H pour horizontal, V pour vertical) : ").upper()
    colonne = input("Colonne (A-J) : ").upper()
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