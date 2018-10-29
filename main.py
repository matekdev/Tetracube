# Library imports
import random
import pygame

# Core & Class import
from core_component import gameboard, window, font, font2, font3
from tetromino import Tetromino


# Check if the game is over
def gameover(gameboard):
    for x in range(0, 10):
        if gameboard[0][x] >= 1:
            return True
    return False


# Shift blocks downward after a block clear
def shiftblocks(gameboard, y):
    rowvalues = []
    # Copy all values within the gameboard
    for row in range(0, 16):
        for col in range(0, 10):
            rowvalues.append(gameboard[row][col])

    # Shift down and replace
    for row in range(y-1, -1, -1):
        for col in range(0, 10):
            gameboard[row+1][col] = rowvalues[(row*10)+col]


# Clears the blocks
def clearblocks(gameboard):
    for y in range(15, -1, -1):                      # Go through each row
        blockcount = 0                          # Count the blocks
        for x in range(0, 10):                  # Go through each column
            if gameboard[y][x] >= 1:
                blockcount += 1
                if blockcount >= 10:
                    for i in range(0, 10):      # Found a full line, begin deleting
                        gameboard[y][i] = 0
                    shiftblocks(gameboard, y)
                    return True
    return False


# Generic function to play sounds and noises
def playsound(soundname):
    if not soundoff:
        pygame.mixer.music.load("sounds/"+soundname)
        pygame.mixer.music.play(0)


# Ticks to control speed of fall
ticks = 0

# Score
score = 0

# Determine if key_down is pressed
pressed = False

# Determine if blocks are currently moving
blockinmotion = False

# Setup NES style piece randomization
previouspiece = 4

# Toggle for sound control
soundoff = False

# Current game is over
IsGameOver = False

