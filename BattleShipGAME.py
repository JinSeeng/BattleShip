import random
import json
import os

# Statistiques des joueurs (victoires/défaites)
statistiques_joueurs = {}

# Initialisation de la grille pour les deux joueurs
def initialiser_grille():
    """Crée une grille de 10x10 vide pour le jeu"""
    return [[' ' for _ in range(10)] for _ in range(10)]

def afficher_grille(grille, masquer_bateaux=False):
    """Affiche la grille de jeu avec les coordonnées. Si masquer_bateaux est True, les bateaux sont cachés"""
    print("   A B C D E F G H I J")
    print("  +" + "-+" * 10)
    for i, ligne in enumerate(grille):
        print(f"{i+1:2}|{'|'.join(' ' if cell == 'X' and masquer_bateaux else cell for cell in ligne)}|")
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
        return None

    with open(fichier_sauvegarde, 'r') as f:
        etat_partie = json.load(f)

    return (etat_partie['grille_joueur1'], etat_partie['grille_joueur2'],
            etat_partie['grille_tirs_joueur1'], etat_partie['grille_tirs_joueur2'])

def initialiser_partie():
    """Initialise les grilles et demande au joueur de choisir entre une partie sauvegardée ou nouvelle"""
    charger = input("Voulez-vous charger une partie sauvegardée ? (o/n) : ").lower()
    if charger == 'o':
        partie = charger_partie()
        if partie:
            return partie
        else:
            print("Aucune partie à charger, démarrage d'une nouvelle partie.")
    grille_joueur1 = initialiser_grille()
    grille_joueur2 = initialiser_grille()
    grille_tirs_joueur1 = initialiser_grille()
    grille_tirs_joueur2 = initialiser_grille()

    return grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2

def choisir_adversaire():
    """Permet au joueur de choisir s'il veut jouer contre un autre joueur ou une IA"""
    choix = input("Voulez-vous jouer contre un autre joueur ou une IA ? (1: Joueur, 2: IA) : ")
    while choix not in ['1', '2']:
        print("Choix invalide.")
        choix = input("Voulez-vous jouer contre un autre joueur ou une IA ? (1: Joueur, 2: IA) : ")

    if choix == '2':
        difficulte = input("Choisissez la difficulté de l'IA (1: Facile, 2: Difficile) : ")
        while difficulte not in ['1', '2']:
            print("Difficulté invalide.")
            difficulte = input("Choisissez la difficulté de l'IA (1: Facile, 2: Difficile) : ")
        return 'IA', difficulte
    return 'Joueur', None

def afficher_statistiques():
    """Affiche les statistiques de victoires et défaites des joueurs"""
    if statistiques_joueurs:
        print("Classement des joueurs :")
        for joueur, stats in statistiques_joueurs.items():
            print(f"{joueur}: {stats['victoires']} victoires, {stats['defaites']} défaites")
    else:
        print("Aucune statistique disponible.")

def mettre_a_jour_statistiques(nom_joueur, victoire):
    """Met à jour les statistiques de victoires et défaites pour un joueur"""
    if nom_joueur not in statistiques_joueurs:
        statistiques_joueurs[nom_joueur] = {'victoires': 0, 'defaites': 0}
    if victoire:
        statistiques_joueurs[nom_joueur]['victoires'] += 1
    else:
        statistiques_joueurs[nom_joueur]['defaites'] += 1

def demander_nom_joueur(numero_joueur):
    """Demande le nom du joueur"""
    return input(f"Nom du joueur {numero_joueur}: ")

# Démarrage de la partie
"""Démarre une partie de bataille navale"""
print("Bienvenue dans la Bataille Navale !")
grille_joueur1, grille_joueur2, grille_tirs_joueur1, grille_tirs_joueur2 = initialiser_partie()
adversaire, difficulte_ia = choisir_adversaire()
nom_joueur1 = demander_nom_joueur(1)
nom_joueur2 = None if adversaire == 'IA' else demander_nom_joueur(2)

print(f"{nom_joueur1}, placez vos bateaux.")
placer_tous_les_bateaux(grille_joueur1)
if adversaire == 'IA':
    print("L'IA place ses bateaux.")
    placement_automatique_ia(grille_joueur2)
else:
    print(f"{nom_joueur2}, placez vos bateaux.")
    placer_tous_les_bateaux(grille_joueur2)

# Affichage des statistiques à la fin de la partie
afficher_statistiques()