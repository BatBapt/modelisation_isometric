import sys

from cube import Cube


class CubeFactory:
    """
    This is the class to create multiple cube in a row such as columns or lines
    """

    def __init__(self, coords, size, color, hauteur, id_case, canvas, container, number_of_cubes):
        try:
            assert isinstance(coords, list), 'Erreur: les coordonées doivent être une liste'
            assert isinstance(size, int), 'Erreur: la taille doit être un entier'
            assert isinstance(color, list), 'Erreur: les couleurs doivent être sous forme de liste'
            assert isinstance(hauteur, int), 'Erreur: la hauteur doit être un entier'
            assert isinstance(id_case, str), "Erreur: l'indentifiant de la case doit être une chaine de caractère"
            assert isinstance(number_of_cubes, int), 'Erreur: le nombre de cube doit être un entier'
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.coords = coords
        self.size = size
        self.color = color
        self.hauteur = hauteur
        self.id_case = id_case
        self.canvas = canvas
        self.container = container
        self.__number = number_of_cubes

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, new_number):
        if new_number < 0:
            raise ValueError('Erreur lors de la création de la figure')
        self.__number = new_number

    def factory_col(self):
        """
        Create a columns
        :return:
        """
        for i in range(self.__number):
            cube = Cube([self.coords[0], self.coords[1] - self.size * i], self.size, self.color, self.hauteur, self.id_case, self.canvas)
            self.container.liste_cube = cube

    def factory_lines(self, direction):
        """
        Create a row
        :param direction: left or right
        :return:
        """
        for i in range(self.__number):
            if direction == "right":
                cube = Cube([self.coords[0] + self.size * i, self.coords[1] + (self.size//2) * i], self.size,
                            self.color, self.hauteur, self.id_case, self.canvas)

            elif direction == "left":
                cube = Cube([self.coords[0] - self.size * i, self.coords[1] + (self.size // 2) * i], self.size,
                            self.color, self.hauteur, self.id_case, self.canvas)

            self.container.liste_cube = cube