# Main game loop
run = True
while run:

    # Pygame timer delay
    pygame.time.delay(50)

    # Draw graphics outside the gameboard
    pygame.draw.rect(window, (45, 45, 45), (400, 0, 10, 640))
    pygame.draw.rect(window, (30, 30, 30), (410, 0, 480, 640))

    # Draw sound icon
    pygame.draw.rect(window, (255, 255, 255), (420, 617.5, 10, 15))
    pygame.draw.rect(window, (255, 255, 255), (434, 620, 2, 10))
    pygame.draw.rect(window, (255, 255, 255), (438, 618, 2, 13))
    pygame.draw.rect(window, (255, 255, 255), (442, 617.5, 2, 15))
    volumesurface = font3.render('(M)', True, (255, 255, 255))
    window.blit(volumesurface, (450, 615))
    # Draw mute icon
    if soundoff:
        pygame.draw.rect(window, (153, 51, 51), (418, 623, 29, 5))

    # Draw "T E T R A CUBE" text
    TETROsurface = font.render('TETRA', True, (255, 255, 255))
    window.blit(TETROsurface, (420, 10))
    CUBEsurface = font.render('CUBE', True, (255, 255, 255))
    window.blit(CUBEsurface, (435, 50))

    # Draw "restart" text
    restartsurface = font2.render('RESTART(R)', True, (255, 255, 255))
    window.blit(restartsurface, (417, 550))

    # Draw "score" text and "score" number
    scoresurface = font2.render('SCORE', True, (255, 255, 255))
    window.blit(scoresurface, (460, 200))
    window.blit(font.render(str(round(score)), 1, (255, 255, 255)), (420, 230))

    # Draw the gameboard and blocks
    for i in range(0, 16):
        for j in range(0, 10):
            if gameboard[i][j] == 0:
                pygame.draw.rect(window, (27, 27, 27), (j*40, i*40, 40, 40))

            # Draw the blocks already placed
            if gameboard[i][j] == 1:
                pygame.draw.rect(window, (122, 216, 239), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 2:
                pygame.draw.rect(window, (47, 100, 214), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 3:
                pygame.draw.rect(window, (255, 182, 0), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 4:
                pygame.draw.rect(window, (255, 255, 153), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 5:
                pygame.draw.rect(window, (0, 255, 127), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 6:
                pygame.draw.rect(window, (84, 0, 255), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)
            elif gameboard[i][j] == 7:
                pygame.draw.rect(window, (255, 58, 58), (j * 40, i * 40, 40, 40))
                pygame.draw.rect(window, (0, 0, 0), (j * 40, i * 40, 40, 40), 1)

    # Draw gameover screen
    if IsGameOver:
        gameoversurface = font.render('GAMEOVER', True, (153, 51, 51))
        window.blit(gameoversurface, (65, 250))

    # Set up Inputs
    input = pygame.key.get_pressed()

    # Setup first block
    if not blockinmotion and not IsGameOver:
        block = Tetromino()                                      # Create new block
        blockchoices = ["I", "J", "L", "O", "S", "T", "Z", "R"]  # Setup the possible choices (NES style)
        randomnumber = random.randint(0, 7)                      # Randomly choose
        if randomnumber == 7 or randomnumber == previouspiece:   # If reroll or duplicate piece is hit
            randomnumber = random.randint(0, 6)                  # Reroll again
        previouspiece = randomnumber                             # Register the previous piece
        block.setshape(blockchoices[randomnumber])               # NES system reduces the chance of a dupe
        block.col = 4                                       # Each piece starts in the middle of the gameboard
        blockinmotion = True                                # Block is now in motion
    elif IsGameOver:
        block = Tetromino()

    # Block moving downwards
    if not IsGameOver:
        ticks += 1                      # Tick rate added to decrease the speed
        if ticks >= 5.5:                # of which the blocks fall
            score += ticks / 5
            if not block.placed:
                block.row += 1
                ticks = 0

    # Controls
    for event in pygame.event.get():

        # Setup mouse
        pos = pygame.mouse.get_pos()

        # Toggle sound with mouse
        if pos[0] >= 420 and pos[0] <= 444 and pos[1] >= 617 and pos[1] <= 635:
            if event.type == pygame.MOUSEBUTTONDOWN:
                soundoff = not soundoff

        # Toggle sound with keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                soundoff = not soundoff

        # Move left
        if event.type == pygame.KEYDOWN and not IsGameOver:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                block.moveleft(gameboard)
                playsound("shift.wav")

        # Move right
        if event.type == pygame.KEYDOWN and not IsGameOver:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                block.moveright(gameboard)
                playsound("shift.wav")

        # Rotate
        if event.type == pygame.KEYDOWN and not IsGameOver:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                block.rotate(gameboard)
                playsound("rotate.wav")

        # Move down
        if event.type == pygame.KEYDOWN and not IsGameOver:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pressed = True
        if event.type == pygame.KEYUP and not IsGameOver:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pressed = False

        # Restart game / restart after game over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                ticks = 0
                score = 0
                playsound("restart.wav")
                for y in range(0, 16):
                    for x in range(0, 10):
                        gameboard[y][x] = 0
                if 'block' in locals():
                    blockchoices = ["I", "J", "L", "O", "S", "T", "Z", "R"]
                    block.setshape(blockchoices[random.randint(0, 6)])
                    block.row = 0
                IsGameOver = False

        # Restart game / restart after game over with mouse
        if pos[0] >= 441 and pos[0] <= 560 and pos[1] >= 557 and pos[1] <= 580:
            if event.type == pygame.MOUSEBUTTONDOWN:
                ticks = 0
                score = 0
                playsound("restart.wav")
                for y in range(0, 16):
                    for x in range(0, 10):
                        gameboard[y][x] = 0
                if 'block' in locals():
                    blockchoices = ["I", "J", "L", "O", "S", "T", "Z", "R"]
                    block.setshape(blockchoices[random.randint(0, 6)])
                    block.row = 0
                IsGameOver = False

        # Exit command
        if event.type == pygame.QUIT:
            run = False

    # Move down toggle state
    if pressed:
        ticks += 2.5

    if not IsGameOver:
        # Draw current block
        block.drawcurrent(gameboard)

        # Check if block hits the left or right
        block.checkcollisionleft(gameboard)
        block.checkcollisionright(gameboard)

        # Check if block is about to hit below
        if block.checkcollisionbelow(gameboard):
            block.drawplaced(gameboard)         # Place the block
            playsound("place.wav")
            del block                           # Delete it
            blockinmotion = False               # No block in motion

            if gameover(gameboard):
                IsGameOver = True

            # Check if blocks need to be cleared
            linescleared = 0                    # Counts the amount of lines cleared
            while clearblocks(gameboard):
                linescleared += 1
                playsound("clear.wav")
                print("cleared line")
                if linescleared == 2:
                    playsound("2clear.wav")
                elif linescleared >= 3:
                    playsound("3clear.wav")

            score += (linescleared*200)         # Add the lines cleared to the score

    # Constantly update pygame graphics
    pygame.display.update()

# Pygame quit out
pygame.quit()

