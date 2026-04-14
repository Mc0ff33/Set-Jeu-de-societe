# SET - Implémentation en Python (Pygame)

## Description
Ce projet est une implémentation numérique du jeu de société classique "SET", développée en Python à l'aide de la bibliothèque Pygame. Le programme gère la logique complète du jeu, l'affichage graphique interactif, la détection des SETs valides et la distribution automatique des cartes selon les règles officielles.

## Prérequis
- Python 3.x
- Bibliothèque `pygame`

## Installation et exécution
1. Cloner le dépôt sur votre machine locale.
2. Installer la bibliothèque Pygame (si ce n'est pas déjà fait) :
   ```bash
   pip install pygame
   ```
3. Exécuter le fichier principal depuis le répertoire racine du projet :
   ```bash
   python main.py
   ```

## Utilisation et contrôles
- **Sélection des cartes** : Clic gauche sur une carte pour la sélectionner (mise en évidence par une bordure bleue). Un second clic permet de la désélectionner.
- **Validation** : Dès que 3 cartes sont sélectionnées, le programme vérifie automatiquement la validité du SET. S'il est valide, les cartes sont retirées et remplacées selon les règles. S'il est invalide, la sélection est annulée.
- **Bouton "Plus de cartes"** : Permet de distribuer 3 cartes supplémentaires. Conformément aux règles, cette action n'est permise que si aucun SET n'est présent parmi les cartes actuellement exposées sur le plateau.
- **Fin de partie** : Lorsque le paquet est épuisé et qu'aucun SET ne peut plus être formé sur le plateau, un écran de fin s'affiche avec la possibilité de recommencer la partie.

## Règles du jeu (Rappel)
Chaque carte présente des symboles caractérisés par 4 attributs, ayant chacun 3 déclinaisons possibles :
- **Forme** : Losange, Ovale, Vague
- **Couleur** : Rouge, Violet, Vert
- **Quantité** : 1, 2 ou 3 symboles
- **Remplissage** : Plein, Vide, Hachuré

**Condition de victoire (Le SET) :**
Trois cartes forment un SET si et seulement si, pour chacune des 4 caractéristiques, l'état de l'attribut est **soit strictement identique** sur les 3 cartes, **soit totalement différent** sur les 3 cartes.

## Structure du projet
```text
.
├── main.py                                 # Moteur du jeu et interface graphique
├── readme.md                               # Documentation du dépôt
├── SET INSTRUCTIONS - FRENCH_0.pdf         # Règles officielles
└── resources/
    └── cards/                              # Sprites de base (9 images PNG transparentes)
        ├── losange_hachure.png
        ├── losange_plein.png
        ├── losange_vide.png
        ├── ovale_hachure.png
        ├── ovale_plein.png
        ├── ovale_vide.png
        ├── vague_hachure.png
        ├── vague_plein.png
        └── vague_vide.png
```

## Crédits
Le concept original du jeu SET est une marque déposée de SET Enterprises Inc.