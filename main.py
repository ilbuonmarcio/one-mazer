import random
import pygame

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1000, 1000
CELLS_PER_UNIT = 10
CELL_UNIT = WIDTH / CELLS_PER_UNIT
FPS = 60
GAME_TITLE = 'One Maze'

window = pygame.display.set_mode(GAME_RES, pygame.HWACCEL|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

no_arrow = pygame.Surface((CELL_UNIT, CELL_UNIT))
pygame.Surface.fill(no_arrow, color=(50, 50, 50))
arrow = pygame.image.load("./arrow.png").convert()
arrow = pygame.transform.scale(arrow, (CELL_UNIT, CELL_UNIT))
arrow.set_alpha(30)


arrow_dirs = {
    (0, 0): no_arrow,
    (1, 0): arrow,
    (0, -1): pygame.transform.rotate(arrow, angle=90),
    (-1, 0): pygame.transform.rotate(arrow, angle=180),
    (0, 1): pygame.transform.rotate(arrow, angle=270)
}

# Game Values

background_color = (150, 150, 150)  # RGB value


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.current = [0, 0]
        self.initialize()

    def initialize(self):
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(Cell(x, y))
            self.grid.append(row)

    def ratio(self):
        walked = 0
        for x in range(0, self.width):
            for y in range(0, self.height):
                walked += 1 if self.grid[x][y].walked else 0

        return walked / (self.width * self.height)

    def walk(self):
        # Let's start from position (0, 0) and walk our way through the maze generation process
        self.current = [0, 0]
        self.grid[self.current[0]][self.current[1]].walked = True

        for i in range(0, 100000):
            # print(f"Current ratio: {self.ratio()}")

            # Decide on a vertical or horizontal movement
            direction, amplitude = random.choice(['x', 'y']), random.choice([-1, 1])

            # print(direction, amplitude)

            # Check if walkable, if not, try again
            if direction == 'y':
                if (self.current[0] == 0 and amplitude == -1) or (self.current[0] == self.width - 1 and amplitude == 1):
                    # print('invalid')
                    continue

                if self.grid[self.current[0] + amplitude][self.current[1]].walked:
                    # print('already walked')
                    continue

                # Apply movement if valid
                self.grid[self.current[0] + amplitude][self.current[1]].walked = True

                # Edit walls
                if amplitude == 1:
                    self.grid[self.current[0]][self.current[1]].walls.down = 0
                    self.grid[self.current[0] + amplitude][self.current[1]].walls.up = 0
                elif amplitude == -1:
                    self.grid[self.current[0]][self.current[1]].walls.up = 0
                    self.grid[self.current[0] + amplitude][self.current[1]].walls.down = 0

                # Update direction
                self.grid[self.current[0]][self.current[1]].insert_direction = (amplitude, 0)

                # Set current as new coordinate
                self.current = [self.current[0] + amplitude, self.current[1]]
            elif direction == 'x':
                if (self.current[1] == 0 and amplitude == -1) or (self.current[1] == self.height - 1 and amplitude == 1):
                    # print('invalid')
                    continue

                if self.grid[self.current[0]][self.current[1] + amplitude].walked:
                    # print('already walked')
                    continue

                # Apply movement if valid
                self.grid[self.current[0]][self.current[1] + amplitude].walked = True

                # Edit walls
                if amplitude == 1:
                    self.grid[self.current[0]][self.current[1]].walls.right = 0
                    self.grid[self.current[0]][self.current[1] + amplitude].walls.left = 0
                elif amplitude == -1:
                    self.grid[self.current[0]][self.current[1]].walls.left = 0
                    self.grid[self.current[0]][self.current[1] + amplitude].walls.right = 0

                # Update direction
                self.grid[self.current[0]][self.current[1]].insert_direction = (0, amplitude)

                # Set current as new coordinate
                self.current = [self.current[0], self.current[1] + amplitude]

    def show(self):
        for row in self.grid:
            print(row)

    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].draw(surface)


class Walls:
    def __init__(self, cell=None, up=1, right=1, down=1, left=1):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.cell = cell

    def draw(self, surface):
        return  # Disabled
        if self.up:
            pygame.draw.line(surface, color=(0, 0, 255), start_pos=(self.cell.x * CELL_UNIT, self.cell.y * CELL_UNIT), end_pos=(self.cell.x * CELL_UNIT + CELL_UNIT, self.cell.y * CELL_UNIT), width=5)
        if self.down:
            pygame.draw.line(surface, color=(0, 255, 0), start_pos=(self.cell.x * CELL_UNIT, self.cell.y * CELL_UNIT + CELL_UNIT), end_pos=(self.cell.x * CELL_UNIT + CELL_UNIT, self.cell.y * CELL_UNIT + CELL_UNIT), width=5)
        if self.left:
            pygame.draw.line(surface, color=(255, 0, 0), start_pos=(self.cell.x * CELL_UNIT, self.cell.y * CELL_UNIT), end_pos=(self.cell.x * CELL_UNIT, self.cell.y * CELL_UNIT + CELL_UNIT), width=5)
        if self.right:
            pygame.draw.line(surface, color=(127, 127, 127), start_pos=(self.cell.x * CELL_UNIT + CELL_UNIT, self.cell.y * CELL_UNIT), end_pos=(self.cell.x * CELL_UNIT + CELL_UNIT, self.cell.y * CELL_UNIT + CELL_UNIT), width=5)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = Walls(cell=self)
        self.walked = False
        self.previous_insert_direction = (0, 0)
        self.insert_direction = (0, 0)

    def draw(self, surface):
        # Drawing cells
        if self.walked:
            pygame.draw.rect(surface, color=(255, 255, 255), rect=(self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))
        else:
            pygame.draw.rect(surface, color=(0, 0, 0), rect=(self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))

        # Drawing walls
        self.walls.draw(surface)

        # Drawing rows
        self.draw_direction(surface)

    def draw_direction(self, surface):
        surface.blit(arrow_dirs[self.insert_direction], (self.x * CELL_UNIT, self.y * CELL_UNIT))

    def __repr__(self):
        return '0' if self.walked else '1'


if __name__ == "__main__":
    good_grids = []
    num_grids_to_gen = 1
    while num_grids_to_gen > 0:
        # Generate new grid and try if good
        grid = Grid(10, 10)
        grid.walk()

        if grid.ratio() >= 0.6:
            good_grids.append(grid)
            num_grids_to_gen -= 1
            print("Good grid found!")
            grid.show()
            print()

    grid = good_grids[0]

    game_ended = False
    while not game_ended:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_ended = True
                    break

        # Game logic
        # HERE

        # Display update
        pygame.Surface.fill(window, background_color)

        # Drawing of grid
        grid.draw(window)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    exit(0)
