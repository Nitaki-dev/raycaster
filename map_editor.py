import pygame
from pygame.locals import *
import ast

# Width and height of the map
WIDTH, HEIGHT = 24, 24

# Size of each cell
CELL_SIZE = 16

# Possible values for each cell
VALUES = list(range(9))

# Directory where textures are stored
TEXTURE_DIR = "pics"

# File where the map will be saved
MAP_FILE = 'map.txt'

# Load the textures
TEXTURES = [pygame.Surface((CELL_SIZE, CELL_SIZE)) if i == 0 else pygame.transform.scale(pygame.image.load(f"{TEXTURE_DIR}/texture_{i-1}.png"), (CELL_SIZE, CELL_SIZE)) for i in VALUES]
TEXTURES[0].fill((0, 0, 0))  # Texture 0 is a black surface

class MapEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
        pygame.display.set_caption('Map Editor')
        self.clock = pygame.time.Clock()
        self.map = self.load_map()

    def draw_map(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                self.screen.blit(TEXTURES[self.map[i][j]], (j*CELL_SIZE, i*CELL_SIZE))
        pygame.display.flip()

    def load_map(self):
        try:
            with open(MAP_FILE, 'r') as f:
                map_data = f.read().replace('{', '[').replace('}', ']')
                print("Map loaded!")
                return ast.literal_eval(map_data)
        except (FileNotFoundError, SyntaxError):
            # If the file doesn't exist or it can't be decoded as a dictionary, return a default map
            print("Couldn't load map file, using blank map instead")
            return [[0]*HEIGHT for _ in range(WIDTH)]

    def save_map(self):
        with open(MAP_FILE, 'w') as f:
            f.write(str(self.map).replace('[', '{').replace(']', '}'))
            print("Map saved!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                i, j = y // CELL_SIZE, x // CELL_SIZE
                if event.button == 1:  # Left mouse button
                    self.map[i][j] = (self.map[i][j] + 1) % len(VALUES)
                elif event.button == 3:  # Right mouse button
                    self.map[i][j] = 0
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    self.save_map()
        return True

    def run(self):
        while self.handle_events():
            self.draw_map()
            self.clock.tick(60)

def main():
    editor = MapEditor()
    editor.run()
    pygame.quit()

if __name__ == '__main__':
    main()
