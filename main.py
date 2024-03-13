import random
import tkinter as tk
from tkinter import messagebox
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# definicje wierzchołków, krawędzi, powierzchni i kolorów sześcianu
vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))
surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
colors = ((1, 0, 0), (0, 1, 0), (1, 0.5, 0), (1, 1, 0), (1, 1, 1), (0, 0, 1))


def show_help():
    text = "Komputerowa symulacja kostki Rubika\n\n"\
           "Opcje dostępne w programie:\n"\
           "* Lewy przycisk myszy - obróć kostkę\n"\
           "* 1 do 9 - obrót warstw kostki\n" \
           "* Q do O - przeciwny obrót warstw kostki\n" \
           "* Z - cofnij ostatni ruch\n" \
           "* X - cofnij wszystkie ruchy\n" \
           "* C - zresetuj ustawienia kamery\n"\
           "* V - potasuj kostkę\n\n"\
           "* H - wyświetl pomoc\n"
    # Funkcja wywoływana po kliknięciu przycisku "Pomoc"
    messagebox.showinfo("Pomoc", text)


# klasa reprezentująca pojedynczy sześcian
class Cube:
    def __init__(self, id, N, scale):
        self.N = N
        self.scale = scale
        self.init_i = [*id]
        self.current_i = [*id]
        self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

    def isMoved(self, axis, slice):
        # sprawdzenie, czy sześcian został obrócony
        return self.current_i[axis] == slice

    def update(self, axis, slice, dir):
        # aktualizacja pozycji i obrót sześcianu po ruchu
        if not self.isMoved(axis, slice):
            return

        i, j = (axis + 1) % 3, (axis + 2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

        self.current_i[i], self.current_i[j] = (
            self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
            self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i])

    def MatrixTransform(self):
        # macierz transformacji dla sześcianu
        scaleA = [[s * self.scale for s in a] for a in self.rot]
        scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_i]
        return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

    def draw(self, surf, animate, angle, axis, slice, dir):
        # rysowanie sześcianów
        glPushMatrix()
        if animate and self.isMoved(axis, slice):
            glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
        glMultMatrixf(self.MatrixTransform())

        glBegin(GL_QUADS)
        for i in range(len(surf)):
            glColor3fv(colors[i])
            for j in surf[i]:
                glVertex3fv(vertices[j])
        glEnd()

        glPopMatrix()


# klasa reprezentująca całą kostkę
class WholeCube:
    def __init__(self, N, scale):
        self.N = N
        cr = range(self.N)
        self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]
        self.small_cube = Cube((N // 2, N, N // 2), self.N, scale/2)  # Tworzenie małego sześcianu
        self.mouse_rotating = False
        self.mouse_start_pos = None
        self.angle_x = 0
        self.angle_y = 0
        self.move_stack = []  # stos przechowuje historię ruchów

    def rotate_cube_with_mouse(self):
        # obrót kostki za pomocą myszy
        if self.mouse_rotating:
            current_pos = pygame.mouse.get_pos()
            diff = (current_pos[0] - self.mouse_start_pos[0], current_pos[1] - self.mouse_start_pos[1])

            rotation_speed = 0.5
            self.angle_y += diff[0] * rotation_speed
            self.angle_x += diff[1] * rotation_speed

            self.mouse_start_pos = current_pos

        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

    def undo_last_move(self):
        # cofnięcie ruchu
        if self.move_stack:
            axis, slice, direction = self.move_stack.pop()
            for cube in self.cubes:
                cube.update(axis, slice, -direction)

    def undo_all_moves(self):
        # początkowe ustawienie kostki
        while self.move_stack:
            self.undo_last_move()

    def reset_camera(self):
        # reset ustawienia kamery
        self.angle_x = 0
        self.angle_y = 0

    def scramble_cube(self, key_map):
        # losowe tasowanie kostki
        moves = list(key_map.keys())
        random.shuffle(moves)
        random_moves = moves[:20]  # Losowy wybór 20 ruchów

        for move in random_moves:
            axis, slice, direction = key_map[move]
            for cube in self.cubes:
                cube.update(axis, slice, direction)

    def mainloop(self):
        rot_slice_map = {K_1: (0, 0, 1), K_2: (0, 1, 1), K_3: (0, 2, 1), K_4: (1, 0, 1), K_5: (1, 1, 1),
                         K_6: (1, 2, 1), K_7: (2, 0, 1), K_8: (2, 1, 1), K_9: (2, 2, 1),
                         K_q: (0, 0, -1), K_w: (0, 1, -1), K_e: (0, 2, -1), K_r: (1, 0, -1), K_t: (1, 1, -1),
                         K_y: (1, 2, -1), K_u: (2, 0, -1), K_i: (2, 1, -1), K_o: (2, 2, -1)}

        ang_x, ang_y, rot_cube = 0, 0, (0, 0)
        animate, animate_ang, animate_speed = False, 0, 5
        action = (0, 0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_rotating = True
                    self.mouse_start_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_rotating = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.mouse_start_pos = None
                if event.type == KEYDOWN:
                    if not animate and event.key in rot_slice_map:
                        animate, action = True, rot_slice_map[event.key]
                        self.move_stack.append(action)
                    elif event.key == K_z:
                        self.undo_last_move()
                    if event.key == K_x:
                        self.undo_all_moves()
                    if event.key == K_c:
                        self.reset_camera()
                    if event.key == K_v:
                        self.scramble_cube(rot_slice_map)
                    if event.key == K_h:
                        show_help()

            ang_x += rot_cube[0] * 2
            ang_y += rot_cube[1] * 2

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -40)

            glRotatef(ang_y, 0, 1, 0)
            glRotatef(ang_x, 1, 0, 0)

            self.rotate_cube_with_mouse()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if animate:
                if animate_ang >= 90:
                    for cube in self.cubes:
                        cube.update(*action)
                    animate, animate_ang = False, 0

            for cube in self.cubes:
                cube.draw(surfaces, animate, animate_ang, *action)
            if animate:
                animate_ang += animate_speed

            # Punkt odniesienia
            glPushMatrix()
            glTranslatef(0, 10, 0)
            glScalef(0.5, 0.5, 0.5)
            color = (0.5, 0.5, 0.5)

            glBegin(GL_QUADS)
            for i in range(len(surfaces)):
                glColor3fv(color)
                for j in surfaces[i]:
                    glVertex3fv(vertices[j])
            glEnd()

            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(10)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    root = tk.Tk()
    root.withdraw()
    show_help()

    NewEntireCube = WholeCube(3, 2)
    NewEntireCube.mainloop()


if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
