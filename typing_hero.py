import pygame
import random
import sys
import os
import unicodedata
from settings import * 
from fases import fases # Importa o dicionário de fases
from gamedata import load_game_data, save_game_data # Importa as funções de save/load
import pygame


pygame.init()
pygame.mixer.init()

try:
    BUTTON_CLICK_SOUND = pygame.mixer.Sound(BUTTON_CLICK_SOUND_PATH)
except pygame.error as e:
    print(f"Erro ao carregar som de clique: {e}")
    BUTTON_CLICK_SOUND = None # Define como None se o som não puder ser carregado



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


game_data = load_game_data()
max_scores = game_data.get("max_scores", {})
unlocked_fases = game_data.get("unlocked_fases", [1]) # Começa com a fase 1 desbloqueada



try:
    pygame.mixer.music.load(MUSIC_MENU_PATH)
except pygame.error as e:
    print(f"Erro ao carregar música do menu: {e}")

def play_menu_music():
    try:
        pygame.mixer.music.load(MUSIC_MENU_PATH) # MUSIC_MENU_PATH deve ser definida no settings.py
        pygame.mixer.music.play(-1) # -1 para loop infinito
    except pygame.error as e:
        print(f"Erro ao carregar ou tocar música do menu: {e}")

    


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

def draw_game_over(final_score):
    screen.blit(GAME_OVER, (0, 0)) 
    
    text = f"Pontuação Final: {final_score}"
    font = pygame.font.SysFont(None, 48)

    # Posição
    x = 490
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
            cor = LIGHT_GRAY if rect.collidepoint(mouse_pos) else BLACK
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

        for event in pygame.event.get(): # APENAS UM LOOP DE EVENTOS
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    if retry_rect.collidepoint(event.pos):
                        play_button_click_sound()
                        return "game"
                    elif menu_rect.collidepoint(event.pos):
                        play_button_click_sound()
                        return "menu"

def stop_music():
    """Para qualquer música que esteja tocando."""
    pygame.mixer.music.stop()

def play_button_click_sound():
    """Toca o som do clique do botão, se disponível."""
    if BUTTON_CLICK_SOUND:
        BUTTON_CLICK_SOUND.play()



def pause_menu():
    # ... (código existente para desenhar o menu de pausa)

    pygame.mixer.music.pause() # Pausa a música ao entrar no menu de pausa

    while True:
        # Isso garante que a tela de pausa seja desenhada continuamente
        # enquanto o menu de pausa estiver ativo.
        screen.blit(IMG_PAUSE, (0, 0)) # Certifique-se de que a imagem de pausa está sendo desenhada

        # Desenha os botões (apenas para ter certeza que são visíveis)
        resume_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        retry_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
        menu_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

        draw_button(screen, resume_rect, "Retomar", BLACK, LIGHT_GRAY, font) 
        draw_button(screen, retry_rect, "Reiniciar Fase", BLACK, LIGHT_GRAY, font) 
        draw_button(screen, menu_rect, "Menu Principal", BLACK, LIGHT_GRAY, font) 
        
        pygame.display.flip()


        for event in pygame.event.get(): # O erro está aqui, fora deste loop
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # O bloco de código que estava fora do loop 'for' agora está aqui dentro.
                # Dessa forma, 'event' sempre terá um valor quando 'event.type' e 'event.button' forem acessados.
                if resume_rect.collidepoint(event.pos):
                    play_button_click_sound()
                    pygame.mixer.music.unpause() # Retoma a música
                    return "resume"  # Retorna para main_game continuar
                elif retry_rect.collidepoint(event.pos):
                    play_button_click_sound()
                    pygame.mixer.music.stop() # Para a música para reiniciar a fase
                    return "restart" # Retorna para run_game reiniciar a fase
                elif menu_rect.collidepoint(event.pos):
                    play_button_click_sound()
                    pygame.mixer.music.stop() # Para a música para ir ao menu principal
                    return "menu" # Retorna para run_game ir ao menu principal
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_button_click_sound()
                    pygame.mixer.music.unpause() # Retoma a música
                    return "resume"

        # Adicione um pequeno delay para evitar que o loop rode muito rápido
        pygame.time.delay(10)

