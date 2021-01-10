import tkinter as tk

from grid import Grid


class Container:
    """
    This is the container class.
    This class will keep in 'memory' the grid and all what we need
    """
    def __init__(self, grid, canvas):
        try:
            assert isinstance(grid, Grid), "Erreur: Ce n'est pas une grille"
            assert isinstance(canvas, tk.Canvas), "Erreur: ce n'est pas un canvas"
        except AssertionError as e:
            print(e)

        self.grid = grid
        self.canvas = canvas
        self.__liste_cube = []

    @property
    def liste_cube(self):
        return self.__liste_cube

    @liste_cube.setter
    def liste_cube(self, new_cube):
        self.__liste_cube.append(new_cube.cube)

    def list_poly_to_dict_case(self):
        """
        Create a dictionnary.
        This dictionnary will contain every informations we need in the app like:
        - The coord of the case on the grid
        - The grid dim
        :return:
        """
        dict_case = {}
        for case in self.grid.list_poly:
            if case not in dict_case:
                tags = self.canvas.gettags(case)
                coords = [s for s in tags if "coords_" in s]
                # Coords[0]: this is the coords for case of the grid
                # Number of cube in the case
                dict_case[coords[0]] = [0, self.grid.dim]
        return dict_case
