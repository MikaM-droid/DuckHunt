import pygame

pygame.init()

# Set up window
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("First Game")

# Load character image
character_img = pygame.image.load("Duck Hunt Reboot/Assets/cat.png").convert_alpha()

# Character properties
x, y = 50, 50
width, height = character_img.get_width(), character_img.get_height()
vel = 5

moveLeft = False
moveRight = False

def move():
    global x
    if moveLeft:
        x -= vel
    if moveRight:
        x += vel

def start_screen():
    """Displays a start screen and waits for a key press."""
    win.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 50)
    text = font.render("Press any key to start", True, (255, 255, 255))
    win.blit(text, (200, 350))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show start screen before the game loop starts
start_screen()

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False

    move()

    # Redraw game window
    win.fill((0, 0, 0))  # Clear screen
    win.blit(character_img, (x, y))  # Draw character
    pygame.display.update()

pygame.quit()


########################################################################################################
import pygame

pygame.init()

win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("First game")

x = 50
y = 50
width = 40
height = 60
vel = 5

moveLeft = False
moveRight = False
run = True

def move():
    global x
    if moveLeft:
        x -= vel
    if moveRight:
        x += vel

while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
    
    move()
    
    win.fill((0, 0, 0))  # Clear screen
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  # Draw character
    pygame.display.update()
    
pygame.quit()

