from joueur import Joueur
from settings import PORTEE_EXPLOSION, MUR, DESTRUCTIBLE, VIDE, TAILLE_CELLULE
import random

class Bot(Joueur):

    def danger(self, grille, bombes, ligne, colonne):
        l_bot = ligne
        c_bot = colonne

        for (l_bombe, c_bombe) in bombes:

            # Même ligne
            if l_bot == l_bombe:
                distance = abs(c_bot - c_bombe)

                if distance <= PORTEE_EXPLOSION:
                    obstacle = False

                    for c in range(min(c_bombe, c_bot) + 1, max(c_bombe, c_bot)):
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

                    for l in range(min(l_bombe, l_bot) + 1, max(l_bombe, l_bot)):
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
        return cellule.etat == VIDE

    def voisines_accessibles(self, grille, ligne, colonne):
        voisines = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),()]

        for dl, dc in directions:
            nl = ligne + dl
            nc = colonne + dc

            if self.case_accessible(grille, nl, nc):
                voisines.append((nl, nc))

        return voisines

    def fuite(self, grille, ligne, colonne, bombes):
        cases_fuite = []

        for nl, nc in self.voisines_accessibles(grille, ligne, colonne):
            if not self.danger(grille, bombes, nl, nc):
                cases_fuite.append((nl, nc))

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
        print("CASES FUITES :", self.fuite(grille, self.ligne, self.colonne, bombes))

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

    def update(self, grille, bombes):
        if self.danger(grille, bombes, self.ligne, self.colonne):
            self.move(grille, bombes)

        elif self.peut_poser_bombe(grille) and self.possible_drop_bombe(grille, bombes):
            self.deposer_bombe(grille)

        print("BOT :", self.ligne, self.colonne)
        print("BOMBES :", bombes)
        print("DANGER :", self.danger(grille, bombes, self.ligne, self.colonne))

    def dessiner(self, screen, assets):
        x = self.colonne * TAILLE_CELLULE
        y = self.ligne * TAILLE_CELLULE
        screen.blit(assets["bot"], (x, y))