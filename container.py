import tkinter as tk

from grid import Grid
from cube import Cube


class Container:

    def __init__(self, grid, canvas):
        try:
            assert isinstance(grid, Grid), "Erreur: Ce n'est pas une grille"
            assert isinstance(canvas, tk.Canvas), "Erreur: ce n'est pas un canvas"
        except AssertionError as e:
            print(e)

        self.grid = grid
        self.canvas = canvas
        self._liste_cube = []

    def get_liste_cube(self):
        return self._liste_cube

    def set_liste_cube(self, new_cube):
        try:
            assert isinstance(new_cube, Cube), "Erreur: Ce n'est pas un cube"
        except AssertionError as e:
            print(e)

        self._liste_cube.append(new_cube.get_cubes())

    def list_poly_to_dict_case(self):
        dict_case = {}
        for case in self.grid.list_poly:
            if case not in dict_case:
                tags = self.canvas.gettags(case)
                coords = [s for s in tags if "coords_" in s]
                dict_case[case] = [coords[0], 0]
        return dict_case

    liste_cube = property(get_liste_cube, set_liste_cube)
