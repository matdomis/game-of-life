import pygame
import random

from utils import DEATH, LIFE, CELL_SIZE, CELL_LIFE_PROBABILITY

class Cell():
    def __init__(self, x, y, cell_size):
        """
        Initialize a cell in the Game of Life.

        Args:
            x (int): The horizontal pixel position of the cell.
            y (int): The vertical pixel position of the cell.
            cell_size (int): The width and height of the cell in pixels.
        """
       
        self.alive = DEATH
        self.rect = pygame.Rect(x, y, cell_size, cell_size)

    def draw(self, surface):
        """
            Draw the cell on the given surface.

            Args:
                surface (pygame.Surface): The surface to draw the cell on.
        """

        if self.alive:
            color = 'white'
        else:
            color = 'black'

        pygame.draw.rect(surface, color, self.rect)
        
    def toggle(self):
        """
            Toggle the cell state between alive and dead.
        """

        if not self.alive:
            self.alive = LIFE
        else:
            self.alive = DEATH

class Grid:
    def __init__(self, width, height, cell_size):
        """
            Initialize the game grid with cells.
            Also gives each generated cell a CELL_LIFE_PROBABILITY to be alive.

            Args:
                width (int): The width of the screen in pixels.
                height (int): The height of the screen in pixels.
                cell_size (int): The size of each cell in pixels.
        """
        
        self.rows = height // cell_size
        self.cols = width // cell_size
        
        self.cell_size = cell_size

        # Initialize game grid - each element is a cell that starts with DEATH
        self.grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = Cell(j*cell_size, i*cell_size, cell_size)

                if random.random() < CELL_LIFE_PROBABILITY:
                    cell.toggle()

                row.append(cell)
            self.grid.append(row)

    def draw(self, surface):
        """
            Draw all cells in the Grid

            Args:
                surface (pygame.Surface): The surface to draw the grid on.
        """

        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].draw(surface)

    def update(self):
        """
            Update Cell's state depending on its neighbors -- Following the Game Of Life's rules.
            It creates a new grid to not overlap the behavour of the next cell.
        """

        new_grid = []

        for row in range(self.rows):
            new_row = []
            
            for col in range(self.cols):
                cell = self.grid[row][col]
                life_neighbors = self.count_life_neighbors(row, col)
                new_cell = Cell(cell.rect.x, cell.rect.y, self.cell_size)
                
                # If current cell is alive
                if self.grid[row][col].alive == LIFE:
                    if (life_neighbors == 2) or (life_neighbors == 3):
                        new_cell.alive = LIFE
                    else:
                        #self.grid[row][col].toggle()
                        new_cell.alive = DEATH

                # If current cell is not alive
                else:
                    if life_neighbors == 3:
                        #self.grid[row][col].toggle()
                        new_cell.alive = LIFE
                    else:
                        new_cell.alive = DEATH

                new_row.append(new_cell)
            new_grid.append(new_row)
        
        self.grid = new_grid

    def count_life_neighbors(self, x, y):
        """
            Count how many live neighbors the cell at position (x, y) has.

            Args:
                x (int): Row index of the cell.
                y (int): Column index of the cell.

            Returns:
                int: Number of live neighboring cells (0 to 8).
        """
       
        live_count = 0
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    ( 0, -1),          ( 0, 1),
                    ( 1, -1), ( 1, 0), ( 1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbor = self.grid[nx][ny]
                if neighbor.alive == LIFE:
                    live_count += 1

        return live_count
    
class Game:
    def __init__(self, info):
        """
            Initialize the game, including screen and grid setup.

            Args:
                info (pygame.display.Info): Screen info to set resolution.
        """

        self.running = True

        self.clock = pygame.time.Clock()

        self.width = info.current_w
        self.height = info.current_h

        self.fullscreen = True
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.cell_size = CELL_SIZE
       
        self.grid = Grid(self.width, self.height, self.cell_size)

        self.last_update = pygame.time.get_ticks()

        # milliseconds between grid updates
        self.update_interval = 100                                  

    def event_handler(self):
        """
            Handle all incoming Pygame events, including quitting, fullscreen toggle,
            grid reset, and exiting the game.

            Controls:
                - Quit window or press ESC to exit the game.
                - Press F11 to toggle fullscreen mode.
                - Press F10 to reset the game grid.

            Updates the game state accordingly.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Key pressed: {event.key}")
                self.running = False
           
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                
                if event.key == pygame.K_F10:
                    self.grid = Grid(self.width, self.height, self.cell_size)

                if event.key == pygame.K_ESCAPE:
                    self.running = False