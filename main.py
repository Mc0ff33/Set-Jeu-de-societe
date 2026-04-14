import random
from itertools import product
import pygame
# from pygame.locals import *

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

def teinter_image(image_blanche: pygame.Surface, couleur_rgb: tuple[int, int, int]) -> pygame.Surface:
    """ Teint une image blanche sur fond transparent. """
    img_teintee: pygame.Surface = image_blanche.copy()
    # On remplit l'image avec la couleur RGB, en multipliant les pixels
    img_teintee.fill(couleur_rgb, special_flags=pygame.BLEND_RGBA_MULT)
    return img_teintee

class App:
    def __init__(self) -> None:
        self._running: bool = True
        self._display_surf: pygame.Surface = None # type: ignore
        self.size = self.width, self.height = 1000, 750

        # Etat du jeu
        self.etat_jeu = "EN_COURS"

        # Initialisation du moteur de jeu
        self.jeu = Jeu()
        self.jeu.distribuer(12)
        self.selection: list[Carte] = []                                # Stockage des cartes sélectionnées
        self.sprites_base: dict[tuple[int, int], pygame.Surface] = {}   # Stockage des 9 PNG blancs

        # Boutons et polices
        self.rect_bouton: pygame.Rect = pygame.Rect(400, 670, 200, 50) # (x, y, largeur, hauteur)
        self.rect_bouton_rejouer: pygame.Rect = pygame.Rect(400, 400, 200, 60)

        self.police: pygame.font.Font = None # type: ignore
        self.police_titre: pygame.font.Font = None # type: ignore

    def on_init(self) -> bool:
        pygame.init()
        self.police = pygame.font.SysFont(None, 28)
        self.police_titre = pygame.font.SysFont(None, 72)
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
                coef = 45 # coef multiplicateur pour ajuster la tailler en conservant le ratio
                img = pygame.transform.smoothscale(img, (1*coef, 2*coef))
                self.sprites_base[(f, r)] = img

        return True

    def dessiner_carte(self, carte: Carte, x: int, y: int):
        """ Dessine une carte à la position (x, y) et gère le surlignage. """

        rect_carte = pygame.Rect(x, y, LARGEUR_CARTE, HAUTEUR_CARTE)

        # Dessin du fond de la carte
        pygame.draw.rect(self._display_surf, (255, 255, 255), rect_carte, border_radius=10)

        # Feedback visuel (surlignage)
        if carte in self.selection:
            # Bordure bleue épaisse
            pygame.draw.rect(self._display_surf, (0, 120, 255), rect_carte, width=5, border_radius=10)
        else:
            # Bordure grise standard
            pygame.draw.rect(self._display_surf, (150, 150, 150), rect_carte, width=2, border_radius=10)

        # Récupération et teinte du sprite
        sprite_blanc: pygame.Surface = self.sprites_base[(carte.forme, carte.remplissage)]
        sprite_colore: pygame.Surface = teinter_image(sprite_blanc, COULEURS_RGB[carte.couleur])

        # Nombre de symboles à afficher sur la carte
        nb_symboles = carte.quantite + 1

        # Affichage des symboles centré verticalement
        largeur_symbole = sprite_colore.get_width()
        hauteur_symbole = sprite_colore.get_height()

        # Calcul de la place totale prise en largeur (avec 15px d'espace entre chaque)
        espace_total = nb_symboles * largeur_symbole + (nb_symboles - 1) * 15

        # Point de départ X pour que le bloc de symboles soit centré
        start_x = x + (LARGEUR_CARTE - espace_total) // 2

        # Point de départ Y fixe (pour centrer verticalement un seul symbole)
        img_y = y + (HAUTEUR_CARTE - hauteur_symbole) // 2

        # On dessine de gauche à droite
        for i in range(nb_symboles):
            img_x = start_x + i * (largeur_symbole + 15)
            self._display_surf.blit(sprite_colore, (img_x, img_y))

    def on_event(self, event: pygame.event.Event) -> None:
        """ Gestion des événements """
        if event.type == pygame.QUIT:
            self._running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos: tuple[int, int] = event.pos
            self.gerer_clic(mouse_pos)
    
    def gerer_clic(self, pos: tuple[int, int]) -> None:
        """ Calcule si on a cliqué sur un bouton ou sur une carte. """
        
        # Si la partie est terminée
        if self.etat_jeu == "TERMINE":
            if self.rect_bouton_rejouer.collidepoint(pos):
                self.reinitialiser_partie()
            return

        # Vérification du bouton "Plus de cartes"
        if self.rect_bouton.collidepoint(pos):
            # On vérifie s'il y a déjà un SET sur le plateau
            if self.jeu.chercher_un_set() is None:
                if len(self.jeu.paquet) > 0:
                    print("Aucun SET disponible. Ajout de 3 cartes.")
                    self.jeu.distribuer(3)
                else:
                    print("Le paquet est vide")
                    self._running = False
            else:
                print("Cherchez bien, il y a au moins un SET sur le plateau !")
            return

        # Calcule quelle carte a été cliquée
        for i, carte in enumerate(self.jeu.plateau):
            # On recrée virtuellement le rectangle de la carte pour test de collision
            colonne = i % 4
            ligne = i // 4
            x = MARGE + colonne * (LARGEUR_CARTE + MARGE)
            y = MARGE + ligne * (HAUTEUR_CARTE + MARGE)
            rect_carte: pygame.Rect = pygame.Rect(x, y, LARGEUR_CARTE, HAUTEUR_CARTE)

            if rect_carte.collidepoint(pos):
                if carte in self.selection:
                    self.selection.remove(carte) # Déselection
                else:
                    if len(self.selection) < 3:
                        self.selection.append(carte) # Sélection
                return
    
    def on_loop(self):
        """ Vérification des règles et de l'état """

        # On ne déclenche la vérification que si 3 cartes sont sélectionnées
        if len(self.selection) == 3:
            c1: Carte = self.selection[0]
            c2: Carte = self.selection[1]
            c3: Carte = self.selection[2]

            if self.jeu.est_un_set(c1, c2, c3):
                print("C'est un SET valide.")

                # On retire les cartes du plateau
                for carte in self.selection:
                    self.jeu.plateau.remove(carte)
                
                # On complète le plateau (si nécessaire)
                while len(self.jeu.plateau) < 12 and len(self.jeu.paquet) > 0:
                    self.jeu.distribuer(1)
            else:
                print("Ce n'est pas un SET.")
            
            # On vide la sélection
            self.selection.clear()
        
        # Vérification fin de partie
        if self.etat_jeu == "EN_COURS":
            if len(self.jeu.paquet) == 0 and self.jeu.chercher_un_set() is None:
                self.etat_jeu = "TERMINE"

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
        

        # Dessin du bouton
        couleur_bouton = (200, 200, 200) # Gris clair
        pygame.draw.rect(self._display_surf, couleur_bouton, self.rect_bouton, border_radius=8)
        pygame.draw.rect(self._display_surf, (100, 100, 100), self.rect_bouton, width=2, border_radius=8)

        # Rendu du texte
        if self.police:
            text_surface: pygame.Surface = self.police.render("Plus de cartes", True, (0, 0, 0))
            texte_rect: pygame.Rect = text_surface.get_rect(center=self.rect_bouton.center)
            self._display_surf.blit(text_surface, texte_rect)

        # Affiche conditionnel de l'écran de fin
        if self.etat_jeu == "TERMINE":
            # Voile noir semi-transparent
            overlay: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Le dernier élément du quadruplet quantifie la transparence
            self._display_surf.blit(overlay, (0, 0))

            # Titre de fin
            if self.police_titre:
                texte_fin = self.police_titre.render("Partie terminée !", True, (255, 255, 255))
                rect_fin = texte_fin.get_rect(center=(self.width // 2, self.height // 2 - 80))
                self._display_surf.blit(texte_fin, rect_fin)

            # Bouton Rejouer
            couleur_btn_rejouer: tuple[int, int, int] = (255, 200, 50) # Orange/Jaune
            pygame.draw.rect(self._display_surf, couleur_btn_rejouer, self.rect_bouton_rejouer, border_radius=10)
            pygame.draw.rect(self._display_surf, (255, 255, 255), self.rect_bouton_rejouer, width=3, border_radius=10)

            if self.police:
                texte_rejouer = self.police.render("Rejouer", True, (0, 0, 0))
                rect_rejouer_texte = texte_rejouer.get_rect(center=self.rect_bouton_rejouer.center)
                self._display_surf.blit(texte_rejouer, rect_rejouer_texte)
        
        pygame.display.flip() # Mise à jour de l'écran

    def reinitialiser_partie(self) -> None:
        """ Relance un toute nouvelle partie. """
        self.jeu = Jeu()
        self.jeu.distribuer(12)
        self.selection.clear()
        self.etat_jeu = "EN_COURS"
        print("\n--- NOUVELLE PARTIE ---")

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