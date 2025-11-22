import pygame
import numpy as np
import math

pygame.init()

# screen
WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# variables

theta = 0
phi = 0

X= 2
Y = 2
Z = -1.5
SIDE = 2
H = 1
B = 1

# class, function

def coor_on_screen(theta, phi, xi, yi, zi):
    e1 = float(-1 * math.cos(theta) * math.sin(phi))
    e2 = float(math.cos(theta) * math.cos(phi))
    e3 = float(math.sin(theta))

    h = H
    b = B

    l = float(xi) 
    m = float(yi)
    n = float(zi - h)

    x = (e2*b - e3*h) / (e1 + e2 * (m / l) + e3 * (n / l))
    y = (m/l) * x
    z = h + (n/l) * x

    xp = x * math.cos(phi) + (y - b) * math.sin(phi)
    yp = -1 * x * math.sin(phi) + (y - b) * math.cos(phi)
    zp = z

    xpp = xp
    ypp = yp * math.cos(theta) + zp * math.sin(theta)
    zpp = -1 * yp * math.sin(theta) + zp * math.cos(theta)

    return xpp, ypp, zpp

def transform_coor(x, y):
    _x = x - WIDTH / 2
    _y = (y - HEIGHT / 2)
    return _x, _y

def transform_coor_rev(x, y):
    _x = x + WIDTH / 2
    _y = y + HEIGHT / 2
    return _x, _y

def draw_line(theta, phi):
    ax, ay, az = coor_on_screen(theta, phi, X, Y, Z + SIDE)
    bx, by, bz = coor_on_screen(theta, phi, X, Y + SIDE, Z + SIDE)
    cx, cy, cz = coor_on_screen(theta, phi, X + SIDE, Y + SIDE, Z + SIDE)
    dx, dy, dz = coor_on_screen(theta, phi, X + SIDE, Y, Z + SIDE)
    ex, ey, ez = coor_on_screen(theta, phi, X, Y, Z)
    fx, fy, fz = coor_on_screen(theta, phi, X, Y + SIDE, Z)
    gx, gy, gz = coor_on_screen(theta, phi, X + SIDE, Y + SIDE, Z)
    hx, hy, hz = coor_on_screen(theta, phi, X + SIDE, Y, Z)

    a_to_b = pygame.draw.line(screen, WHITE, (transform_coor_rev(ax * 100, az * 100)), (transform_coor_rev(bx * 100, bz * 100)), 3)
    a_to_d = pygame.draw.line(screen, WHITE, (transform_coor_rev(ax * 100, az * 100)), (transform_coor_rev(dx * 100, dz * 100)), 3)
    a_to_e = pygame.draw.line(screen, WHITE, (transform_coor_rev(ax * 100, az * 100)), (transform_coor_rev(ex * 100, ez * 100)), 3)
    e_to_f = pygame.draw.line(screen, WHITE, (transform_coor_rev(ex * 100, ez * 100)), (transform_coor_rev(fx * 100, fz * 100)), 3)
    e_to_h = pygame.draw.line(screen, WHITE, (transform_coor_rev(ex * 100, ez * 100)), (transform_coor_rev(hx * 100, hz * 100)), 3)
    b_to_f = pygame.draw.line(screen, WHITE, (transform_coor_rev(bx * 100, bz * 100)), (transform_coor_rev(fx * 100, fz * 100)), 3)
    d_to_h = pygame.draw.line(screen, WHITE, (transform_coor_rev(dx * 100, dz * 100)), (transform_coor_rev(hx * 100, hz * 100)), 3)
    b_to_c = pygame.draw.line(screen, WHITE, (transform_coor_rev(bx * 100, bz * 100)), (transform_coor_rev(cx * 100, cz * 100)), 3)
    c_to_d = pygame.draw.line(screen, WHITE, (transform_coor_rev(cx * 100, cz * 100)), (transform_coor_rev(dx * 100, dz * 100)), 3)
    f_to_g = pygame.draw.line(screen, WHITE, (transform_coor_rev(fx * 100, fz * 100)), (transform_coor_rev(gx * 100, gz * 100)), 3)
    g_to_h = pygame.draw.line(screen, WHITE, (transform_coor_rev(gx * 100, gz * 100)), (transform_coor_rev(hx * 100, hz * 100)), 3)
    c_to_g = pygame.draw.line(screen, WHITE, (transform_coor_rev(cx * 100, cz * 100)), (transform_coor_rev(gx * 100, gz * 100)), 3)

