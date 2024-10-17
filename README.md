# BattleShip

## Description
Bataille Navale est un jeu de stratégie où deux joueurs s'affrontent pour couler les bateaux de l'adversaire. Chaque joueur dispose d'une grille de 10x10 sur laquelle il place 5 bateaux de différentes tailles. Le but du jeu est de couler tous les bateaux de l'adversaire en tirant sur les cases de sa grille.

## Installation

Pour installer le jeu, suivez ces étapes :

1. **Clonez le dépôt** : 
   ```bash
   git clone https://github.com/votre-utilisateur/bataille-navale.git
   cd bataille-navale
   ```

2. **Assurez-vous d'avoir Python installé** :
   Ce projet nécessite Python 3.7 ou supérieur. Vous pouvez télécharger Python [ici](https://www.python.org/downloads/).

3. **Installer Tkinter** :
   Tkinter est généralement inclus avec Python. Si ce n'est pas le cas, installez-le avec votre gestionnaire de paquets.
    - Pour Ubuntu :
      ```bash
      sudo apt-get install python3-tk
      ```
    - Pour Windows, assurez-vous de cocher l'option lors de l'installation de Python.

## Lancement du Jeu

Pour lancer le jeu, exécutez le script Python :

```bash
python main.py
```

Assurez-vous que vous êtes dans le répertoire du projet.

## Règles du Jeu

1. **Préparation** :
    - Chaque joueur place 5 bateaux sur sa grille. Les bateaux et leurs tailles sont les suivants :
        - **Porte-avions** (5 cases)
        - **Croiseur** (4 cases)
        - **Contre-torpilleur** (3 cases)
        - **Sous-marin** (3 cases)
        - **Torpilleur** (2 cases)

2. **Placement des bateaux** :
    - Les bateaux peuvent être placés horizontalement ou verticalement, mais ne peuvent pas se chevaucher ou sortir des limites de la grille.

3. **Déroulement du jeu** :
    - Les joueurs s'alternent pour tirer sur les cases de la grille de l'adversaire.
    - Un joueur annonce une case (par exemple, B3) pour tirer.
    - Si la case contient un bateau, c'est un "touché". Si c'est une case d'eau, c'est un "manqué".
    - Lorsqu'un joueur touche toutes les cases d'un bateau, il annonce que le bateau est "coulé".

4. **Fin de la partie** :
    - Le jeu se termine lorsque tous les bateaux d'un joueur sont coulés. Le joueur qui a réussi à couler tous les bateaux de l'adversaire remporte la partie.

## Auteur
- NADE Sellia

## Sources
- Mon Python Pas à Pas - Tkintker : https://sites.google.com/site/pythonpasapas/modules/tkinter/tkinter-methodes/tkinter-grid
- Docs Python : https://docs.python.org/3/library/tkinter.ttk.html#module-tkinter.ttk
- Tailwindcss : https://tailwindcss.com/docs/grid-column
- ChatGPT : https://chatgpt.com
