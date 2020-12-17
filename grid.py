from math import sqrt
import tkinter as tk


# x+- d, y +- (d/2)


class Grid:

    def __init__(self, x, y, d, canvas):
        self.x = x
        self.y = y
        self._dim = d
        self.canvas = canvas

        self._origin_x = self.x//2+100
        self._origin_y = self.y//6+50

        self.list_poly = []
        self.list_cube = []

    def get_origin_x(self):
        return self._origin_x

    def get_origin_y(self):
        return self._origin_y

    def get_dim(self):
        return self._dim

    def set_dim(self, new_dim):
        if new_dim < 0:
            raise ValueError("La dimension ne peut pas être négative")
        self._dim = new_dim

    def add_item_on_case(self, id_item, cube):
        # id_item = self.canvas.find_withtag('current')
        tags = self.canvas.gettags(id_item)
        if len(tags[4]) == 0:
            cubes = [cubes]
        else:
            cubes = tags[4]
            cubes.append(cube)

        self.canvas.itemconfig(id_item, tags=("grille", tags[1], tags[2], tags[3], cubes))

    def get_list_cube(self):
        return self.liste_cube

    def set_list_cube(self, new_cube):
        print("Here")
        if new_cube in self.list_cube:
            raise ValueError("Erreur. Ce cube est déjà présent.")
        if not isinstance(new_cube, list):
            raise TypeError("Erreur. Le cube doit être une liste")

        self.liste_cube.append(new_cube)

    liste_cube = property(get_list_cube, set_list_cube)
    origin_x = property(get_origin_x)
    origin_y = property(get_origin_y)
    dim = property(get_dim, set_dim)

    def barycentre(self, points):
        bary_x = sum([points[i][0] for i in range(len(points))])/4
        bary_y = sum([points[i][1] for i in range(len(points))])/4

        return int(bary_x), int(bary_y)

    def draw_grid(self):
        for i in range(10):
            A = [self._origin_x + self._dim*i, self._origin_y + (self._dim//2) *i]
            for j in range(10):
                A = [A[0] - self._dim, A[1] + (self._dim//2)]
                B = [A[0] + self._dim, A[1] + (self._dim//2)]
                C = [A[0], A[1] + self._dim]
                D = [A[0] - self._dim, A[1] + (self._dim/2)]

                bary_x, bary_y = self.barycentre([A, B, C, D])

                a = self.canvas.create_polygon([A, B, C, D], fill="white", outline="black", tags=("grille", '{}:{}'.format(i, j), bary_x, bary_y, []))
                self.list_poly.append(a)



    def distance(self, P1, P2):
        dist = sqrt((P2[0] - P1[0])**2 - (P2[1] - P1[1])**2)
        return dist
