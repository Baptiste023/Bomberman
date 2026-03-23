from cellule import Cellule
from settings import *

class Grille:
    def __init__(self):
        self.ligne = ROW
        self.colonne = COL
        self.cellules = []

        for i in range(ROW):
            ligne_cellules = []
            for j in range(COL):
                c = Cellule(i, j, TAILLE_CELLULE)

                # Coins départ joueurs à laisser vides
                if (i == 1 and j in [1, 2]) or (i == 2 and j == 1):
                    c.set_etat(VIDE)
                elif (i == ROW - 2 and j in [COL - 2, COL - 3]) or (i == ROW - 3 and j == COL - 2):
                    c.set_etat(VIDE)
                # Bordures
                elif i == 0 or i == ROW - 1 or j == 0 or j == COL - 1:
                    c.set_etat(MUR)
                # Piliers intérieurs
                elif i % 2 == 0 and j % 2 == 0:
                    c.set_etat(MUR)
                # Le reste = destructible
                else:
                    c.set_etat(DESTRUCTIBLE)

                ligne_cellules.append(c)
            self.cellules.append(ligne_cellules)

    def dessiner(self, screen, assets):


        for ligne in self.cellules:
            for c in ligne:
                if c.etat == MUR :
                    x = c.colonne * TAILLE_CELLULE
                    y = c.ligne * TAILLE_CELLULE
                    screen.blit(assets["mur"], (x, y))
                if c.etat == DESTRUCTIBLE :
                    x = c.colonne * TAILLE_CELLULE
                    y = c.ligne * TAILLE_CELLULE
                    screen.blit(assets["destructible"], (x, y))
                if c.etat == VIDE:
                    x = c.colonne * TAILLE_CELLULE
                    y = c.ligne * TAILLE_CELLULE
                    screen.blit(assets["herbe"], (x, y))
                if c.etat == BOMBE :
                    x = c.colonne * TAILLE_CELLULE
                    y = c.ligne * TAILLE_CELLULE
                    screen.blit(assets["bombe"], (x, y))
                if c.etat == EXPLOSION:
                    x = c.colonne * TAILLE_CELLULE
                    y = c.ligne * TAILLE_CELLULE
                    screen.blit(assets[c.type_explosion], (x,y))

    def get_cellule(self, ligne, colonne):
        return self.cellules[ligne][colonne]

    def in_bounds(self, ligne, colonne):
        return 0 <= ligne < self.ligne and 0 <= colonne < self.colonne

    def update_explosions(self, now_ms):
        for ligne in self.cellules:
            for c in ligne:
                if c.etat == EXPLOSION and now_ms >= c.explosion_end_time:
                    c.set_etat(VIDE)
                    c.explosion_end_time = 0
