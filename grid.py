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

        self._list_poly = []

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

                a = self.canvas.create_polygon([A, B, C, D], fill="white", outline="black", tags=("grille", 'coords_{}:{}'.format(i, j), bary_x, bary_y))
                self._list_poly.append(a)

    def distance(self, P1, P2):
        dist = sqrt((P2[0] - P1[0])**2 - (P2[1] - P1[1])**2)
        return dist

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

    def get_list_poly(self):
        return self._list_poly

    origin_x = property(get_origin_x)
    origin_y = property(get_origin_y)
    dim = property(get_dim, set_dim)
    list_poly = property(get_list_poly)
