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


player_image = pygame.image.load('./player.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (CELL_UNIT, CELL_UNIT))


arrow_dirs = {
    (0, 0): no_arrow,
    (1, 0): arrow,
    (0, -1): pygame.transform.rotate(arrow, angle=90),
    (-1, 0): pygame.transform.rotate(arrow, angle=180),
    (0, 1): pygame.transform.rotate(arrow, angle=270)
}

# Game Values

background_color = (255, 255, 255)  # RGB value


class Player(pygame.sprite.Sprite):
    def __init__(self, image, grid):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.coordinates = [0, 0]
        self.grid = grid
        self.dead = False

    def move(self, dir):
        if self.dead:
            return

        if (dir[0] == 0 and dir[1] == 0):
            return

        if (self.coordinates[0] + dir[0]) < 0 or self.coordinates[0] + dir[0] >= self.grid.width:
            return
        if (self.coordinates[1] + dir[1]) < 0 or self.coordinates[1] + dir[1] >= self.grid.height:
            return

        # If hitting a wall
        if not self.grid.grid[self.coordinates[0] + dir[0]][self.coordinates[1] + dir[1]].walkable:
            return

        # If already walked and want to walk it, dead!
        if self.grid.grid[self.coordinates[0] + dir[0]][self.coordinates[1] + dir[1]].walked:
            self.dead = True

        # Move it!
        self.coordinates[0] += dir[0]
        self.coordinates[1] += dir[1]
        self.rect.x = self.coordinates[0] * CELL_UNIT
        self.rect.y = self.coordinates[1] * CELL_UNIT

        # Update grid walked status on current cell
        self.grid.grid[self.coordinates[0]][self.coordinates[1]].walked = True
        if self.dead:
            self.grid.grid[self.coordinates[0]][self.coordinates[1]].murdered_here = True


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
        walkable = 0
        for x in range(0, self.width):
            for y in range(0, self.height):
                walkable += 1 if self.grid[x][y].walkable else 0

        return walkable / (self.width * self.height)

    def completion_status(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.grid[x][y].walkable and not self.grid[x][y].walked:
                    return False
        return True

    def walk(self):
        # Let's start from position (0, 0) and walk our way through the maze generation process
        self.current = [0, 0]
        self.grid[self.current[0]][self.current[1]].walkable = True
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

                if self.grid[self.current[0] + amplitude][self.current[1]].walkable:
                    # print('already walkable')
                    continue

                # Apply movement if valid
                self.grid[self.current[0] + amplitude][self.current[1]].walkable = True

                # Update direction
                self.grid[self.current[0]][self.current[1]].insert_direction = (amplitude, 0)

                # Set current as new coordinate
                self.current = [self.current[0] + amplitude, self.current[1]]
            elif direction == 'x':
                if (self.current[1] == 0 and amplitude == -1) or (self.current[1] == self.height - 1 and amplitude == 1):
                    # print('invalid')
                    continue

                if self.grid[self.current[0]][self.current[1] + amplitude].walkable:
                    # print('already walkable')
                    continue

                # Apply movement if valid
                self.grid[self.current[0]][self.current[1] + amplitude].walkable = True

                # Update direction
                self.grid[self.current[0]][self.current[1]].insert_direction = (0, amplitude)

                # Set current as new coordinate
                self.current = [self.current[0], self.current[1] + amplitude]

        self.grid[self.current[0]][self.current[1]].end = True
        self.grid[self.current[0]][self.current[1]].walkable = True

    def show(self):
        for row in self.grid:
            print(row)

    def draw(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].draw(surface)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walkable = False
        self.walked = False
        self.murdered_here = False
        self.end = False
        self.insert_direction = (0, 0)

    def draw(self, surface):
        # Drawing cells
        if self.walkable:
            pygame.draw.rect(surface, color=(255, 255, 255), rect=(self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))
            self.draw_direction(surface)

            if self.walked:
                pygame.draw.rect(surface, color=(255, 127, 0), rect=(
                self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))
            if self.murdered_here:
                pygame.draw.rect(surface, color=(125, 0, 0), rect=(
                    self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT,
                    self.y * CELL_UNIT + CELL_UNIT))
        else:
            pygame.draw.rect(surface, color=(55, 55, 55), rect=(self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))

        if self.end:
            pygame.draw.rect(surface, color=(255, 0, 0), rect=(self.x * CELL_UNIT, self.y * CELL_UNIT, self.x * CELL_UNIT + CELL_UNIT, self.y * CELL_UNIT + CELL_UNIT))

    def draw_direction(self, surface):
        surface.blit(arrow_dirs[self.insert_direction], (self.x * CELL_UNIT, self.y * CELL_UNIT))

    def __repr__(self):
        return '0' if self.walkable else '1'


if __name__ == "__main__":
    while True:
        good_grids = []
        num_grids_to_gen = 1
        while num_grids_to_gen > 0:
            # Generate new grid and try if good
            grid = Grid(10, 10)
            grid.walk()

            if grid.ratio() >= 0.6:
                good_grids.append(grid)
                num_grids_to_gen -= 1
                # print("Good grid found!")
                # grid.show()
                # print()

        grid = good_grids[0]

        player = Player(player_image, grid)
        player_group = pygame.sprite.GroupSingle(player)

        game_ended = False
        wait_cycles = 60  # Wait one second for showing off blood
        while True:
            player_dir = (0, 0)
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_ended = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_ended = True
                        break
                    if event.key == pygame.K_w:
                        player_dir = (0, -1)
                    if event.key == pygame.K_s:
                        player_dir = (0, 1)
                    if event.key == pygame.K_a:
                        player_dir = (-1, 0)
                    if event.key == pygame.K_d:
                        player_dir = (1, 0)


            # Game logic
            player.move(player_dir)
            if player.dead or grid.completion_status():
                wait_cycles -= 1
            if grid.completion_status() and wait_cycles == 0:
                break
            if player.dead and wait_cycles == 0:
                break
            if game_ended:
                break

            # Display update
            pygame.Surface.fill(window, background_color)

            # Drawing of grid
            grid.draw(window)

            # Drawing of player
            player_group.draw(window)

            pygame.display.update()
            clock.tick(FPS)

        if game_ended:
            break

    pygame.quit()
    exit(0)