def find_vanishing_point(theta, phi):
    ax, ay, az = coor_on_screen(theta, phi, X, Y, Z + SIDE)
    bx, by, bz = coor_on_screen(theta, phi, X, Y + SIDE, Z + SIDE)
    cx, cy, cz = coor_on_screen(theta, phi, X + SIDE, Y + SIDE, Z + SIDE)
    dx, dy, dz = coor_on_screen(theta, phi, X + SIDE, Y, Z + SIDE)
    ex, ey, ez = coor_on_screen(theta, phi, X, Y, Z)
    fx, fy, fz = coor_on_screen(theta, phi, X, Y + SIDE, Z)
    gx, gy, gz = coor_on_screen(theta, phi, X + SIDE, Y + SIDE, Z)
    hx, hy, hz = coor_on_screen(theta, phi, X + SIDE, Y, Z)

    left1_A = np.array([[bz - az, -(bx - ax)], [fz - ez, -(fx - ex)]])
    left1_B = np.array([ax*(bz - az) - az*(bx - ax), ex*(fz - ez) - ez*(fx - ex)])

    # horizontal 
    if abs(np.linalg.det(left1_A)) < 0.0001:
        line1 = None
        line2 = None
    else:
        left1_C = np.linalg.solve(left1_A, left1_B)
        left1_vanishing_point = [left1_C[0], left1_C[1]]

        line1 = pygame.draw.line(screen, RED, (transform_coor_rev(left1_C[0] * 100, left1_C[1] * 100)), (transform_coor_rev(bx * 100, bz * 100)), 1)
        line2 = pygame.draw.line(screen, RED, (transform_coor_rev(left1_C[0] * 100, left1_C[1] * 100)), (transform_coor_rev(fx * 100, fz * 100)), 1)

    left2_A = np.array([[cz - dz, -(cx - dx)], [gz - hz, -(gx - hx)]])
    left2_B = np.array([dx*(cz - dz) - dz*(cx - dx), hx*(gz - hz) - hz*(gx - hx)])

    if abs(np.linalg.det(left2_A)) < 0.0001:
        line3 = None
        line4 = None
    else:
        left2_C = np.linalg.solve(left2_A, left2_B)
        left2_vanishing_point = [left2_C[0], left2_C[1]]

        line3 = pygame.draw.line(screen, RED, (transform_coor_rev(left2_C[0] * 100, left2_C[1] * 100)), (transform_coor_rev(cx * 100, cz * 100)), 1)
        line4 = pygame.draw.line(screen, RED, (transform_coor_rev(left2_C[0] * 100, left2_C[1] * 100)), (transform_coor_rev(gx * 100, gz * 100)), 1)

    right1_A = np.array([[dz - az, -(dx - ax)], [ez - hz, -(ex - hx)]])
    right1_B = np.array([ax*(dz - az) - az*(dx - ax), hx*(ez - hz) - hz*(ex - hx)])

    if abs(np.linalg.det(right1_A)) < 0.0001:
        line7 = None
        line8 = None
    else:
        right1_C = np.linalg.solve(right1_A, right1_B)
        right1_vanishing_point = [right1_C[0], right1_C[1]]

        line7 = pygame.draw.line(screen, RED, (transform_coor_rev(right1_C[0] * 100, right1_C[1] * 100)), (transform_coor_rev(ax * 100, az * 100)), 1)
        line8 = pygame.draw.line(screen, RED, (transform_coor_rev(right1_C[0] * 100, right1_C[1] * 100)), (transform_coor_rev(ex * 100, ez * 100)), 1)
    
    right2_A = np.array([[cz - bz, -(cx - bx)], [fz - gz, -(fx - gx)]])
    right2_B = np.array([bx*(cz - bz) - bz*(cx - bx), gx*(fz - gz) - gz*(fx - gx)])
    if abs(np.linalg.det(right2_A)) < 0.0001:
        line9 = None
        line10 = None
    else:
        right2_C = np.linalg.solve(right2_A, right2_B)
        right2_vanishing_point = [right2_C[0], right2_C[1]]

        line9 = pygame.draw.line(screen, RED, (transform_coor_rev(right2_C[0] * 100, right2_C[1] * 100)), (transform_coor_rev(bx * 100, bz * 100)), 1)
        line10 = pygame.draw.line(screen, RED, (transform_coor_rev(right2_C[0] * 100, right2_C[1] * 100)), (transform_coor_rev(gx * 100, gz * 100)), 1)

    # vertical
    # if abs(ax - ex) < 0.0001:
    #     line5 = None
    #     line6 = None
    # else:
    #     vertical1_A = np.array([[az - ez, -(ax - ex)], [dz - hz, -(dx - hx)]])
    #     vertical1_B = np.array([ex*(az - ez) - ez*(ax - ex), hx*(dz - hz) - dz*(dx - hx)])
    #     vertical1_C = np.linalg.solve(vertical1_A, vertical1_B)
    #     vertical1_vanishing_point = [vertical1_C[0], vertical1_C[1]]

    #     # line5 = pygame.draw.line(screen, RED, (transform_coor_rev(vertical1_C[0] * 100, vertical1_C[1] * 100)), (transform_coor_rev(ax * 100, az * 100)), 1)
    #     # line6 = pygame.draw.line(screen, RED, (transform_coor_rev(vertical1_C[0] * 100, vertical1_C[1] * 100)), (transform_coor_rev(dx * 100, dz * 100)), 1)

    if abs(ax - ex) < 0.0001 and abs(bx - fx) < 0.0001:
        line11 = None
        line12 = None
    else:
        vertical2_A = np.array([[bz - fz, -(bx - fx)], [az - ez, -(ax - ex)]])
        vertical2_B = np.array([fx*(bz - fz) - fz*(bx - fx), ex*(az - ez) - ez*(ax - ex)])
        vertical2_C = np.linalg.solve(vertical2_A, vertical2_B)
        vertical2_vanishing_point = [vertical2_C[0], vertical2_C[1]]

        line11 = pygame.draw.line(screen, RED, (transform_coor_rev(vertical2_C[0] * 100, vertical2_C[1] * 100)), (transform_coor_rev(ax * 100, az * 100)), 1)
        line12 = pygame.draw.line(screen, RED, (transform_coor_rev(vertical2_C[0] * 100, vertical2_C[1] * 100)), (transform_coor_rev(bx * 100, bz * 100)), 1)
        line13 = pygame.draw.line(screen, RED, (transform_coor_rev(vertical2_C[0] * 100, vertical2_C[1] * 100)), (transform_coor_rev(dx * 100, dz * 100)), 1)
        

    s1 = ((left1_vanishing_point[0]*100)**2 + (left1_vanishing_point[1]*100)**2)**0.5
    s2 = ((left2_vanishing_point[0]*100)**2 + (left2_vanishing_point[1]*100)**2)**0.5
    s3 = ((vertical2_vanishing_point[0]*100)**2 + (vertical2_vanishing_point[1]*100)**2)**0.5 if abs(ax - ex) >= 0.0001 else None

    temp = (s2 / s1)**0.5
    temp2 = ((s1 * s2) ** 0.5) / s3 if s3 is not None else 0

    #print(temp, temp2)
    phi = math.atan(temp)
    if temp2 <= 1 and temp2 >= -1:
        theta = math.asin(temp2)
    else:
        theta = 0
    return theta, phi


# running loop
running = True

while running == True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            phi -= math.radians(5)
        if keys[pygame.K_RIGHT]:
            phi += math.radians(5)   
        if keys[pygame.K_UP]:
            theta += math.radians(5)
        if keys[pygame.K_DOWN]:
            theta -= math.radians(5)

    # inner screen

    screen.fill(BLACK)

    draw_line(theta, phi)
    find_vanishing_point(theta, phi)
    thetap, phip = find_vanishing_point(theta, phi)

    system_font = pygame.font.SysFont('verdanai', 30)
    degree_font = system_font.render("Phi: {0}˚, Theta: {1}˚".format(math.degrees(phi), math.degrees(theta)), True, WHITE, BLACK)
    degree_font_rect = degree_font.get_rect()
    degree_font_rect.center = (WIDTH / 2, 50)
    screen.blit(degree_font, degree_font_rect)
    pygame.display.flip()

pygame.quit()