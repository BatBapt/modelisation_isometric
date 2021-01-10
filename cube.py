import sys


class Cube:
    """
    This is the Cube class
    This class will create a cube
    """
    # This variable is used to count how many cube we have
    cpt_cube = 0

    def __init__(self, coords, size, color, hauteur, id_case, canvas):
        try:
            assert isinstance(coords, list), 'Erreur: les coordonées doivent être une liste'
            assert isinstance(size, int), 'Erreur: la taille doit être un entier'
            assert isinstance(color, list), 'Erreur: les couleurs doivent être sous forme de liste'
            assert isinstance(hauteur, int), 'Erreur: la hauteur doit être un entier'
            assert isinstance(id_case, str), "Erreur: l'indentifiant de la case doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._coords = coords
        self.__size = size
        self._color = color
        self.hauteur = hauteur
        self.id_case = id_case
        self._canvas = canvas

        self._cube = []

        self._cpt_cube = 0
        self.draw_cube()

    # Main methods

    def draw_cube(self):
        """
        This function will create a cube with a single point
        :return:
        """
        A = [self._coords[0], self._coords[1]]
        B = [A[0], A[1] + self.__size]
        C = [B[0] + self.__size, B[1] - (self.__size // 2)]
        D = [A[0] + self.__size, A[1] - (self.__size // 2)]
        E = [A[0], A[1] - self.__size]
        F = [A[0] - self.__size, A[1] - (self.__size // 2)]
        G = [B[0] - self.__size, B[1] - (self.__size // 2)]

        id_cube_str = 'cpt_{}'.format(Cube.cpt_cube)

        # Next line will create the 3 face of the cube:
        # The left one
        # The top one
        # The right one
        # All faces will have informations about them such as their barycenter, their size, their face...

        bary_x, bary_y = self.barycentre([F, A, B, G])
        left_side = self._canvas.create_polygon([F, A, B, G], fill=self._color[0], outline="black",
                                                tags=('cube', id_cube_str, bary_x, bary_y, "gauche",
                                                      "size_{}".format(self.__size), self.hauteur,
                                                      self.id_case, self._color[0],
                                                      )
                                               )

        bary_x, bary_y = self.barycentre([A, D, E, F])
        top_side = self._canvas.create_polygon([A, D, E, F], fill=self._color[1], outline="black",
                                               tags=('cube', id_cube_str, bary_x, bary_y, "haut",
                                                     "size_{}".format(self.__size), self.hauteur,
                                                     self.id_case, self._color[1],
                                                     )
                                              )

        bary_x, bary_y = self.barycentre([A, B, C, D])
        right_side = self._canvas.create_polygon([A, B, C, D], fill=self._color[2], outline="black",
                                                 tags=('cube', id_cube_str, bary_x, bary_y, "droite",
                                                       "size_{}".format(self.__size), self.hauteur,
                                                       self.id_case, self._color[2],
                                                       )
                                                )

        Cube.cpt_cube += 1

        # A cube is defined by his face, so we store it
        self._cube = [left_side, top_side, right_side]

    def barycentre(self, points):
        """
        :param points: the point we need to calculate the barycenter
        :return: a tuple that contains the barycenter in x and y
        """
        bary_x = sum([points[i][0] for i in range(len(points))]) / 4
        bary_y = sum([points[i][1] for i in range(len(points))]) / 4

        return int(bary_x), int(bary_y)

    # Getters
    @property
    def cube(self):
        return self._cube

    # Setter

    def set__size(self, new_size):
        try:
            assert isinstance(new_size, int), 'Erreur: la taille doit être un entier'
        except AssertionError as e:
            print(e)

        if new_size < 0:
            raise ValueError("Erreur: la taille d'un cube ne peut pas être négative")

        self._size = new_size

    def set__color(self, id_face, new_color):
        try:
            assert isinstance(new_color, list), 'Erreur: les couleurs doivent être sous forme de liste'
        except AssertionError as e:
            print(e)

        if len(new_color) != 1:
            raise IndexError('La taille de la liste doit être de 1')

        id_item = self._cube[id_face]
        fill = self._canvas.itemcget(id_item, "fill")
        self._canvas.itemconfig(id_item, fill=new_color[0])
