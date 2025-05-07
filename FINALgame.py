import pygame
import sys
import random

# Must intitialize pygame
pygame.init()

#setting constants for game logic, more convenient to place here
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

#to have colors at the ready, so it doesn't have to be stated later
white = (255, 255, 255)
green = (0, 200, 0)
red = (200, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 200)

#starting the game and setting the caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project Snake Game")

#more game logic and setting up the font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

#pulled from online, don't touch because something will probably break
def draw_text(text, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

#setting up food distribution, making use of the random module 
def get_randomize_food(snake):
    while True:
        position = [random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
               random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE]
        if position not in snake:
            return position

#defining the game and also setting the starting size for the snake
def game_loop():
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = [CELL_SIZE, 0]
    food = get_randomize_food(snake)
    score = 0
    game_over = False

#the main course
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #allowing for the player to either restart or quit
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        return game_loop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else: #Input from the player to move the snake, too confusing
                    if event.key == pygame.K_UP and direction[1] == 0:
                        direction = [0, -CELL_SIZE]
                    elif event.key == pygame.K_DOWN and direction[1] == 0:
                        direction = [0, CELL_SIZE]
                    elif event.key == pygame.K_LEFT and direction[0] == 0:
                        direction = [-CELL_SIZE, 0]
                    elif event.key == pygame.K_RIGHT and direction[0] == 0:
                        direction = [CELL_SIZE, 0]

        if not game_over:
            #Ensuring it actually moves
            new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

            #To ensure the game ends when the snakes collides with itself
            if (new_head in snake or
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_over = True
            else:
                snake.insert(0, new_head)

                #To ensure the game's singular goal is fulfilled
                if new_head == food:
                    score += 1
                    food = get_randomize_food(snake)
                else:
                    snake.pop()

        #Creating graphics for every element in the game
        screen.fill(blue)
        for segment in snake:
            pygame.draw.rect(screen, green, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, red, (*food, CELL_SIZE, CELL_SIZE))

        draw_text(f"Score: {score}", white, 10, 10, center=False)

        if game_over:
            draw_text("NICE TRY", red, WIDTH // 2, HEIGHT // 2 - 20)
            draw_text("Want a rematch? R to restart, Q to quit", red, WIDTH // 2, HEIGHT // 2 + 20)
 
        pygame.display.flip()
        clock.tick(FPS)

game_loop()