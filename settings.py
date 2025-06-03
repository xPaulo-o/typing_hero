
import pygame
import os
from PIL import Image

#cores
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
RED = (255, 0, 0)
RED_LIGHT = (220, 70, 70)
RED_DARK = (150, 50, 50)
BACKGROUND_DARK = (30, 30, 30)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE_LIGHT = (173, 216, 230)
GREEN_LIGHT = (144, 238, 144)

import pygame

pygame.init()

# Detecta a resolução atual da tela
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Define se o jogo deve rodar em tela cheia
FULLSCREEN_MODE = True


WORD_SPAWN_INTERVAL_MS = 2000  # Exemplo: uma nova palavra a cada 2 segundos
WORD_INITIAL_Y_OFFSET = 50  # Ajuste este valor conforme a necessidade


def load_gif_frames(path, size):
    pil_img = Image.open(path)
    frames = []

    try:
        while True:
            frame = pil_img.convert("RGBA")
            pygame_img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            pygame_img = pygame.transform.scale(pygame_img, size)
            frames.append(pygame_img)
            pil_img.seek(pil_img.tell() + 1)
    except EOFError:
        pass  # acabou os frames

    return frames


def draw_text_with_outline(text, font, text_color, outline_color, bg_color, pos, screen):
    # Renderiza o texto principal
    base = font.render(text, True, text_color, bg_color)

    # Cria a borda em 8 direções
    outline = pygame.Surface((base.get_width() + 2, base.get_height() + 2), pygame.SRCALPHA)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                offset = font.render(text, True, outline_color)
                outline.blit(offset, (1 + dx, 1 + dy))

    # Coloca o texto principal por cima da borda
    outline.blit(base, (1, 1))

    # Preenche o fundo (Light Gray)
    bg_surface = pygame.Surface((outline.get_width(), outline.get_height()))
    bg_surface.fill((50, 50, 50))  
    bg_surface.blit(outline, (0, 0))

    # Exibe na tela
    screen.blit(bg_surface, pos)



PAUSE_MENU_BUTTON_WIDTH = 240
PAUSE_MENU_BUTTON_HEIGHT = 60
PAUSE_MENU_BUTTON_GAP = 30
PAUSE_OVERLAY_ALPHA = 180


# Pontuação e Barra de Energia
BASE_SCORE_PER_WORD = 1               # Pontuação padrão por palavra
SPECIAL_WORD_BONUS_SCORE = 10         # Pontos por palavra especial
COMBO_MAX_MULTIPLIER_BASE = 4         # Combo normal máximo: x4
BONUS_MODE_COMBO_ADDITION = 10        # Combo x10 extra ao acertar palavra especial
ENERGY_GAIN_ON_CORRECT = 10           # Energia ganha ao acertar uma palavra
ENERGY_LOSS_ON_INCORRECT = 15         # Energia perdida ao errar
ENERGY_LOSS_ON_MISS = 5               # Energia perdida ao deixar palavra cair
INITIAL_ENERGY = 50                   # Energia inicial
MAX_ENERGY = 100                      # Energia máxima
MIN_ENERGY_FOR_GAME_OVER = 0          # Quando chegar a esse valor, game over

# Palavras especiais
SPECIAL_WORD_CHANCE = 0.1             # 10% de chance da palavra ser especial

# Cores das palavras especiais
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)                # Cor do texto de combo

# UI
PLAYER_INPUT_X_RATIO = 0.02
PLAYER_INPUT_Y_RATIO = 0.93
SCORE_DISPLAY_X_RATIO = 0.02
SCORE_DISPLAY_Y_RATIO = 0.03
ENERGY_BAR_WIDTH_RATIO = 0.3
ENERGY_BAR_HEIGHT_RATIO = 0.035
ENERGY_BAR_RIGHT_MARGIN_RATIO = 0.02
ENERGY_BAR_Y_RATIO = 0.03
BONUS_TEXT_Y_OFFSET_FROM_BAR = 10


SCREEN_WIDTH = 1920 
SCREEN_HEIGHT = 1080

# Cminhos de recursos
IMG_PAUSE = pygame.image.load("img/pause_menu.png")
IMG_PAUSE = pygame.transform.scale(IMG_PAUSE, (WIDTH, HEIGHT))
GAME_OVER = pygame.image.load("img/game_over.png")
GAME_OVER = pygame.transform.scale(GAME_OVER, (WIDTH, HEIGHT))
IMG_MENU_BG = "img/img0.png"
FASE_MENU_BG = pygame.image.load("img/menu.png")
FASE_MENU_BG = pygame.transform.scale(FASE_MENU_BG, (WIDTH, HEIGHT))
MUSIC_MENU_PATH = "sounds/menu_music.mp3"
BUTTON_CLICK_SOUND_PATH = os.path.join("sounds", "click.ogg")
ANIMATED_BG_FRAMES = load_gif_frames("videos/fundo_gameplay.gif", (WIDTH, HEIGHT))
ANIMATED_BG_FRAME_COUNT = len(ANIMATED_BG_FRAMES)
