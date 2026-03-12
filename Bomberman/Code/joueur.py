import pygame
from settings import *

class Joueur:
    def __init__(self, ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne

        # bombes dict {(l,c): {"pose_time":..., "armed":bool}}
        self.bombes = {}

        # Cooldown déplacement
        self.temps_dernier_deplacement = 0
        self.temps_min_entre_2_deplacement = MOVE_COOLDOWN_MS

        # Cooldown bombes
        self.temps_derniere_bombe = 0
        self.temps_min_entre_2_bombe = BOMB_COOLDOWN_MS

    def dessiner(self, screen, assets):
        x = self.colonne * TAILLE_CELLULE
        y = self.ligne * TAILLE_CELLULE
        screen.blit(assets["personnage"], (x, y))


    def can_walk_on(self, cell):
        return cell.etat == VIDE or cell.etat == DESTRUCTIBLE

    def movement(self, grille, d_ligne, d_colonne):
        now = pygame.time.get_ticks()

        if now - self.temps_dernier_deplacement < self.temps_min_entre_2_deplacement:
            return

        nl = self.ligne + d_ligne
        nc = self.colonne + d_colonne

        if not grille.in_bounds(nl, nc):
            return

        cell_cible = grille.get_cellule(nl, nc)

        if self.can_walk_on(cell_cible):
            # si on quitte une bombe non armée, on l'arme
            pos_actuelle = (self.ligne, self.colonne)
            if pos_actuelle in self.bombes and self.bombes[pos_actuelle]["armed"] is False:
                self.bombes[pos_actuelle]["armed"] = True
                grille.get_cellule(*pos_actuelle).set_etat(BOMBE)

            self.ligne = nl
            self.colonne = nc
            self.temps_dernier_deplacement = now

    def deposer_bombe(self, grille):
        now = pygame.time.get_ticks()

        if now - self.temps_derniere_bombe < self.temps_min_entre_2_bombe:
            return

        pos = (self.ligne, self.colonne)
        if pos in self.bombes:
            return

        # bombe posée sous le joueur, non armée tant qu'il reste dessus
        self.bombes[pos] = {"pose_time": now, "armed": False}
        self.temps_derniere_bombe = now

    def trigger_explosion(self, grille, centre_l, centre_c, now):

        def explode_cell(l, c, type_explosion):
            cell = grille.get_cellule(l, c)
            cell.set_etat(EXPLOSION)
            cell.type_explosion = type_explosion
            cell.explosion_end_time = now + EXPLOSION_DURATION_MS

        explode_cell(centre_l, centre_c, "centre")

        directions = [
            (-1, 0, "verticale", "bout_h"),
            (1, 0, "verticale", "bout_b"),
            (0, -1, "horizontale", "bout_g"),
            (0, 1, "horizontale", "bout_d"),
        ]

        for dl, dc, type_ligne, type_bout in directions:
            for step in range(1, PORTEE_EXPLOSION + 1):
                nl = centre_l + dl * step
                nc = centre_c + dc * step

                if not grille.in_bounds(nl, nc):
                    break

                cell = grille.get_cellule(nl, nc)

                if cell.etat == MUR:
                    break

                type_case = type_bout if step == PORTEE_EXPLOSION else type_ligne

                if cell.etat == DESTRUCTIBLE:
                    explode_cell(nl, nc, type_case)
                    break

                if cell.etat == BOMBE:
                    explode_cell(nl, nc, type_case)
                    break

                explode_cell(nl, nc, type_case)
    def gestion_bombes(self, grille):
        now = pygame.time.get_ticks()
        to_remove = []

        for (bl, bc), info in self.bombes.items():
            if now - info["pose_time"] >= BOMBE_DELAY_MS:
                self.trigger_explosion(grille, bl, bc, now)
                to_remove.append((bl, bc))

        for pos in to_remove:
            self.bombes.pop(pos, None)

    def Mort_joueur(self, grille):
        cellule = grille.get_cellule(self.ligne, self.colonne)
        return cellule.etat == EXPLOSION