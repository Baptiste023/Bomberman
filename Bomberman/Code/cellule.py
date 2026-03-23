import pygame
from settings import *

class Cellule:
    def __init__(self, ligne, colonne, taille_cellule):
        self.ligne = ligne
        self.colonne = colonne
        self.taille_cellule = taille_cellule
        self.etat = VIDE
        self.type_explosion = None

        self.x = colonne * taille_cellule
        self.y = ligne * taille_cellule

        self.explosion_end_time = 0

    def set_etat(self, etat):
        self.etat = etat
        if etat != EXPLOSION:
            self.type_explosion = None

