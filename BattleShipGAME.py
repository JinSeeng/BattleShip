import random
import json
import os

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

def demander_tir():
    """Demande au joueur une case à attaquer"""
    colonne = input("Colonne à attaquer (A-J) : ").upper()
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
        # Vérifier s'il y a de la place pour le bateau
        for i in range(taille):
            if grille[ligne][col_debut + i] != ' ':
                return placer_bateau_aleatoire(grille, taille)  # Recommence si l'emplacement est occupé
        # Placer le bateau
        for i in range(taille):
            grille[ligne][col_debut + i] = 'X'
    else:
        col = random.randint(0, 9)
        ligne_debut = random.randint(0, 10 - taille)
        # Vérifier s'il y a de la place pour le bateau
        for i in range(taille):
            if grille[ligne_debut + i][col] != ' ':
                return placer_bateau_aleatoire(grille, taille)  # Recommence si l'emplacement est occupé
        # Placer le bateau
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

def jouer_contre_ia(mode_ia):
    """Fonction de jeu contre l'IA avec une logique d'attaque intelligente pour le mode difficile."""
    grille_joueur1 = initialiser_grille()
    grille_ia = initialiser_grille()

    grille_tirs_joueur1 = initialiser_grille()
    grille_tirs_ia = initialiser_grille()

    # Placer les bateaux pour le joueur
    print("Placement des bateaux pour le joueur 1 :")
    placer_tous_les_bateaux(grille_joueur1)

    # Placer les bateaux pour l'IA
    print("Placement des bateaux pour l'IA :")
    placer_bateaux_automatique(grille_ia)

    # Boucle de jeu principale
    tour = 0
    while True:
        print(f"\n--- Tour {tour + 1} ---")
        print("Grille des tirs du joueur 1 :")
        afficher_grille(grille_tirs_joueur1)

        if jouer_tour(grille_ia, grille_tirs_joueur1):
            # Vérifier si l'IA est coulée
            if all(cell != 'X' for row in grille_ia for cell in row):
                print("Félicitations ! Vous avez coulé tous les bateaux de l'IA !")
                break
        else:
            print("C'est au tour de l'IA de jouer.")
            # IA joue
            if mode_ia == "facile":
                ligne_ia = random.randint(0, 9)
                colonne_ia = random.randint(0, 9)
            else:  # mode difficile
                # Ici, nous pourrions implémenter une logique d'attaque intelligente
                ligne_ia, colonne_ia = intelligent_attack(grille_joueur1, grille_tirs_ia)

            verifier_tir(grille_joueur1, grille_tirs_ia, ligne_ia, colonne_ia)
            print(f"L'IA a tiré sur {chr(colonne_ia + 65)}{ligne_ia + 1}.")

            # Vérifier si le joueur est coulé
            if all(cell != 'X' for row in grille_joueur1 for cell in row):
                print("Dommage ! L'IA a coulé tous vos bateaux.")
                break

        tour += 1

def intelligent_attack(grille_joueur, grille_tirs):
    """Logique d'attaque intelligente pour l'IA (difficile)"""
    # Cette fonction doit être développée pour rendre l'IA plus intelligente en fonction des attaques précédentes.
    # Pour l'instant, faisons une attaque aléatoire.
    while True:
        ligne = random.randint(0, 9)
        colonne = random.randint(0, 9)
        if grille_tirs[ligne][colonne] not in ['T', 'C']:  # Vérifier que cette case n'a pas été déjà attaquée
            return ligne, colonne

def jouer():
    """Fonction principale pour gérer le jeu et l'interaction avec le joueur"""
    grille_joueur1 = initialiser_grille()
    grille_joueur2 = initialiser_grille()

    grille_tirs_joueur1 = initialiser_grille()
    grille_tirs_joueur2 = initialiser_grille()

    # Placer les bateaux pour le joueur 1
    print("Placement des bateaux pour le joueur 1 :")
    placer_tous_les_bateaux(grille_joueur1)

    # Placer les bateaux pour le joueur 2
    print("Placement des bateaux pour le joueur 2 :")
    placer_tous_les_bateaux(grille_joueur2)

    # Boucle de jeu principale
    tour = 0
    while True:
        print(f"\n--- Tour {tour + 1} ---")
        print("Grille des tirs du joueur 1 :")
        afficher_grille(grille_tirs_joueur1)

        if jouer_tour(grille_joueur2, grille_tirs_joueur1):
            # Vérifier si le joueur 2 est coulé
            if all(cell != 'X' for row in grille_joueur2 for cell in row):
                print("Félicitations ! Le joueur 1 a coulé tous les bateaux du joueur 2 !")
                break

        print("Grille des tirs du joueur 2 :")
        afficher_grille(grille_tirs_joueur2)

        if jouer_tour(grille_joueur1, grille_tirs_joueur2):
            # Vérifier si le joueur 1 est coulé
            if all(cell != 'X' for row in grille_joueur1 for cell in row):
                print("Félicitations ! Le joueur 2 a coulé tous les bateaux du joueur 1 !")
                break

        tour += 1

# Menu principal
if __name__ == "__main__":
    print("Bienvenue dans le jeu de la Bataille Navale !")

    while True:  # Boucle pour continuer à demander un choix
        choix = input("Voulez-vous jouer contre un autre joueur (1) ou contre l'IA (2) ? ")

        if choix == "1":
            jouer()
            break  # Sortir de la boucle si un choix valide est effectué
        elif choix == "2":
            niveau_ia = input("Choisissez le niveau de l'IA (facile/difficile) : ").lower()
            jouer_contre_ia(niveau_ia)
            break  # Sortir de la boucle si un choix valide est effectué
        else:
            print("Choix non valide. Veuillez choisir 1 ou 2.")

