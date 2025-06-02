import pygame
import random
import sys
import os
import unicodedata
from settings import * # Garanta que settings.py tenha as cores e outras constantes
from fases import fases # Importa o dicionário de fases
from gamedata import load_game_data, save_game_data # Importa as funções de save/load
from moviepy import VideoFileClip
import pygame


pygame.init()
pygame.mixer.init()


DISPLAY_INFO = pygame.display.Info()
WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Hero")
clock = pygame.time.Clock()

font_size = WIDTH // 53
title_size = WIDTH // 30
font = pygame.font.SysFont("Arial", font_size)
title_font = pygame.font.SysFont("Arial", title_size)

# Tamanhos dinâmicos com base na resolução da tela
logo_width = int(WIDTH * 0.5)
logo_height = int(logo_width * 0.625)

# Carrega e redimensiona as imagens definidas no settings.py
IMG_MENU_BG = pygame.transform.scale(pygame.image.load(IMG_MENU_BG), (WIDTH, HEIGHT))

# --- VARIÁVEIS GLOBAIS PARA DADOS DO JOGO ---
game_data = load_game_data()
max_scores = game_data.get("max_scores", {})
unlocked_fases = game_data.get("unlocked_fases", [1]) # Começa com a fase 1 desbloqueada
fase_atual = 1 # Inicia na fase 1
# --- FIM VARIÁVEIS GLOBAIS ---