def main_game():
    global fase_atual, max_scores, unlocked_fases

    falling_words = []
    input_text = ""
    score = 0
    bar_value = INITIAL_ENERGY
    bonus_mode = False
    combo = 0

    frame_index = 0
    frame_timer = 0
    FRAME_DURATION = 100  # milissegundos por frame

    stop_music() 

    # Pega as configurações da fase atual do dicionário 'fases'
    if fase_atual not in fases:
        print(f"Erro: Fase {fase_atual} não encontrada no dicionário de fases. Voltando para a Fase 1.")
        fase_atual = 1
        current_fase_data = fases[fase_atual]
    else:
        current_fase_data = fases[fase_atual]

    word_list = current_fase_data["palavras"]
    current_min_speed = current_fase_data["min_speed"]
    current_max_speed = current_fase_data["max_speed"]

    # Variável para controlar se a velocidade já foi acelerada
    accelerated_speed = False

    # Carrega e toca a música da gameplay
    try:
        pygame.mixer.music.load(MUSIC_GAMEPLAY_PATH)
        pygame.mixer.music.play(-1) # -1 para loop infinito
    except pygame.error as e:
        print(f"Erro ao carregar ou tocar música da gameplay: {e}")

    NEW_WORD_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(NEW_WORD_EVENT, WORD_SPAWN_INTERVAL_MS)

    running = True
    while running:
        # Atualiza o fundo animado do gif
        frame_timer += clock.get_time()
        if frame_timer >= FRAME_DURATION:
            frame_timer = 0
            frame_index = (frame_index + 1) % ANIMATED_BG_FRAME_COUNT

        screen.blit(ANIMATED_BG_FRAMES[frame_index], (0, 0))

        # Verifica o tempo da música para aumentar a velocidade das palavras
        # Certifique-se de que a música está tocando antes de tentar obter a posição
        if not accelerated_speed and pygame.mixer.music.get_busy() and \
           pygame.mixer.music.get_pos() >= MUSIC_ACCELERATION_TIME_MS:

            print("Acelerando a velocidade das palavras!") 
            current_min_speed *= 2  # Dobra a velocidade mínima
            current_max_speed *= 2  # Dobra a velocidade máxima
            accelerated_speed = True # Garante que só acelere uma vez


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu() # Pega a ação da tela de pausa
                    if action == "resume":
                        # Se a música estava tocando e foi pausada, retome-a
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()
                        pass # Continua o loop do jogo
                    elif action == "restart":
                        pygame.mixer.music.stop() # Para a música antes de reiniciar
                        return "restart" # Indica ao run_game para reiniciar
                    elif action == "menu":
                        pygame.mixer.music.stop() # Para a música antes de voltar ao menu
                        return "menu"
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
                # Passa as velocidades que podem ter sido ajustadas
                falling_words.append(new_word(word_list, current_min_speed, current_max_speed)) 

        # Atualiza posição e checa palavras que caíram
        for word in list(falling_words):
            word["y"] += word["speed"]
            if word["y"] > HEIGHT:
                falling_words.remove(word)
                bar_value = max(bar_value - ENERGY_LOSS_ON_MISS, MIN_ENERGY_FOR_GAME_OVER)
                combo = 0
                input_text = ""

        bonus_mode = bar_value >= MAX_ENERGY

        # Renderizar palavras (restante do seu código de renderização)
        for word in falling_words:
            text_surface = font.render(word["word"], True, word.get("color", WHITE))

            # Cálculo da posição e tamanho
            text_rect = text_surface.get_rect()
            padding = 10  # Espaço interno
            bg_rect = pygame.Rect(
                word["x"] - padding // 2,
                word["y"] - padding // 2,
                text_rect.width + padding,
                text_rect.height + padding
            )

            # Cria superfície com fundo transparente
            word_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)

            # Desenha retângulo arredondado com fundo preto semi-transparente
            pygame.draw.rect(word_bg, BLACK, word_bg.get_rect(), border_radius=12)

            # Desenha o texto por cima
            word_bg.blit(text_surface, (padding // 2, padding // 2))

            # Blita tudo na tela principal
            screen.blit(word_bg, (bg_rect.x, bg_rect.y))

        # Mostrar entrada do jogador (restante do seu código)
        input_text_display = input_text
        input_surface = font.render(input_text_display, True, WHITE)

        padding = 20
        bg_width = input_surface.get_width() + padding
        bg_height = input_surface.get_height() + padding
        bg_x = (WIDTH - bg_width) // 2
        bg_y = int(HEIGHT * 0.88)

        input_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(input_bg, BLACK, input_bg.get_rect(), border_radius=16)
        input_bg.blit(input_surface, (padding // 2, padding // 2))

        screen.blit(input_bg, (bg_x, bg_y))

        # Mostrar pontuação (restante do seu código)
        score_text = f"Score: {score}"
        score_surface = font.render(score_text, True, WHITE)

        score_bg_w = score_surface.get_width() + 20
        score_bg_h = score_surface.get_height() + 10
        score_bg_x = int(WIDTH * SCORE_DISPLAY_X_RATIO) - 10
        score_bg_y = int(HEIGHT * SCORE_DISPLAY_Y_RATIO) - 5

        score_bg = pygame.Surface((score_bg_w, score_bg_h), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (0, 0, 0, 150), score_bg.get_rect(), border_radius=12)
        screen.blit(score_bg, (score_bg_x, score_bg_y))

        screen.blit(score_bg, (score_bg_x, score_bg_y))
        screen.blit(score_surface, (score_bg_x + 10, score_bg_y + 5))

        # Barra de energia (restante do seu código)
        bar_w = int(WIDTH * ENERGY_BAR_WIDTH_RATIO)
        bar_h = int(HEIGHT * ENERGY_BAR_HEIGHT_RATIO)
        bar_x = WIDTH - bar_w - int(WIDTH * ENERGY_BAR_RIGHT_MARGIN_RATIO)
        bar_y = int(HEIGHT * ENERGY_BAR_Y_RATIO)
        fill = int((bar_value / MAX_ENERGY) * bar_w)
        bar_color = GOLD if bonus_mode else GREEN
        pygame.draw.rect(screen, (40, 40, 40), (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), border_radius=10)
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill, bar_h), border_radius=8)

        # Combo
        if combo >= 1:
            combo_text = font.render(f"Combo x{min(combo // 10 + 1, COMBO_MAX_MULTIPLIER_BASE)}", True, YELLOW)
            screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, bar_y + bar_h + 10))

        # Modo bônus
        if bonus_mode:
            bonus_text = font.render("Modo Bônus!", True, bar_color)
            screen.blit(bonus_text, (bar_x + bar_w // 2 - bonus_text.get_width() // 2, bar_y + bar_h + BONUS_TEXT_Y_OFFSET_FROM_BAR))

        if bar_value <= MIN_ENERGY_FOR_GAME_OVER:
            if score > max_scores.get(str(fase_atual), 0):
                max_scores[str(fase_atual)] = score
                game_data["max_scores"] = max_scores
                save_game_data(game_data)

            if score > 0 and (fase_atual + 1) in fases and (fase_atual + 1) not in unlocked_fases:
                unlocked_fases.append(fase_atual + 1)
                unlocked_fases.sort()
                game_data["unlocked_fases"] = unlocked_fases
                save_game_data(game_data)

            pygame.mixer.music.stop() # Para a música ao finalizar o jogo
            return draw_game_over(score) 

        pygame.display.flip()
        clock.tick(60)

    return "menu" # Por garantia, se o loop 'running' terminar inesperadamente

def draw_main_menu():
    screen.blit(IMG_MENU_BG, (0, 0))

    # Define o tamanho dos botões com base na resolução da tela
    button_width = int(WIDTH * 0.25)
    button_height = int(HEIGHT * 0.08)

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

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                play_button_click_sound() 
                return "levels"  # Vai para o menu de seleção de fases
            if exit_button_rect.collidepoint(event.pos):
                play_button_click_sound() 
                pygame.quit()
                sys.exit()
    return "menu"



def draw_level_selection_menu():
    global fase_atual, unlocked_fases, max_scores
    screen.blit(FASE_MENU_BG, (0, 0)) # Fundo do menu de fases

    button_width = int(WIDTH * 0.10) # Botões mais estreitos
    button_height = int(HEIGHT * 0.07) # Botões mais baixos
    
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
                                  button_rect.centery - level_text.get_height() // 2 - font_size // 4)) # Ajustar Y para deixar espaço para o score

        # Exibir Score Máximo
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
    back_button_rect = pygame.Rect(WIDTH * 0.02, HEIGHT * 0.88, back_button_width, back_button_height) 

    mouse_pos = pygame.mouse.get_pos()
    back_color = LIGHT_GRAY if back_button_rect.collidepoint(mouse_pos) else DARK_GRAY
    pygame.draw.rect(screen, back_color, back_button_rect, border_radius=8)
    back_text = font.render("VOLTAR", True, WHITE) 
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
                        play_button_click_sound()
                        fase_atual = i
                        return "game" # Inicia o jogo na fase selecionada
                    else:
                        print(f"Fase {i} bloqueada!") # Mensagem de depuração
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                play_button_click_sound() 
                return "menu" # Volta para o menu principal
            
    return "levels"



def run_game():
    current_state = "menu"

    play_menu_music() 

    while True:
        if current_state == "menu":
            if not pygame.mixer.music.get_busy(): 
                play_menu_music()
            current_state = draw_main_menu()
        elif current_state == "game":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop() 
            returned_state = main_game()
            if returned_state == "menu":
                current_state = "menu"
            elif returned_state == "restart":
                current_state = "game" # Permanece no estado 'game' para reiniciar o loop de main_game
            else: # Se o retorno for de game over (draw_game_over), ele já retorna "game" ou "menu"
                current_state = returned_state 
        elif current_state == "levels":
            current_state = draw_level_selection_menu()
        elif current_state == "restart": 
            current_state = "game" # Isso fará com que main_game seja chamado novamente
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    run_game()