import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2048')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Define font
FONT = pygame.font.SysFont(None, 36)

# Game constants
GRID_SIZE = 4
TILE_SIZE = 80
GRID_MARGIN = 10
GRID_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN
GRID_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2

# Define directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def draw_tile(x, y, value):
    """Draw a tile at the specified position with the specified value."""
    pygame.draw.rect(SCREEN, get_tile_color(value), (x, y, TILE_SIZE, TILE_SIZE))
    text_surface = FONT.render(str(value), True, BLACK)
    text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
    SCREEN.blit(text_surface, text_rect)

def get_tile_color(value):
    """Return the color for the tile based on its value."""
    if value == 0:
        return GRAY
    colors = {
        2: (255, 255, 128),
        4: (255, 255, 0),
        8: (255, 200, 0),
        16: (255, 160, 0),
        32: (255, 128, 0),
        64: (255, 100, 0),
        128: (255, 80, 0),
        256: (255, 60, 0),
        512: (255, 40, 0),
        1024: (255, 20, 0),
        2048: (255, 0, 0)
    }
    return colors.get(value, BLACK)

def draw_grid(grid):
    """Draw the entire grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_OFFSET_X + col * (TILE_SIZE + GRID_MARGIN)
            y = GRID_OFFSET_Y + row * (TILE_SIZE + GRID_MARGIN)
            value = grid[row][col]
            draw_tile(x, y, value)

def generate_random_tile(grid):
    """Generate a random tile (2 or 4) in a random empty position."""
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = random.choice([2, 4])

def move(grid, direction):
    """Move tiles in the specified direction."""
    if direction == UP:
        grid = transpose(grid)
        grid = slide_left(grid)
        grid = transpose(grid)
    elif direction == DOWN:
        grid = transpose(grid)
        grid = slide_right(grid)
        grid = transpose(grid)
    elif direction == LEFT:
        grid = slide_left(grid)
    elif direction == RIGHT:
        grid = slide_right(grid)
    return grid

def transpose(grid):
    """Transpose the grid."""
    return [list(row) for row in zip(*grid)]

def slide_left(grid):
    """Slide tiles to the left."""
    new_grid = []
    for row in grid:
        new_row = []
        last_merged = False
        for tile in row:
            if tile == 0:
                continue
            if not new_row or (new_row[-1] != tile and last_merged):
                new_row.append(tile)
                last_merged = False
            elif new_row[-1] == tile and not last_merged:
                new_row[-1] *= 2
                last_merged = True
        new_row += [0] * (GRID_SIZE - len(new_row))
        new_grid.append(new_row)
    return new_grid

def slide_right(grid):
    """Slide tiles to the right."""
    new_grid = []
    for row in grid:
        new_row = []
        last_merged = False
        for tile in reversed(row):
            if tile == 0:
                continue
            if not new_row or (new_row[-1] != tile and last_merged):
                new_row.append(tile)
                last_merged = False
            elif new_row[-1] == tile and not last_merged:
                new_row[-1] *= 2
                last_merged = True
        new_row = [0] * (GRID_SIZE - len(new_row)) + list(reversed(new_row))
        new_grid.append(new_row)
    return new_grid

def is_game_over(grid):
    """Check if the game is over."""
    for row in grid:
        if 0 in row:
            return False
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i+1]:
                return False
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1):
            if grid[row][col] == grid[row+1][col]:
                return False
    return True

def main():
    """Main game loop."""
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    generate_random_tile(grid)
    generate_random_tile(grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    grid = move(grid, UP)
                elif event.key == pygame.K_DOWN:
                    grid = move(grid, DOWN)
                elif event.key == pygame.K_LEFT:
                    grid = move(grid, LEFT)
                elif event.key == pygame.K_RIGHT:
                    grid = move(grid, RIGHT)
                generate_random_tile(grid)

        SCREEN.fill(WHITE)
        draw_grid(grid)
        pygame.display.flip()

        if is_game_over(grid):
            print("Game Over!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
