import pygame

from joueur import Joueur
from settings import PORTEE_EXPLOSION, MUR, DESTRUCTIBLE, VIDE, TAILLE_CELLULE,MOVE_COOLDOWN_BOT_MS,EXPLOSION
import random
from collections import deque

class Bot(Joueur):
    def __init__(self, ligne, colonne):
        super().__init__(ligne, colonne)

        self.temps_min_entre_2_deplacement = MOVE_COOLDOWN_BOT_MS

    def danger(self, grille, bombes, ligne, colonne):
        l_bot = ligne
        c_bot = colonne

        if grille.in_bounds(l_bot, c_bot):
            cellule = grille.get_cellule(l_bot, c_bot)
            if cellule.etat == EXPLOSION:
                return True

        for (l_bombe, c_bombe) in bombes:

            # Même ligne
            if l_bot == l_bombe:
                distance = abs(c_bot - c_bombe)

                if distance <= PORTEE_EXPLOSION:
                    obstacle = False

                    for c in range(min(c_bombe, c_bot)+1, max(c_bombe, c_bot)):
                        cellule = grille.get_cellule(l_bot, c)
                        if cellule.etat in (MUR, DESTRUCTIBLE):
                            obstacle = True
                            break

                    if not obstacle:
                        return True

            # Même colonne
            if c_bot == c_bombe:
                distance = abs(l_bot - l_bombe)

                if distance <= PORTEE_EXPLOSION:
                    obstacle = False

                    for l in range(min(l_bombe, l_bot)+1, max(l_bombe, l_bot)):
                        cellule = grille.get_cellule(l, c_bot)
                        if cellule.etat in (MUR, DESTRUCTIBLE):
                            obstacle = True
                            break

                    if not obstacle:
                        return True

        return False

    def case_accessible(self, grille, ligne, colonne):
        if not grille.in_bounds(ligne, colonne):
            return False

        cellule = grille.get_cellule(ligne, colonne)
        if cellule.etat == EXPLOSION :
            return False
        return cellule.etat == VIDE

    def voisines_accessibles(self, grille, ligne, colonne):
        voisines = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dl, dc in directions:
            nl = ligne + dl
            nc = colonne + dc

            if self.case_accessible(grille, nl, nc):
                voisines.append((nl, nc))

        return voisines

    def fuite(self, grille, ligne, colonne, bombes):
        depart = (ligne, colonne)
        visited = {depart}
        queue = deque()

        for nl, nc in self.voisines_accessibles(grille, ligne, colonne):
            queue.append(((nl, nc), (nl, nc)))
            visited.add((nl, nc))

        cases_fuite = []

        while queue:
            (cl, cc), premier_pas = queue.popleft()

            if not self.danger(grille, bombes, cl, cc):
                cases_fuite.append(premier_pas)
                continue

            for nl, nc in self.voisines_accessibles(grille, cl, cc):
                if (nl, nc) not in visited:
                    visited.add((nl, nc))
                    queue.append(((nl, nc), premier_pas))

        return cases_fuite

    def choisir_case(self, grille, ligne, colonne, bombes):
        cases = self.fuite(grille, ligne, colonne, bombes)

        if len(cases) == 0:
            return None

        return random.choice(cases)

    def move(self, grille, bombes):
        case = self.choisir_case(grille, self.ligne, self.colonne, bombes)

        if case is not None:
            dl = case[0] - self.ligne
            dc = case[1] - self.colonne
            self.movement(grille, dl, dc)
    def peut_poser_bombe(self, grille):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dl, dc in directions:
            nl = self.ligne + dl
            nc = self.colonne + dc

            if not grille.in_bounds(nl, nc):
                continue

            cellule = grille.get_cellule(nl, nc)

            if cellule.etat == DESTRUCTIBLE:
                return True

        return False

    def possible_drop_bombe(self, grille, bombes):
        bombes_test = bombes.copy()
        bombes_test[(self.ligne, self.colonne)] = {"pose_time": 0, "armed": True}

        cases_fuite = self.fuite(grille, self.ligne, self.colonne, bombes_test)

        return len(cases_fuite) > 0

    def update(self, grille, bombes, joueur):
        # Fusionner toutes les bombes (joueur + bot)
        toutes_bombes = {**bombes, **self.bombes}

        if self.danger(grille, toutes_bombes, self.ligne, self.colonne):
            self.move(grille, toutes_bombes)

        elif self.bot_attaque(grille, joueur):
            self.deposer_bombe(grille)

        else:
            ligne_avant = self.ligne
            colonne_avant = self.colonne

            self.approche_joueur_avec_bombes(grille, joueur, toutes_bombes)

            if self.ligne == ligne_avant and self.colonne == colonne_avant:
                if self.casser_mur(grille, joueur) and self.possible_drop_bombe(grille, toutes_bombes):
                    self.deposer_bombe(grille)

    def dessiner(self, screen, assets):
        x = self.colonne * TAILLE_CELLULE
        y = self.ligne * TAILLE_CELLULE
        screen.blit(assets["bot"], (x, y))

    def bot_attaque(self,grille,joueur):
        l_joueur= joueur.ligne
        c_joueur= joueur.colonne
        if l_joueur == self.ligne:
            distance = abs(c_joueur - self.colonne)

            if distance <= PORTEE_EXPLOSION:
                obstacle = False

                for c in range(min(c_joueur, self.colonne) + 1, max(c_joueur, self.colonne)):
                    cellule = grille.get_cellule(self.ligne, c)
                    if cellule.etat in (MUR, DESTRUCTIBLE):
                        obstacle = True
                        break

                if not obstacle:
                    return True

        if c_joueur == self.colonne:
            distance = abs(l_joueur - self.ligne)

            if distance <= PORTEE_EXPLOSION:
                obstacle = False

                for c in range(min(l_joueur, self.ligne) + 1, max(l_joueur, self.ligne)):
                    cellule = grille.get_cellule(c,self.colonne)
                    if cellule.etat in (MUR, DESTRUCTIBLE):
                        obstacle = True
                        break

                if not obstacle:
                    return True

        return False

    def approche_joueur(self, grille, joueur):
        # Déjà adjacent ?
        if abs(self.ligne - joueur.ligne) + abs(self.colonne - joueur.colonne) == 1:
            return

        depart = (self.ligne, self.colonne)
        visited = {depart}
        queue = deque()

        voisines = self.voisines_accessibles(grille, self.ligne, self.colonne)

        # Initialiser la queue avec les voisines immédiates
        for nl, nc in voisines:
            visited.add((nl, nc))
            queue.append(((nl, nc), (nl, nc)))

        # BFS
        while queue:
            (cl, cc), premier_pas = queue.popleft()

            # Case adjacente au joueur trouvée ?
            if abs(cl - joueur.ligne) + abs(cc - joueur.colonne) == 1:
                dl = premier_pas[0] - self.ligne
                dc = premier_pas[1] - self.colonne
                self.movement(grille, dl, dc)
                return

            # Explorer les voisines
            for nl, nc in self.voisines_accessibles(grille, cl, cc):
                if (nl, nc) not in visited:
                    visited.add((nl, nc))
                    queue.append(((nl, nc), premier_pas))

        # Aucun chemin trouvé
        return None
    def casser_mur (self, grille, joueur):

        dc = 0 if joueur.colonne == self.colonne else (1 if joueur.colonne > self.colonne else -1 )
        dl = 0 if joueur.ligne == self.ligne else (1 if joueur.ligne > self.ligne else -1)

        if dl != 0 and dc != 0:
            if abs(joueur.colonne - self.colonne) > abs(joueur.ligne - self.ligne):
                dl = 0
            else:
                dc = 0


        nl = self.ligne + dl
        nc = self.colonne + dc

        if not grille.in_bounds(nl, nc):
            return False

        cellule = grille.get_cellule(nl,nc)
        if cellule.etat == DESTRUCTIBLE  :
            return True
        return False

    def voisines_toutes(self, grille, ligne, colonne):
        """
        Retourne TOUTES les voisines (incluant les murs destructibles)
        sauf les murs indestructibles et les bombes
        """
        voisines = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite

        for dl, dc in directions:
            nl = ligne + dl
            nc = colonne + dc

            # Vérifier les limites de la grille
            if not grille.in_bounds(nl, nc):
                continue

            cellule = grille.get_cellule(nl, nc)

            # Accepter :
            # - Cases vides (VIDE = 1)
            # - Murs destructibles (DESTRUCTIBLE = 3)
            # Refuser :
            # - Murs indestructibles (MUR = 2)
            # - Bombes (BOMBE = 4)
            # - Explosions (EXPLOSION = 5)

            if cellule.etat in (VIDE, DESTRUCTIBLE):
                voisines.append((nl, nc))

        return voisines

    def approche_joueur_avec_bombes(self, grille, joueur, bombes):
        """
        BFS qui considère les murs destructibles comme accessibles
        et pose une bombe si un mur bloque le chemin
        """
        # Déjà adjacent ?
        if abs(self.ligne - joueur.ligne) + abs(self.colonne - joueur.colonne) == 1:
            return

        depart = (self.ligne, self.colonne)
        visited = {depart}
        queue = deque()

        # Initialiser avec toutes les voisines (même murs destructibles)
        voisines = self.voisines_toutes(grille, self.ligne, self.colonne)

        for nl, nc in voisines:
            visited.add((nl, nc))
            queue.append(((nl, nc), (nl, nc)))

        # BFS
        while queue:
            (cl, cc), premier_pas = queue.popleft()

            # Case adjacente au joueur trouvée ?
            if abs(cl - joueur.ligne) + abs(cc - joueur.colonne) == 1:
                # Vérifier si le premier pas est un mur destructible
                cellule_premier_pas = grille.get_cellule(premier_pas[0], premier_pas[1])

                if cellule_premier_pas.etat == DESTRUCTIBLE:
                    if self.possible_drop_bombe(grille, bombes):
                        self.deposer_bombe(grille)
                        # Fusionner les bombes du bot avec les existantes et fuir immédiatement
                        toutes_bombes_apres = {**bombes, **self.bombes}
                        if self.danger(grille, toutes_bombes_apres, self.ligne, self.colonne):
                            self.move(grille, toutes_bombes_apres)
                    return

                # Sinon, se déplacer normalement vers cette case
                dl = premier_pas[0] - self.ligne
                dc = premier_pas[1] - self.colonne
                self.movement(grille, dl, dc)
                return

            # Explorer les voisines (toutes, y compris murs destructibles)
            for nl, nc in self.voisines_toutes(grille, cl, cc):
                if (nl, nc) not in visited:
                    visited.add((nl, nc))
                    queue.append(((nl, nc), premier_pas))

        # Aucun chemin trouvé même avec murs destructibles
        return None