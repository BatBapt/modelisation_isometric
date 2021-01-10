class Grid:
    """
    This is the Grid class
    This class will create and store informations about the grid.
    """
    def __init__(self, x, y, d, n, canvas):
        """
        :param x: coords for the starting point of the grid x
        :param y: coords for the starting point of the grid y
        :param d: dimension of the grid (depends on cube size => cubes size)
        :param n: number of case in the grid
        :param canvas: the canvas
        """
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

                a = self.canvas.create_polygon([A, B, C, D],
                                               fill="white", outline="black",
                                               tags=("grille", 'coords_{}:{}'.format(i, j), bary_x, bary_y))
                self._list_poly.append(a)
    @property
    def get_origin_x(self):
        return self._origin_x

    @property
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
