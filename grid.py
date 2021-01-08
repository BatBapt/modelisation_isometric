from math import sqrt
import tkinter as tk


# x+- d, y +- (d/2)


class Grid:
    """
    This is the Grid class
    This class will create and store informations about the grid.
    """
    def __init__(self, x, y, d, n, canvas):
        self.x = x
        self.y = y
        self._dim = d
        self._n = n
        self.canvas = canvas

        self._origin_x = self.x//2+200
        self._origin_y = self.y//6

        self._list_poly = []

    def barycentre(self, points):
        """
        :param points: the point we need to calculate the barycenter
        :return: a tuple that contains the barycenter in x and y
        """
        bary_x = sum([points[i][0] for i in range(len(points))])/4
        bary_y = sum([points[i][1] for i in range(len(points))])/4

        return int(bary_x), int(bary_y)

    def draw_grid(self):
        """
        Draw the grid in function of the dimension
        All the case of the grid are created with a single point: A
        A is the top point
        :return:
        """
        for i in range(self._n):
            A = [self._origin_x + self._dim * i, self._origin_y + (self._dim//2) * i]
            for j in range(self._n):
                A = [A[0] - self._dim, A[1] + (self._dim//2)]
                B = [A[0] + self._dim, A[1] + (self._dim//2)]
                C = [A[0], A[1] + self._dim]
                D = [A[0] - self._dim, A[1] + (self._dim/2)]

                bary_x, bary_y = self.barycentre([A, B, C, D])

                a = self.canvas.create_polygon([A, B, C, D], fill="white", outline="black", tags=("grille", 'coords_{}:{}'.format(i, j), bary_x, bary_y))
                self._list_poly.append(a)

    def look_in(self, find_bary):
        for elem in self._list_poly:
            box = self.canvas.gettags(elem)
            barys = box[2:4]
            if find_bary == barys:
                return box
        return 0

    def distance(self, p1, p2):
        """
        Calcule the distance between 2 points
        :param p1: first point
        :param p2: second point
        :return: return the distance
        """
        dist = sqrt((p2[0] - p1[0]) ** 2 - (p2[1] - p1[1]) ** 2)
        return dist

    def get_origin_x(self):
        return self._origin_x

    def get_origin_y(self):
        return self._origin_y

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, new_dim):
        if new_dim < 0:
            raise ValueError("La dimension ne peut pas être négative")
        self._dim = new_dim

    @property
    def list_poly(self):
        return self._list_poly

    origin_x = property(get_origin_x)
    origin_y = property(get_origin_y)
