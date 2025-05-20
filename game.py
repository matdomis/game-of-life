import pygame

from game_objects import Game, Grid, Cell
from utils import FPS

def main():
    pygame.init()
    info = pygame.display.Info()
    game = Game(info)

    while game.running:
        game.event_handler() 

        current_time = pygame.time.get_ticks()
        if current_time - game.last_update >= game.update_interval:
            game.last_update = current_time
            game.grid.update()
        
        game.screen.fill('black')
        game.grid.draw(game.screen)

        pygame.display.flip()
        game.clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
