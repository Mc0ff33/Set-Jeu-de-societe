import random
from itertools import product
import pygame
from pygame.locals import *

class Carte:
    def __init__(self, forme:int, couleur:int, quantite:int, remplissage:int) -> None:
        """
        Forme : 0 = Losange, 1 = Ovale, 2 = Vague.
        Couleur : 0 = Rouge, 1 = Violet, 2 = Vert.
        Quantité : 0, 1, 2.
        Remplissage : 0 = Hachuré, 1 = Plein, 2 = Vide.
        """
        self.forme = forme
        self.couleur = couleur
        self.quantite = quantite
        self.remplissage = remplissage

    def afficher_texte(self) -> None:
        f = self.forme
        c = self.couleur
        q = self.quantite
        r = self.remplissage
        print(f"Carte ({f}, {c}, {q}, {r})")

class Jeu:
    def __init__(self) -> None:
        self.paquet: list[Carte] = self._generer_paquet()
        self.plateau: list[Carte] = []
        self.melanger()

    def _generer_paquet(self) -> list[Carte]:
        """ Génère les 81 cartes du jeu. """
        cartes = []
        for f, c, q, r in product([0, 1, 2], repeat=4):
            cartes.append(Carte(f, c, q, r))
        return cartes

    def melanger(self) -> None:
        """ Mélange les cartes restantes dans le paquet. """
        random.shuffle(self.paquet)

    def distribuer(self, nombre=12):
        """ Tire un nombre donné de cartes du paquet
        pour les mettre sur le plateau. """
        for _ in range(nombre):
            if self.paquet: # On vérifie qu'il reste des cartes
                self.plateau.append(self.paquet.pop())

    def est_un_set(self, c1:Carte, c2:Carte, c3:Carte) -> bool:
        """ Vérifie si 3 cartes forme un set valide. """
        # On regroupe les caractéristiques dans des ensembles (pas de doublons).
        formes = {c1.forme, c2.forme, c3.forme}
        couleurs = {c1.couleur, c2.couleur, c3.couleur}
        quantites = {c1.quantite, c2.quantite, c3.quantite}
        remplissages = {c1.remplissage, c2.remplissage, c3.remplissage}

        # [On a un set] ssi [la taille de l'ensemble est 1 ou 3]
        # i.e. les 3 sont identiques ou les 3 sont différents.
        return (
            len(formes) in [1, 3] and
            len(couleurs) in [1, 3] and
            len(quantites) in [1, 3] and
            len(remplissages) in [1, 3]
        )
    
    def afficher_plateau(self):
        print('-' * 32)
        for carte in self.plateau:
            carte.afficher_texte()

    def chercher_un_set(self) -> list[Carte] | None:
        n = len(self.plateau)
        for i in range(n-2):
            for j in range(i+1, n-1):
                for k in range(j+1, n):
                    c1, c2, c3 = self.plateau[i], self.plateau[j], self.plateau[k]
                    if self.est_un_set(c1, c2, c3):
                        return [c1, c2, c3]
        return None
    
    def jouer_seul(self) -> None:
        partie_en_cours = True
        
        while partie_en_cours:
            self.afficher_plateau()
            set_trouve = self.chercher_un_set()
            
            if set_trouve:
                print("\n*** SET ! ***")
                for carte in set_trouve:
                    carte.afficher_texte()
                    self.plateau.remove(carte)
                
                # On ne complète que si on a moins de 12 cartes sur la table
                while len(self.plateau) < 12 and len(self.paquet) > 0:
                    self.distribuer(1)
            else:
                if len(self.paquet) > 0:
                    print("\nPas de set sur le plateau. On ajoute 3 cartes.")
                    self.distribuer(3)
                else:
                    print("\nPlus de set possible et le paquet est vide. Fin de la partie !")
                    partie_en_cours = False



