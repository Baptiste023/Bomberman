def danger(self, grille, bombes):
    l_bot = self.ligne
    c_bot = self.colonne

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