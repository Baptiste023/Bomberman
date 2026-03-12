import pygame

from settings import *
from grille import Grille
from joueur import Joueur
from bot import Bot

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Boomberman")
    clock = pygame.time.Clock()

    grille = Grille()
    joueur = Joueur(1, 1)
    bot = Bot(ROW-2,COL-2)
    assets =chargement_assets()

    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        bombes_visibles = {}
        bombes_visibles.update(joueur.bombes)
        bombes_visibles.update(bot.bombes)
        bot.update(grille,bombes_visibles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    joueur.deposer_bombe(grille)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            joueur.movement(grille, -1, 0)
        elif keys[pygame.K_s]:
            joueur.movement(grille, 1, 0)
        elif keys[pygame.K_q]:
            joueur.movement(grille, 0, -1)
        elif keys[pygame.K_d]:
            joueur.movement(grille, 0, 1)

        joueur.gestion_bombes(grille)
        bot.gestion_bombes(grille)
        grille.update_explosions(now)


        if joueur.Mort_joueur(grille):
            affichage_mort(screen)
            recommencer_fin()
            grille= Grille()
            joueur = Joueur(1, 1)
            bot = Bot(ROW - 2, COL - 2)


        screen.fill((0, 0, 0))
        grille.dessiner(screen,assets)
        joueur.dessiner(screen,assets)
        bot.dessiner(screen,assets)
        pygame.display.flip()

    pygame.quit()

def affichage_mort(screen):
    screen.fill((0, 0, 0))

    font = pygame.font.SysFont("Arial", 48)
    text = font.render("GAME OVER", True, (255, 0, 0))

    sub = pygame.font.SysFont("Arial", 24).render(
        "Cliquez pour recommencer", True, (255, 255, 255)
    )

    screen.blit(text, (HAUTEUR // 2 - 140, LARGEUR // 2 - 60))
    screen.blit(sub, (HAUTEUR // 2 - 150, LARGEUR // 2))

    pygame.display.flip()

def recommencer_fin():
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                   return

def chargement_assets():

    assets={}

    # Image MUR
    image_mur = pygame.image.load("../assets/MUR.png").convert_alpha()
    assets["mur"]= pygame.transform.scale(image_mur, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image MUR Destructible
    image_destructible= pygame.image.load("../assets/Destructible.png").convert_alpha()
    assets["destructible"]= pygame.transform.scale(image_destructible, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image Herbe
    image_herbe= pygame.image.load("../assets/Herbe.png").convert_alpha()
    assets["herbe"]= pygame.transform.scale(image_herbe, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image Bombe
    image_bombe= pygame.image.load("../assets/bombe.png").convert_alpha()
    assets["bombe"]=pygame.transform.scale(image_bombe, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion centre
    image_centre= pygame.image.load("../assets/explosion_centrale.png").convert_alpha()
    assets["centre"]=pygame.transform.scale(image_centre, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion horizontale
    image_horizontale = pygame.image.load("../assets/explosion_horizontale.png").convert_alpha()
    assets["horizontale"]=pygame.transform.scale(image_horizontale, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion verticale
    image_verticale= pygame.image.load("../assets/explosion_verticale.png").convert_alpha()
    assets["verticale"]=pygame.transform.scale(image_verticale, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion bout haut
    image_explosion_bout_haut= pygame.image.load("../assets/explosion_bout_h.png").convert_alpha()
    assets["bout_h"]=pygame.transform.scale(image_explosion_bout_haut, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion bout bas
    image_explosion_bout_bas= pygame.image.load("../assets/explosion_bout_b.png").convert_alpha()
    assets["bout_b"]=pygame.transform.scale(image_explosion_bout_bas, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion bout droite
    image_bout_droite= pygame.image.load("../assets/explosion_bout_d.png").convert_alpha()
    assets["bout_d"]= pygame.transform.scale(image_bout_droite, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image explosion bout gauche
    image_bout_gauche=pygame.image.load("../assets/explosion_bout_g.png").convert_alpha()
    assets["bout_g"]=pygame.transform.scale(image_bout_gauche, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image personnage
    image_personnage= pygame.image.load("../assets/perso.png").convert_alpha()
    assets["personnage"]=pygame.transform.scale(image_personnage, (TAILLE_CELLULE, TAILLE_CELLULE))

    # Image Bot
    image_bot = pygame.image.load("../assets/Bot.png").convert_alpha()
    assets["bot"]=pygame.transform.scale(image_bot, (TAILLE_CELLULE, TAILLE_CELLULE))
    return assets


if __name__ == "__main__":
    main()