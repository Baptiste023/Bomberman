# 💣 Bomberman

Un jeu Bomberman classique en Python avec Pygame, mettant en avant un joueur humain face à un adversaire IA intelligent.

## 🎮 Fonctionnalités

- **Joueur contrôlable au clavier** avec système de placement de bombes
- **Bot** capable de :
  - Détecter et fuir les danger (explosions)
  - Planifier des chemins vers le joueur
  - Casser les murs destructibles stratégiquement
  - Attaquer le joueur en ligne droite
  - Gérer ses propres bombes de façon intelligente
- **Système de bombes** avec explosions en croix avec portée configurable
- **Grille de jeu générative** avec murs indestructibles, destructibles et zones vides
- **Limitation à 1 bombe active** par joueur/bot (contrainte classique Bomberman)
- **Détection de mort** et écrans de victoire/défaite
- **Gestion robuste des assets** avec chemins absolus

## 🎮 Contrôles

| Touche | Action |
|--------|--------|
| **Z** | Aller vers le haut |
| **S** | Aller vers le bas |
| **Q** | Aller vers la gauche |
| **D** | Aller vers la droite |
| **ESPACE** | Poser une bombe |
| **Clic souris** | Recommencer après une partie |

## 📋 Prérequis

- Python 3.7+
- Pygame 2.0+

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd Bomberman
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv .venv
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. Installer les dépendances
```bash
pip install pygame
```

### 4. Lancer le jeu
```bash
cd Code
python main.py
```

## 📁 Structure du projet

```
Bomberman/
├── Code/
│   ├── main.py                 # Point d'entrée du jeu
│   ├── settings.py             # Configuration (résolution, constantes)
│   ├── grille.py               # Gestion de la grille de jeu
│   ├── joueur.py               # Classe du joueur et logique commune
│   ├── bot.py                  # Bot
│   ├── bot_v_fin.py            # Version alternative du bot
│   ├── bot_final_complet.py    # Version complète du bot avec handicap
│   ├── cellule.py              # Classe représentant une cellule
│   └── __pycache__/
├── assets/                     # Images et ressources du jeu
│   ├── MUR.png
│   ├── Destructible.png
│   ├── Herbe.png
│   ├── bombe.png
│   ├── perso.png
│   ├── Bot.png
│   ├── explosion_centrale.png
│   ├── explosion_horizontale.png
│   ├── explosion_verticale.png
│   ├── explosion_bout_h.png
│   ├── explosion_bout_b.png
│   ├── explosion_bout_d.png
│   └── explosion_bout_g.png
└── README.md
```

## 🎯 Mécanique du jeu

### Le joueur
- Commence au coin supérieur gauche (1, 1)
- Peut se déplacer librement sur les cases vides
- Peut poser une seule bombe à la fois
- Meurt s'il est touché par une explosion

### Le Bot 
- Commence au coin inférieur droit (19, 19)
- Utilise des algorithmes BFS pour la navigation
- Stratégies prioritaires :
  1. **Fuir le danger** - S'échapper immédiatement si en danger
  2. **Attaquer** - Poser une bombe si le joueur est en ligne droite
  3. **Approcher** - Marcher vers le joueur et casser les murs si nécessaire
- Évalue toujours s'il a une route de fuite avant de poser une bombe

### Les bombes
- Délai d'explosion : **2 secondes**
- Portée d'explosion : **2 cases** en croix
- Seulement **1 bombe active** par entité
- Les murs destructibles bloquent l'explosion
- Les murs indestructibles arrêtent complètement l'explosion

### La victoire
- **Joueur gagne** : Éliminer le bot
- **Bot gagne** : Éliminer le joueur

## 🔧 Fichiers principaux

### `main.py`
Point d'entrée du jeu. Gère :
- Initialisation Pygame
- Boucle principale du jeu
- Chargement des assets
- Gestion des événements (mouvements, bombes)
- Écrans de victoire/défaite

### `settings.py`
Constantes configurables :
- Résolution : `800x800`
- Grille : `21x21`
- FPS : `60`
- Délais et cooldowns des mouvements/bombes

### `bot.py`
Bot avec :
- Détection des dangers (`danger()`)
- Recherche de chemins BFS (`fuite()`, `approche_joueur()`)
- Attaque directe (`bot_attaque()`)
- Destruction de murs (`casser_mur()`)

### `joueur.py`
Classe de base pour le joueur et le bot :
- Gestion du mouvement
- Placement des bombes
- Système d'explosion
- Détection de mort



## 💡 Améliorations possibles

- [ ] Menu principal avec options de difficulté
- [ ] Powerups (portée augmentée, vitesse, bombes supplémentaires)
- [ ] Mode local multijoueur
- [ ] Personnages et skins personnalisables
- [ ] Effets sonores et musique


## 👨‍💻 Auteur

Développé avec Python 3 et Pygame 2.

---

**Bon jeu! 🎮**