def new_word(word_pool, min_speed, max_speed): # Adicionado min_speed e max_speed
    word = random.choice(word_pool)
    is_special = random.random() < SPECIAL_WORD_CHANCE
    return {
        "word": word,
        "x": random.randint(WIDTH // 20, WIDTH - WIDTH // 4),
        "y": WORD_INITIAL_Y_OFFSET,
        "speed": random.randint(min_speed, max_speed), # Usa as velocidades da fase
        "special": is_special,
        "color": CYAN if is_special else WHITE
    }

def draw_game_over(final_score): # Renomeado e recebe final_score
    screen.blit(GAME_OVER, (0, 0))
    
    text = f"Pontuação Final: {final_score}"
    font = pygame.font.SysFont(None, 48)
    pos = (WIDTH // 2, HEIGHT // 2)

    # Posição
    x = 500
    y = 200
    draw_text_with_outline(
        text,
        font,
        text_color=(255, 255, 255),     # Branco
        outline_color=(0, 0, 0),        # Preto
        bg_color=(50, 50, 50),       
        pos=(x, y),
        screen=screen
    )


    # Botões
    retry_rect = pygame.Rect(500, 350, 300, 60)
    menu_rect = pygame.Rect(500, 450, 300, 60)

    while True:

        mouse_pos = pygame.mouse.get_pos()

        # Lista de botões: (retângulo, texto)
        botoes = [
            (retry_rect, "Reiniciar Fase"),
            (menu_rect, "Menu Principal")
        ]

        for rect, label in botoes:
            cor = LIGHT_GRAY if rect.collidepoint(mouse_pos) else DARK_GRAY
            pygame.draw.rect(screen, cor, rect, border_radius=20)

            texto = font.render(label, True, WHITE)
            screen.blit(
                texto,
                (
                    rect.centerx - texto.get_width() // 2,
                    rect.centery - texto.get_height() // 2
                )
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    if retry_rect.collidepoint(event.pos):
                        return "game"
                    elif menu_rect.collidepoint(event.pos):
                        return "menu"

def pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(PAUSE_OVERLAY_ALPHA)
    overlay.fill(BLACK)

    button_w = PAUSE_MENU_BUTTON_WIDTH
    button_h = PAUSE_MENU_BUTTON_HEIGHT

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    resume_rect = pygame.Rect(center_x - button_w // 2, center_y - button_h - PAUSE_MENU_BUTTON_GAP, button_w, button_h)
    retry_rect = pygame.Rect(center_x - button_w // 2, center_y, button_w, button_h)
    menu_rect = pygame.Rect(center_x - button_w // 2, center_y + button_h + PAUSE_MENU_BUTTON_GAP, button_w, button_h)

    while True:
        screen.blit(IMG_PAUSE , (0, 0))

        title = title_font.render("Jogo Pausado", True, WHITE)
        screen.blit(title, (center_x - title.get_width() // 2, HEIGHT // 4))

        mouse_pos = pygame.mouse.get_pos()

        # Botões com hover
        botoes = [
            (resume_rect, "Continuar"),
            (retry_rect, "Reiniciar Fase"),
            (menu_rect, "Menu Principal")
        ]

        for rect, label in botoes:
            cor = LIGHT_GRAY if rect.collidepoint(mouse_pos) else DARK_GRAY
            pygame.draw.rect(screen, cor, rect, border_radius=20)
            texto = font.render(label, True, WHITE)
            screen.blit(texto, (rect.centerx - texto.get_width() // 2, rect.centery - texto.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_rect.collidepoint(event.pos):
                    return  # Continua
                elif retry_rect.collidepoint(event.pos):
                    main_game()  # Reinicia
                    return
                elif menu_rect.collidepoint(event.pos):
                    return draw_main_menu() # Volta ao menu


def main_game():
    global fase_atual, max_scores, unlocked_fases

    falling_words = []
    input_text = ""
    score = 0
    bar_value = INITIAL_ENERGY
    bonus_mode = False
    combo = 0

    # Pega as configurações da fase atual do dicionário 'fases'
    # Usa fase_atual para acessar corretamente (fases são de 1 a 13)
    # Certifique-se de que fase_atual é um valor válido para a chave no dicionário fases
    if fase_atual not in fases:
        print(f"Erro: Fase {fase_atual} não encontrada no dicionário de fases. Voltando para a Fase 1.")
        fase_atual = 1
        current_fase_data = fases[fase_atual]
    else:
        current_fase_data = fases[fase_atual]

    word_list = current_fase_data["palavras"]
    current_min_speed = current_fase_data["min_speed"]
    current_max_speed = current_fase_data["max_speed"]

    NEW_WORD_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(NEW_WORD_EVENT, WORD_SPAWN_INTERVAL_MS)

    running = True
    while running:
        screen.fill(BLACK) # Limpa a tela a cada frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Se pause_menu retorna "menu", significa que o usuário quer ir para o menu principal
                    if pause_menu() == "menu":
                        return "menu" # Retorna "menu" para a função run_game
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    matched = False
                    for word in falling_words:
                        if input_text.lower() == word["word"]:
                            special_bonus = BONUS_MODE_COMBO_ADDITION if word.get("special") else 0
                            base_multiplier = min(combo + 1, COMBO_MAX_MULTIPLIER_BASE)
                            total_multiplier = base_multiplier + special_bonus

                            points = (SPECIAL_WORD_BONUS_SCORE if word.get("special") else BASE_SCORE_PER_WORD)
                            score += points * total_multiplier

                            bar_value = min(bar_value + ENERGY_GAIN_ON_CORRECT, MAX_ENERGY)
                            falling_words.remove(word)
                            combo += 1
                            matched = True
                            break
                    if not matched:
                        bar_value = max(bar_value - ENERGY_LOSS_ON_INCORRECT, MIN_ENERGY_FOR_GAME_OVER)
                        combo = 0
                    input_text = ""
                else:
                    if event.unicode:
                        if unicodedata.combining(event.unicode):
                            continue
                        if event.unicode == "~": # Evita o caracter til solto
                            continue
                        input_text += event.unicode
            elif event.type == NEW_WORD_EVENT:
                falling_words.append(new_word(word_list, current_min_speed, current_max_speed)) # Passa as velocidades

        # Atualiza posição e checa palavras que caíram
        for word in list(falling_words):
            word["y"] += word["speed"]
            if word["y"] > HEIGHT:
                falling_words.remove(word)
                bar_value = max(bar_value - ENERGY_LOSS_ON_MISS, MIN_ENERGY_FOR_GAME_OVER)
                combo = 0
                input_text = ""

        bonus_mode = bar_value >= MAX_ENERGY

        # Renderizar palavras
        for word in falling_words:
            surface = font.render(word["word"], True, word.get("color", WHITE))
            screen.blit(surface, (word["x"], word["y"]))

        # Mostrar entrada do jogador
        input_surface = font.render(f"> {input_text}", True, WHITE)
        screen.blit(input_surface, (WIDTH * PLAYER_INPUT_X_RATIO, HEIGHT * PLAYER_INPUT_Y_RATIO))

        # Mostrar pontuação
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (WIDTH * SCORE_DISPLAY_X_RATIO, HEIGHT * SCORE_DISPLAY_Y_RATIO))

        # Barra de energia
        bar_w = int(WIDTH * ENERGY_BAR_WIDTH_RATIO)
        bar_h = int(HEIGHT * ENERGY_BAR_HEIGHT_RATIO)
        bar_x = WIDTH - bar_w - int(WIDTH * ENERGY_BAR_RIGHT_MARGIN_RATIO)
        bar_y = int(HEIGHT * ENERGY_BAR_Y_RATIO)
        fill = int((bar_value / MAX_ENERGY) * bar_w)
        bar_color = GOLD if bonus_mode else GREEN
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill, bar_h))

        # Combo
        if combo >= 1:
            combo_text = font.render(f"Combo x{min(combo + 1, COMBO_MAX_MULTIPLIER_BASE)}", True, YELLOW)
            screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, bar_y + bar_h + 10))

        # Modo bônus
        if bonus_mode:
            bonus_text = font.render("Modo Bônus!", True, bar_color)
            screen.blit(bonus_text, (bar_x + bar_w // 2 - bonus_text.get_width() // 2, bar_y + bar_h + BONUS_TEXT_Y_OFFSET_FROM_BAR))

        if bar_value <= MIN_ENERGY_FOR_GAME_OVER:

            # Sempre atualiza o score máximo se o score atual for maior
            if score > max_scores.get(str(fase_atual), 0):
                max_scores[str(fase_atual)] = score
                game_data["max_scores"] = max_scores
                save_game_data(game_data)

            # Lógica para desbloquear a próxima fase se o score for maior que 0
            # e a próxima fase existir e não estiver desbloqueada
            if score > 0 and (fase_atual + 1) in fases and (fase_atual + 1) not in unlocked_fases:
                unlocked_fases.append(fase_atual + 1)
                unlocked_fases.sort() # Mantém a lista ordenada
                game_data["unlocked_fases"] = unlocked_fases
                save_game_data(game_data)
         

            return draw_game_over(score) # Chama a tela de Game Over e retorna o estado
        
        pygame.display.flip()
        clock.tick(60)

    return "menu" # Por garantia, se o loop 'running' terminar inesperadamente

def draw_main_menu():
    screen.blit(IMG_MENU_BG, (0, 0))

    # Define o tamanho dos botões com base na resolução da tela
    button_width = int(WIDTH * 0.25)
    button_height = int(HEIGHT * 0.08)

    # Posicionamento dos botões baseado na imagem que você enviou
    play_button_x = WIDTH // 1.2 - button_width // 1
    play_button_y = int(HEIGHT * 0.60)  # Botão JOGAR 

    exit_button_x = WIDTH // 1.2 - button_width // 1
    exit_button_y = int(HEIGHT * 0.73)  # Botão SAIR 

    # Define os retângulos dos botões
    play_button_rect = pygame.Rect(play_button_x, play_button_y, button_width, button_height)
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()

    # Botão JOGAR
    play_color = LIGHT_GRAY if play_button_rect.collidepoint(mouse_pos) else DARK_GRAY
    pygame.draw.rect(screen, play_color, play_button_rect, border_radius=20)
    play_text = font.render("JOGAR", True, WHITE)
    screen.blit(play_text, (play_button_rect.centerx - play_text.get_width() // 2,
                            play_button_rect.centery - play_text.get_height() // 2))

    # Botão SAIR
    exit_color = RED_LIGHT if exit_button_rect.collidepoint(mouse_pos) else RED_DARK
    pygame.draw.rect(screen, exit_color, exit_button_rect, border_radius=20)
    exit_text = font.render("SAIR", True, WHITE)
    screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                            exit_button_rect.centery - exit_text.get_height() // 2))

    pygame.display.flip()

    # Evento de clique
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                return "levels"  # Vai para o menu de seleção de fases
            if exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    return "menu" # Permanece no menu se nenhuma opção for clicada

def draw_level_selection_menu():
    global fase_atual, unlocked_fases, max_scores
    screen.blit(FASE_MENU_BG, (0, 0)) # Fundo do menu de fases

    #itle_text = title_font.render("SELECIONE A FASE", True, BLACK)
    #screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 10))

    button_width = int(WIDTH * 0.10) # Botões mais estreitos
    button_height = int(HEIGHT * 0.07) # Botões mais baixos
    
    # Posições para os botões de fase (vertical, como na imagem)
    # Calcula a posição inicial X para centralizar a coluna de botões
    start_x = WIDTH // 2.8 - button_width // 1
    start_y = HEIGHT // 140

    espacamento_y = button_height + 2.5 # Espaçamento vertical entre os botões
    

    button_width = 100   
    button_height = 40  

    # Botões de fase
    for i in range(1, len(fases) + 1): # Itera sobre todas as fases disponíveis
        button_y = start_y + (i - 1) * espacamento_y
        button_rect = pygame.Rect(start_x, button_y, button_width, button_height)

        is_unlocked = (i in unlocked_fases)
        
        mouse_pos = pygame.mouse.get_pos()
        if is_unlocked:
            button_color = LIGHT_GRAY if button_rect.collidepoint(mouse_pos) else DARK_GRAY
        else:
            button_color = GRAY
        
        text_color = WHITE if is_unlocked else DARK_GRAY

        pygame.draw.rect(screen, button_color, button_rect, border_radius=40) # Cantos levemente arredondados
        level_text = font.render(f"Fase {i}", True, text_color)
        screen.blit(level_text, (button_rect.centerx - level_text.get_width() // 2,
                                  button_rect.centery - level_text.get_height() // 2 - font_size // 4)) # Ajuste Y para deixar espaço para o score

        # Exibir Score Máximo
        # Certifique-se que a chave é uma string, pois JSON salva chaves como strings
        if str(i) in max_scores:
            score_display_text = f"PONTUAÇÂO MAXIMA: {max_scores[str(i)]}"
            score_surface = font.render(score_display_text, True, BLACK)
            screen.blit(score_surface, (
                        button_rect.right + 280, 
                        button_rect.centery - score_surface.get_height() // 2  # Centralizado verticalmente
                         ))


    # Botão Voltar (posicionado no canto inferior esquerdo como na imagem)
    back_button_width = int(WIDTH * 0.10)
    back_button_height = int(HEIGHT * 0.06)
    back_button_rect = pygame.Rect(WIDTH * 0.02, HEIGHT * 0.88, back_button_width, back_button_height) # Ajustado para o canto inferior esquerdo

    mouse_pos = pygame.mouse.get_pos()
    back_color = LIGHT_GRAY if back_button_rect.collidepoint(mouse_pos) else DARK_GRAY
    pygame.draw.rect(screen, back_color, back_button_rect, border_radius=8)
    back_text = font.render("VOLTAR", True, WHITE) # Texto como na imagem
    screen.blit(back_text, (back_button_rect.centerx - back_text.get_width() // 2,
                            back_button_rect.centery - back_text.get_height() // 2))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i in range(1, len(fases) + 1):
                button_y = start_y + (i - 1) * espacamento_y
                button_rect = pygame.Rect(start_x, button_y, button_width, button_height)

                if button_rect.collidepoint(mouse_x, mouse_y):
                    if i in unlocked_fases:
                        fase_atual = i
                        return "game" # Inicia o jogo na fase selecionada
                    else:
                        print(f"Fase {i} bloqueada!") # Mensagem de depuração
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                return "menu" # Volta para o menu principal
    return "levels" # Permanece no menu de fases



def run_game():
    current_state = "menu" # Inicia no menu principal

    while True:
        if current_state == "menu":
            current_state = draw_main_menu()
        elif current_state == "game":
            current_state = main_game()
        elif current_state == "levels":
            current_state = draw_level_selection_menu()
        else:
            # Caso algum estado inesperado seja retornado, encerra o jogo
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    run_game()