# Constantes visuelles
NOMS_FORMES = {0: "losange", 1: "ovale", 2: "vague"}
NOMS_REMPLISSAGES = {0: "hachure", 1: "plein", 2: "vide"}

# Couleurs RGB
COULEURS_RGB = {
    0: (238, 29, 35),   # Rouge
    1: (72, 46, 146),   # Violet
    2: (33, 178, 89)    # Vert
}

# Dimensions
LARGEUR_CARTE, HAUTEUR_CARTE = 220, 140
MARGE = 20

def teinter_image(image_blanche, couleur_rgb):
    """ Teint une image blanche sur fond transparent. """
    img_teintee = image_blanche.copy()
    # On remplit l'image avec la couleur RGB, en multipliant les pixels
    img_teintee.fill(couleur_rgb, special_flags=pygame.BLEND_RGBA_MULT)
    return img_teintee

class App:
    def __init__(self):
        self._running = True
        self._display_surf: pygame.Surface = None
        self.size = self.width, self.height = 1000, 600

        # Initialisation du moteur de jeu
        self.jeu = Jeu()
        self.jeu.distribuer(12)

        # Stockage des 9 PNG blancs
        self.sprites_base = {}

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Jeu de SET !")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        # Chargement en mémoire des 9 images
        nom_dossier = 'resources/cards'
        for f in [0, 1, 2]:
            for r in [0, 1, 2]:
                nom_fichier = f"{NOMS_FORMES[f]}_{NOMS_REMPLISSAGES[r]}.png"
                chemin_fichier = nom_dossier + '/' + nom_fichier
                # convert_alpha() permet de conserver la transparence
                img = pygame.image.load(chemin_fichier).convert_alpha()
                # Redimensionnement de l'image si l'originale est trop grande
                img = pygame.transform.smoothscale(img, (120, 60))
                self.sprites_base[(f, r)] = img

        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def dessiner_carte(self, carte: Carte, x: int, y: int):
        """ Dessine une carte à la position (x, y) """
        # Dessin du fond de la carte
        rect_carte = pygame.Rect(x, y, LARGEUR_CARTE, HAUTEUR_CARTE)
        pygame.draw.rect(self._display_surf, (255, 255, 255), rect_carte, border_radius=10)
        pygame.draw.rect(self._display_surf, (150, 150, 150), rect_carte, width=2, border_radius=10)

        # Récupération et teinte du sprite
        sprite_blanc = self.sprites_base[(carte.forme, carte.remplissage)]
        sprite_colore = teinter_image(sprite_blanc, COULEURS_RGB[carte.couleur])

        # Nombre de symboles à afficher sur la carte
        nb_symboles = carte.quantite + 1

        # Affichage des symboles centré verticalement
        hauteur_symbole = sprite_colore.get_height()
        espace_total = nb_symboles * hauteur_symbole + (nb_symboles - 1) * 10
        start_y = y + (HAUTEUR_CARTE - espace_total) // 2

        img_x = x + (LARGEUR_CARTE - sprite_colore.get_width()) // 2
        for i in range(nb_symboles):
            img_y = start_y + i * (hauteur_symbole + 10)
            self._display_surf.blit(sprite_colore, (img_x, img_y))
    
    def on_loop(self):
        pass

    def on_render(self):
        # Fond de la fenêtre
        self._display_surf.fill((230, 240, 250))

        # Dessiner toutes les cartes du plateau
        for i, carte in enumerate(self.jeu.plateau):
            # Calcul de la colonne (x) et de la ligne (y) pour une grille 4x3
            colonne = i % 4
            ligne = i // 4

            x = MARGE + colonne * (LARGEUR_CARTE + MARGE)
            y = MARGE + ligne * (HAUTEUR_CARTE + MARGE)

            self.dessiner_carte(carte, x, y)
        
        pygame.display.flip() # Mise à jour de l'écran

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        
        self.on_cleanup()

if __name__ == "__main__":
    the_app = App()
    the_app.on_execute()