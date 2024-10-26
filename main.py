import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

WIDTH = 600*1.5
HEIGHT = 400*1.5
SIDE_PANEL_WIDTH = 200*1.5

genius_board = pygame.image.load('img/genius.png')
genius_blue = pygame.image.load('img/genius_blue.png')
genius_green = pygame.image.load('img/genius_green.png')
genius_yellow = pygame.image.load('img/genius_yellow.png')
genius_red = pygame.image.load('img/genius_red.png')

board_size = (WIDTH - SIDE_PANEL_WIDTH, HEIGHT)
color_size = (int(board_size[0] / 2), int(board_size[1] / 2))

genius_board = pygame.transform.scale(genius_board, board_size)
genius_blue = pygame.transform.scale(genius_blue, board_size)
genius_green = pygame.transform.scale(genius_green, board_size)
genius_yellow = pygame.transform.scale(genius_yellow, board_size)
genius_red = pygame.transform.scale(genius_red, board_size)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genius da Estrela")

def tela_inicial():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Clique para Iniciar o Jogo", True, BLACK)
    screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
    pygame.display.update()
    
def tela_jogo(score, round_number):
    screen.fill(WHITE)
    
    screen.blit(genius_board, (0, 0))

    pygame.draw.rect(screen, GRAY, (WIDTH - SIDE_PANEL_WIDTH, 0, SIDE_PANEL_WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)

    score_text = font.render(f"Placar: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - SIDE_PANEL_WIDTH + 10, 50))

    round_text = font.render(f"Rodada: {round_number}", True, BLACK)
    screen.blit(round_text, (WIDTH - SIDE_PANEL_WIDTH + 10, 150))
    
    pygame.display.update()

def obter_cor_da_posicao(pos):
    x, y = pos
    if x < (WIDTH - SIDE_PANEL_WIDTH) / 2 and y < HEIGHT / 2:
        return 'green'
    elif x < (WIDTH - SIDE_PANEL_WIDTH) / 2 and y > HEIGHT / 2:
        return 'red'
    elif x > (WIDTH - SIDE_PANEL_WIDTH) / 2 and y > HEIGHT / 2:
        return 'blue'
    elif x > (WIDTH - SIDE_PANEL_WIDTH) / 2 and y < HEIGHT / 2:
        return 'yellow'
    return None

def mostra_cor(color):
    if color == 'green':
        screen.blit(genius_green, (0, 0))
    elif color == 'red':
        screen.blit(genius_red, (0, 0))
    elif color == 'blue':
        screen.blit(genius_blue, (0, 0))
    elif color == 'yellow':
        screen.blit(genius_yellow, (0, 0))
    
    pygame.display.update()
    pygame.time.delay(500)
    
   
    screen.blit(genius_board, (0, 0))
    pygame.display.update()
    pygame.time.delay(250)
    
def contagem():
    font = pygame.font.Font(None, 72)
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        contagem_text = font.render(str(i), True, BLACK)
        screen.blit(contagem_text, ((WIDTH - contagem_text.get_width()) // 2, (HEIGHT - contagem_text.get_height()) // 2))
        pygame.display.update()
        pygame.time.delay(1000)

    screen.fill(WHITE)
    pygame.display.update()
    
def mostra_erro():
    font = pygame.font.Font(None, 62)
    erro_text = font.render("ERROU!", True, BLACK)
    screen.blit(erro_text, (WIDTH - SIDE_PANEL_WIDTH + 10, 250))
    pygame.display.update()
    pygame.time.delay(500)
    
def chances_esgotadas():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 62)
    erro_text = font.render("Chances Esgotadas!", True, BLACK)
    screen.blit(erro_text, ((WIDTH - erro_text.get_width()) // 2, (HEIGHT - erro_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    tela_inicial()
    

def main():
    clock = pygame.time.Clock()
    start_game = False
    score = 0
    round_number = 1
    sequence = []
    player_sequence = []
    
    tela_inicial()

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_game = True

    contagem()

    while True:
        tela_jogo(score, round_number)
        if round_number == 1:
            pygame.time.delay(1000)

        if len(player_sequence) == 0:
            sequence.append(random.choice(['green', 'red', 'blue', 'yellow']))

        for color in sequence:
            mostra_cor(color)
            pygame.time.delay(500)

        player_sequence = []
        player_turn = True
        index = 0

        while player_turn and index < len(sequence):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    guessed_color = obter_cor_da_posicao(event.pos)
                    
                    if guessed_color:
                        mostra_cor(guessed_color)
                        player_sequence.append(guessed_color)

                        if guessed_color != sequence[index]:
                            mostra_erro()
                            if 'num_errors' not in locals():
                                num_errors = 0
                            num_errors += 1
                            if num_errors == 3:
                                chances_esgotadas()
                                main()
                            tela_jogo(score, round_number)
                            pygame.time.delay(1000)
                            player_turn = False
                            break

                        if len(player_sequence) == len(sequence):
                            if len(sequence) < 5:
                                score += 15
                            elif len(sequence) >= 5 and len(sequence) < 10:
                                score += 25 + round_number
                            else:
                                score += 35 + round_number * 1.2
                                
                            player_turn = False
                        else:
                            index += 1

        if not player_turn and len(player_sequence) == len(sequence):
            round_number += 1

            sequence.append(random.choice(['green', 'red', 'blue', 'yellow']))
            
            tela_jogo(score, round_number)
            pygame.time.delay(1000)

        clock.tick(60)

main()