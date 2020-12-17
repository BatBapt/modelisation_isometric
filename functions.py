def draw_cube_col(start_point, n, taille, canvas):
    for i in range(n):
        draw_cube([start_point[0], start_point[1]-taille*i], taille, canvas)


def draw_cube_row(start_point, n, taille, direction, canvas):
    for i in range(n):
        if direction == "right":
            draw_cube([start_point[0]+taille*i, start_point[1]+(taille//2)*i], taille, canvas)
        elif direction == "left":
            draw_cube([start_point[0]-taille*i, start_point[1]+(taille//2)*i], taille, canvas)


def distance(self, A, B):
    dist = sqrt(((A[0]-B[0])**2) + (A[1]-B[1])**2)
    return dist
