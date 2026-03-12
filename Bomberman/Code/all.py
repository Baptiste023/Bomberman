import pygame

# Variables modifiables
l = 800
L = 800
row = 20
col = 20
FPS = 60

taille_cellule = l // row

# Etats cellule
vide = 1
mur = 2
destructible = 3
bombe = 4
explosion = 5

# Couleurs
c_vide = (10, 138, 24)
c_mur = (0, 0, 0)
c_destructible = (134, 138, 132)
c_bombe = (0, 0, 0)
c_explosion = (247, 40, 40)
c_joueur = (0, 0, 255)

# Durées
BOMBE_DELAY_MS = 3000
EXPLOSION_DURATION_MS = 500
PORTEE_EXPLOSION = 2  # ajuste ici


class Cellule:
    def __init__(self, ligne, collone, taille_cellule):
        self.ligne = ligne
        self.collone = collone
        self.taille_cellule = taille_cellule
        self.etat = vide

        self.x = collone * taille_cellule
        self.y = ligne * taille_cellule

        # explosion gérée par horodatage (pas de timer global)
        self.explosion_end_time = 0

    def set_etat(self, etat):
        self.etat = etat

    def dessiner_cellule(self, screen):
        rect = pygame.Rect(self.x, self.y, self.taille_cellule, self.taille_cellule)

        if self.etat == vide:
            pygame.draw.rect(screen, c_vide, rect)
        elif self.etat == mur:
            pygame.draw.rect(screen, c_mur, rect)
        elif self.etat == destructible:
            pygame.draw.rect(screen, c_destructible, rect)
        elif self.etat == explosion:
            pygame.draw.rect(screen, c_explosion, rect)
        elif self.etat == bombe:
            pygame.draw.rect(screen, c_vide, rect)
            pygame.draw.circle(
                screen,
                c_bombe,
                (self.x + self.taille_cellule // 2, self.y + self.taille_cellule // 2),
                self.taille_cellule // 3
            )
        else:
            pygame.draw.rect(screen, c_vide, rect)

        pygame.draw.rect(screen, (200, 200, 200), rect, 1)


class Grille:
    def __init__(self, ligne, collone, taille_cellule):
        self.ligne = ligne
        self.collone = collone
        self.taille_cellule = taille_cellule
        self.cellule = []

        for i in range(ligne):
            ligne_cellule = []
            for j in range(collone):
                c = Cellule(i, j, taille_cellule)

                # Coins départ joueurs à laisser vides
                if (i == 1 and j in [1, 2]) or (i == 2 and j == 1):
                    c.set_etat(vide)
                elif (i == ligne - 2 and j in [collone - 2, collone - 3]) or (i == ligne - 3 and j == collone - 2):
                    c.set_etat(vide)
                # Bordures
                elif i == 0 or i == ligne - 1 or j == 0 or j == collone - 1:
                    c.set_etat(mur)
                # Piliers intérieurs
                elif i % 2 == 0 and j % 2 == 0:
                    c.set_etat(mur)
                # Le reste = destructible
                else:
                    c.set_etat(destructible)

                ligne_cellule.append(c)
            self.cellule.append(ligne_cellule)

    def dessiner_grille(self, screen):
        for ligne in self.cellule:
            for c in ligne:
                c.dessiner_cellule(screen)

    def get_cellule(self, ligne, collone):
        return self.cellule[ligne][collone]

    def in_bounds(self, ligne, collone):
        return 0 <= ligne < self.ligne and 0 <= collone < self.collone

    def update_explosions(self, now_ms):
        for ligne in self.cellule:
            for c in ligne:
                if c.etat == explosion and now_ms >= c.explosion_end_time:
                    c.set_etat(vide)
                    c.explosion_end_time = 0


class Joueur:
    def __init__(self, ligne, collone, taille_cellule):
        self.ligne = ligne
        self.collone = collone
        self.taille_cellule = taille_cellule
        self.couleur = c_joueur

        # Bombes
        self.temps_derniere_bombe = 0
        self.temps_min_entre_2_bombe = 600
        # bombes: dict {(l,c): {"pose_time":..., "armed":bool}}
        # armed=False = la case reste traversable tant que joueur n'est pas sorti
        self.bombes = {}

        # Cooldown déplacement
        self.temps_dernier_deplacement = 0
        self.temps_min_entre_2_deplacement = 150  # ms

    def dessiner_joueur(self, screen):
        x = self.collone * self.taille_cellule
        y = self.ligne * self.taille_cellule
        centre = (x + self.taille_cellule // 2, y + self.taille_cellule // 2)
        rayon = self.taille_cellule // 3
        pygame.draw.circle(screen, self.couleur, centre, rayon)

    def can_walk_on(self, cell: Cellule):
        return cell.etat == vide  # garde simple; explosion = mort plus tard

    def movement_joueur(self, grille, d_ligne, d_collone):
        temps_deplacement = pygame.time.get_ticks()

        # cooldown
        if temps_deplacement - self.temps_dernier_deplacement < self.temps_min_entre_2_deplacement:
            return

        nl = self.ligne + d_ligne
        nc = self.collone + d_collone

        if not grille.in_bounds(nl, nc):
            return

        cellule_cible = grille.get_cellule(nl, nc)

        if self.can_walk_on(cellule_cible):
            # si on quitte une bombe non armée, on l'arme (la case devient bombe)
            pos_actuelle = (self.ligne, self.collone)
            if pos_actuelle in self.bombes and self.bombes[pos_actuelle]["armed"] is False:
                self.bombes[pos_actuelle]["armed"] = True
                grille.get_cellule(*pos_actuelle).set_etat(bombe)

            self.ligne = nl
            self.collone = nc

            # IMPORTANT : mise à jour du dernier déplacement
            self.temps_dernier_deplacement = temps_deplacement

    def deposer_bombe(self, grille):
        now = pygame.time.get_ticks()

        if now - self.temps_derniere_bombe < self.temps_min_entre_2_bombe:
            return

        pos = (self.ligne, self.collone)
        if pos in self.bombes:
            return

        # Pose sous le joueur, non armée tant qu'il n'est pas sorti
        self.bombes[pos] = {"pose_time": now, "armed": False}
        self.temps_derniere_bombe = now

    def trigger_explosion(self, grille, centre_l, centre_c, now):
        def explode_cell(l, c):
            cell = grille.get_cellule(l, c)
            # si déjà explosion, on n'écrase pas le timer (optionnel)
            cell.set_etat(explosion)
            cell.explosion_end_time = max(cell.explosion_end_time, now + EXPLOSION_DURATION_MS)

        # Centre
        explode_cell(centre_l, centre_c)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dl, dc in directions:
            for step in range(1, PORTEE_EXPLOSION + 1):
                nl = centre_l + dl * step
                nc = centre_c + dc * step

                if not grille.in_bounds(nl, nc):
                    break

                cell = grille.get_cellule(nl, nc)

                # Mur : bloque tout
                if cell.etat == mur:
                    break

                # Destructible : on détruit + explosion visible + stop la propagation
                if cell.etat == destructible:
                    explode_cell(nl, nc)


                # Bombe : explosion visible + stop (chain reaction plus tard)
                if cell.etat == bombe:
                    explode_cell(nl, nc)
                    break

                # Vide (ou explosion déjà) : explosion continue
                explode_cell(nl, nc)
    def gestion_bombes(self, grille):
        now = pygame.time.get_ticks()
        to_remove = []

        for (bl, bc), info in self.bombes.items():
            if now - info["pose_time"] >= BOMBE_DELAY_MS:
                self.trigger_explosion(grille, bl, bc, now)
                to_remove.append((bl, bc))

        for pos in to_remove:
            self.bombes.pop(pos, None)


def main():
    pygame.init()
    screen = pygame.display.set_mode((l, L))
    pygame.display.set_caption("Boomberman")
    clock = pygame.time.Clock()

    ma_grille = Grille(row, col, taille_cellule)
    joueur = Joueur(1, 1, taille_cellule)

    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    joueur.deposer_bombe(ma_grille)

        keys = pygame.key.get_pressed()

        # une direction à la fois (sinon diagonales bizarres)
        if keys[pygame.K_z]:
            joueur.movement_joueur(ma_grille, -1, 0)
        elif keys[pygame.K_s]:
            joueur.movement_joueur(ma_grille, 1, 0)
        elif keys[pygame.K_q]:
            joueur.movement_joueur(ma_grille, 0, -1)
        elif keys[pygame.K_d]:
            joueur.movement_joueur(ma_grille, 0, 1)

        joueur.gestion_bombes(ma_grille)
        ma_grille.update_explosions(now)

        screen.fill((0, 0, 0))
        ma_grille.dessiner_grille(screen)
        joueur.dessiner_joueur(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()