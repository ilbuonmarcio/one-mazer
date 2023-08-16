import random


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

    def walk(self):
        # Let's start from position (0, 0) and walk our way through the maze generation process
        self.current = [0, 0]
        self.grid[self.current[0]][self.current[1]].walked = True

        for i in range(0, 5000):
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

                # Set current as new coordinate
                self.current = [self.current[0], self.current[1] + amplitude]
        

    def show(self):
        for row in self.grid:
            print(row)

class Walls:
    def __init__(self, up=1, right=1, down=1, left=1):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = Walls()
        self.walked = False

    def __repr__(self):
        return '0' if self.walked else '1'


if __name__ == "__main__":
    grid = Grid(10, 10)
    grid.show()
    print("Walking on maze...")
    grid.walk()
    grid.show()
