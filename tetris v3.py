import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = ( 0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the grid
grid_width = 10
grid_height = 20

# This sets the margin between each cell
margin = 5

# Set width and height of the window
window_width = grid_width * (margin + 20) + margin
window_height = grid_height * (margin + 20) + margin

# Set the title of the window
pygame.display.set_caption('Tetris')

# Create the window
screen = pygame.display.set_mode([window_width, window_height])

# Create a 2D list representing the grid
grid = []
for row in range(grid_height):
    grid.append([])
    for column in range(grid_width):
        grid[row].append(0)

# Define shapes of the different pieces
# O-shape
O_shape = [[1, 1],
           [1, 1]]

# I-shape
I_shape = [[1],
           [1],
           [1],
           [1]]

# S-shape
S_shape = [[0, 1, 1],
           [1, 1, 0]]

# Z-shape
Z_shape = [[1, 1, 0],
           [0, 1, 1]]

# L-shape
L_shape = [[1, 0],
           [1, 0],
           [1, 1]]

# Reverse L-shape
RL_shape = [[0, 1],
            [0, 1],
            [1, 1]]

# T-shape
T_shape = [[1, 1, 1],
           [0, 1, 0]]

# List of all the pieces
shapes_list = [O_shape, I_shape, S_shape, Z_shape, L_shape, RL_shape, T_shape]

# Pick a random piece from the list
current_piece = random.choice(shapes_list)

# Get the width and height of the piece
piece_height = len(current_piece)
piece_width = len(current_piece[0])

# Random position for the piece
piece_row = 0
piece_column = random.randint(0, grid_width - piece_width)

# Set the speed of the piece
fall_freq = 0.3

# Set the score to 0
score = 0

# Set the game clock
clock = pygame.time.Clock()

# Loop until the user clicks the close button
done = False

# Draw the grid
def draw_grid():
    # Draw the vertical lines
    for row in range(grid_height):
        for column in range(grid_width):
            color = WHITE
            # Set the color of the lines
            if grid[row][column] == 1:
                color = GREEN
            # Draw the rectangles
            pygame.draw.rect(screen,
                             color,
                             [(margin + 20) * column + margin,
                              (margin + 20) * row + margin,
                              20,
                              20])
            # Draw the horizontal lines
            pygame.draw.line(screen, BLACK, [0, (margin + 20) * row + margin], [window_width, (margin + 20) * row + margin], 2)
        # Draw the vertical lines
        pygame.draw.line(screen, BLACK, [(margin + 20) * column + margin, 0], [(margin + 20) * column + margin, window_height], 2)

# Draw the current piece
def draw_piece(piece, row, column):
    for row_num in range(len(piece)):
        for column_num in range(len(piece[row_num])):
            if piece[row_num][column_num] == 1:
                color = GREEN
            else:
                color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(margin + 20) * (column + column_num) + margin,
                              (margin + 20) * (row + row_num) + margin,
                              20,
                              20])

# Move the piece
def move_piece(direction):
    global piece_row, piece_column
    if direction == 'left':
        piece_column -= 1
    elif direction == 'right':
        piece_column += 1
    elif direction == 'down':
        piece_row += 1

# Check for collision
def is_collision(piece, row, column):
    for row_num in range(len(piece)):
        for column_num in range(len(piece[row_num])):
            if piece[row_num][column_num] == 1:
                if row + row_num >= grid_height:
                    return True
                elif column + column_num >= grid_width:
                    return True
                elif grid[row + row_num][column + column_num] == 1:
                    return True
    return False

# Add the piece to the grid
def add_piece_to_grid(piece, row, column):
    for row_num in range(len(piece)):
        for column_num in range(len(piece[row_num])):
            if piece[row_num][column_num] == 1:
                grid[row + row_num][column + column_num] = 1

# Remove complete rows
def remove_complete_rows():
    global score
    for row in range(grid_height):
        complete = True
        for column in range(grid_width):
            if grid[row][column] == 0:
                complete = False
        if complete:
            score += 1
            for row_num in range(row, 0, -1):
                for column_num in range(grid_width):
                    grid[row_num][column_num] = grid[row_num - 1][column_num]

# Main game loop
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_piece('left')
            elif event.key == pygame.K_RIGHT:
                move_piece('right')
            elif event.key == pygame.K_DOWN:
                move_piece('down')

    # Update the grid
    screen.fill(BLACK)
    draw_grid()
    draw_piece(current_piece, piece_row, piece_column)

    # Check if the piece has collided
    if is_collision(current_piece, piece_row, piece_column):
        add_piece_to_grid(current_piece, piece_row, piece_column)
        current_piece = random.choice(shapes_list)
        piece_row = 0
        piece_column = random.randint(0, grid_width - piece_width)
        remove_complete_rows()

    # Move the piece down
    time_elapsed = clock.tick()
    if time_elapsed > fall_freq * 1000:
        move_piece('down')
        time_elapsed = 0

    pygame.display.flip()

pygame.quit()