from cube import Cube


class CubeFactory:
    """
    This is the class to create multiple cube in a row such as columns or lines
    """

    def __init__(self, coords, size, color, canvas, container, number_of_cubes):
        self.coords = coords
        self.size = size
        self.color = color
        self.canvas = canvas
        self.container = container
        self.number = number_of_cubes

    def factory_col(self):
        for i in range(self.number):
            cube = Cube([self.coords[0], self.coords[1] - self.size * i], self.size, self.color, self.canvas)
            self.container.liste_cube = cube

    def factory_lines(self, direction):
        for i in range(self.number):
            if direction == "right":
                cube = Cube([self.coords[0] + self.size * i, self.coords[1] + (self.size//2) * i], self.size,
                            self.color, self.canvas)

            elif direction == "left":
                cube = Cube([self.coords[0] - self.size * i, self.coords[1] + (self.size // 2) * i], self.size,
                            self.color, self.canvas)

            self.container.liste_cube = cube
