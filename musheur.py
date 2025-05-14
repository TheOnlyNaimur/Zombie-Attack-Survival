from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import math
import random

# Initialize global variables for camera, player, and game state
camera_pos = (0, 500, 500)  # Camera position
fovY = 120  # Field of view
GRID_LENGTH = 700  # Grid size
rand_var = 423  # Random seed

# Camera movement limits
CAMERA_X_MIN = -GRID_LENGTH
CAMERA_X_MAX = GRID_LENGTH
CAMERA_Y_MIN = 100
CAMERA_Y_MAX = 800

# Player attributes
playerPosition = [0, 0, 620]  # Player's position
playerAngle = 180  # Player's angle
movementSpeed = 10  # Player's movement speed
roundno = 1  # Current round number
playerLife = 5  # Player's life
playerMaxLife = 5  # Player's maximum life for health bar

# Game state variables
bullets = []  # List of bullets
maxMissedBullets = 20  # Maximum missed bullets allowed
gameScore = 0  # Player's score

# Enemy attributes
enemies = []  # List of enemies
numOfEnemies = 20  # Initial number of enemies

# Game control flags
followCamera = False  # Toggle for follow camera
gameOver = False  # Game over flag
gamePaused = False  # Game paused flag
roundTransition = False  # Round transition flag

# Initialize enemies with randomized attributes
i = 0
while i < numOfEnemies:
    x = random.randint(-GRID_LENGTH - 20, GRID_LENGTH - 20)
    z = -GRID_LENGTH
    scale = 2.0 if random.random() < 0.1 else 1.0
    direction = 0.01
    hp = 4 if scale == 2.0 else 2  # Increased health: 4 for large, 2 for regular
    max_hp = hp  # Store max health for health bar
    enemies.append([x, 25, z, scale, direction, 0.5, hp, max_hp])
    i += 1

def draw_text2(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def draw_player():
    glPushMatrix()
    glTranslatef(playerPosition[0], playerPosition[1], playerPosition[2])
    glRotatef(playerAngle, 0, 1, 0)
    glPushMatrix()
    glScalef(1, 2, 1)
    glColor3f(0.5, 0.5, 1)
    glutSolidCube(30)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 35, 0)
    glColor3f(1, 0.8, 0.6)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(-5, 38, 12)
    glutSolidSphere(2, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(5, 38, 12)
    glutSolidSphere(2, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 10, 15)
    glColor3f(0, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 10)
    glPopMatrix()
    glPopMatrix()


def draw_bullets():
    global bullets
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        glColor3f(0, 0, 0)
        glutSolidCube(10)
        glPopMatrix()

def draw_zombie(x, y, z, scale, hp, max_hp):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    glPushMatrix()
    glColor3f(0.3, 0.6, 0.3)
    glScalef(1.1, 1.5, 0.5)
    glutSolidCube(20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 25, 0)
    glColor3f(0.4, 0.8, 0.4)
    glutSolidSphere(10, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-3, 28, 8)
    glColor3f(1, 0, 0)
    glutSolidSphere(1.5, 5, 5)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(3, 28, 8)
    glColor3f(1, 0, 0)
    glutSolidSphere(1.5, 5, 5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.15, 0.35, 0.15)
    glTranslatef(-13, 10, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.15, 0.35, 0.15)
    glTranslatef(13, 10, 0)
    glRotatef(-90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.05, 0.2, 0.05)
    glTranslatef(-10, -25, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 20, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.05, 0.2, 0.05)
    glTranslatef(10, -25, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1.5, 1.5, 20, 10, 10)
    glPopMatrix()
    glPopMatrix()


def draw_enemies():
    for e in enemies:
        draw_zombie(e[0], e[1], e[2], e[3], e[6], e[7])

def drawBuilding(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.4, 0.4, 0.4)
    glPushMatrix()
    glScalef(60, 280, 60)
    glutSolidCube(1)
    glPopMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.8, 0.5, 0.9)
    glBegin(GL_QUADS)
    glVertex3f(-20, 100, 30.1)
    glVertex3f(-20, 120, 30.1)
    glVertex3f(-5, 120, 30.1)
    glVertex3f(-5, 100, 30.1)
    glVertex3f(-20, 80, 30.1)
    glVertex3f(-20, 100, 30.1)
    glVertex3f(-5, 100, 30.1)
    glVertex3f(-5, 80, 30.1)
    glVertex3f(5, 100, 30.1)
    glVertex3f(5, 120, 30.1)
    glVertex3f(20, 120, 30.1)
    glVertex3f(20, 100, 30.1)
    glVertex3f(5, 80, 30.1)
    glVertex3f(5, 100, 30.1)
    glVertex3f(20, 100, 30.1)
    glVertex3f(20, 80, 30.1)
    glVertex3f(-20, 100, -30.1)
    glVertex3f(-20, 120, -30.1)
    glVertex3f(-5, 120, -30.1)
    glVertex3f(-5, 100, -30.1)
    glVertex3f(-20, 80, -30.1)
    glVertex3f(-20, 100, -30.1)
    glVertex3f(-5, 100, -30.1)
    glVertex3f(-5, 80, -30.1)
    glVertex3f(5, 100, -30.1)
    glVertex3f(5, 120, -30.1)
    glVertex3f(20, 120, -30.1)
    glVertex3f(20, 100, -30.1)
    glVertex3f(5, 80, -30.1)
    glVertex3f(5, 100, -30.1)
    glVertex3f(20, 100, -30.1)
    glVertex3f(20, 80, -30.1)
    glVertex3f(-30.1, 100, -20)
    glVertex3f(-30.1, 120, -20)
    glVertex3f(-30.1, 120, -5)
    glVertex3f(-30.1, 100, -5)
    glVertex3f(-30.1, 80, -20)
    glVertex3f(-30.1, 100, -20)
    glVertex3f(-30.1, 100, -5)
    glVertex3f(-30.1, 80, -5)
    glVertex3f(-30.1, 100, 5)
    glVertex3f(-30.1, 120, 5)
    glVertex3f(-30.1, 120, 20)
    glVertex3f(-30.1, 100, 20)
    glVertex3f(-30.1, 80, 5)
    glVertex3f(-30.1, 100, 5)
    glVertex3f(-30.1, 100, 20)
    glVertex3f(-30.1, 80, 20)
    glVertex3f(30.1, 100, -20)
    glVertex3f(30.1, 120, -20)
    glVertex3f(30.1, 100, -5)
    glVertex3f(30.1, 120, -5)
    glVertex3f(30.1, 80, -20)
    glVertex3f(30.1, 100, -20)
    glVertex3f(30.1, 100, -5)
    glVertex3f(30.1, 80, -5)
    glVertex3f(30.1, 100, 5)
    glVertex3f(30.1, 120, 5)
    glVertex3f(30.1, 120, 20)
    glVertex3f(30.1, 100, 20)
    glVertex3f(30.1, 80, 5)
    glVertex3f(30.1, 100, 5)
    glVertex3f(30.1, 100, 20)
    glVertex3f(30.1, 80, 20)
    glEnd()
    glDisable(GL_BLEND)
    glPopMatrix()

def drawRegularTree(x, z):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glColor3f(0.25, 0.12, 0.05)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 70, 10, 10)
    glPopMatrix()
    glColor3f(0.05, 0.15, 0.05)
    glPushMatrix()
    glTranslatef(0, 70, 0)
    glutSolidSphere(40, 10, 10)
    glPopMatrix()
    glPopMatrix()

def drawTrees():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    offset_from_wall = 50
    tree_spacing = 160
    left_wall_trees = [(-GRID_LENGTH + offset_from_wall, z) 
                      for z in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    right_wall_trees = [(GRID_LENGTH - offset_from_wall, z) 
                       for z in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    top_wall_trees = [(x, -GRID_LENGTH + offset_from_wall) 
                     for x in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    all_tree_positions = left_wall_trees + right_wall_trees + top_wall_trees
    building_positions = [
        (-650, 80), (-650, 420), (-650, -320), (650, -260), (650, 120), (650, 420)
    ]
    regular_tree_positions = [
        (-650, 280), (-650, -120), (-650, -30), (-650, -480), (650, -160), (650, 220), (650, 330),
        (-30, -650), (-80, -650), (-150, -650), (-200, -650), (-220, -650), (-270, -650), 
        (-320, -650), (-390, -650), (-460, -650), (-550, -650), (-630, -650),
        (80, -650), (180, -650), (200, -650), (270, -650), (320, -650), (390, -650), 
        (460, -650), (550, -650), (630, -650)
    ]
    dead_tree_positions = [pos for pos in all_tree_positions if pos not in building_positions and pos not in regular_tree_positions]
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for x, z in dead_tree_positions:
        glPushMatrix()
        glTranslatef(x, 0, z)
        random.seed(x * 1000 + z)
        tree_rotation = random.uniform(0, 360)
        glColor3f(0.2, 0.1, 0.05)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 6, 80, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 80, 0)
        glRotatef(tree_rotation, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 6, 0, 15, 6, 6)
        glPopMatrix()
        branch_length = 40
        glPushMatrix()
        glTranslatef(0, 60, 0)
        glRotatef(-45, 0, 0, 1)
        glRotatef(30, 1, 0, 0)
        glRotatef(random.uniform(-20, 20), 0, 1, 0)
        gluCylinder(gluNewQuadric(), 3, 1, branch_length, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 70, 0)
        glRotatef(45, 0, 0, 1)
        glRotatef(20, 1, 0, 0)
        glRotatef(random.uniform(-15, 15), 0, 1, 0)
        gluCylinder(gluNewQuadric(), 4, 1, branch_length * 0.8, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 50, 0)
        glRotatef(180, 0, 1, 0)
        glRotatef(-15, 1, 0, 0)
        glRotatef(random.uniform(-15, 15), 0, 1, 0)
        gluCylinder(gluNewQuadric(), 3, 0.5, branch_length * 0.7, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 40, 0)
        glRotatef(-60, 0, 0, 1)
        glRotatef(25, 1, 0, 0)
        glRotatef(random.uniform(-20, 20), 0, 1, 0)
        gluCylinder(gluNewQuadric(), 2.5, 1, branch_length * 0.6, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 45, 0)
        glRotatef(60, 0, 0, 1)
        glRotatef(30, 1, 0, 0)
        glRotatef(random.uniform(-15, 15), 0, 1, 0)
        gluCylinder(gluNewQuadric(), 2.5, 1, branch_length * 0.7, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 75, 0)
        glRotatef(random.uniform(0, 360), 0, 1, 0)
        glRotatef(-30, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 3, 0.5, branch_length * 0.5, 6, 6)
        glPopMatrix()
        if random.random() > 0.7:
            glPushMatrix()
            glTranslatef(random.uniform(-5, 5), 50, random.uniform(-5, 5))
            glColor3f(1, 0, 0)
            glutSolidSphere(2, 5, 5)
            glPopMatrix()
        glPopMatrix()
    for x, z in regular_tree_positions:
        drawRegularTree(x, z)
    for x, z in building_positions:
        drawBuilding(x, 0, z)
    glDisable(GL_BLEND)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)

def draw_grid():
    step = 50
    size = GRID_LENGTH
    for x in range(-size, size, step):
        for z in range(-size, size, step):
            glBegin(GL_QUADS)
            if 550 <= z <= 700:
                glColor3f(0.6, 1.0, 0.6)
            else:
                glColor3f(0.2, 0.2, 0.0)
            glVertex3f(x, 0, z)
            glVertex3f(x + step, 0, z)
            glVertex3f(x + step, 0, z + step)
            glVertex3f(x, 0, z + step)
            glEnd()
    drawTrees()
    wallHeight = 0
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.53, 0.81, 0.92, 0.7)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(size, 0, -size)
    glVertex3f(size, wallHeight, -size)
    glVertex3f(-size, wallHeight, -size)
    glEnd()
    glColor4f(0.3, 0.3, 0.3, 0.7)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(size, wallHeight, size)
    glVertex3f(-size, wallHeight, size)
    glEnd()
    glColor4f(0.3, 0.3, 0.3, 0.7)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(-size, 0, size)
    glVertex3f(-size, wallHeight, size)
    glVertex3f(-size, wallHeight, -size)
    glEnd()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(size, 0, -size)
    glVertex3f(size, 0, size)
    glVertex3f(size, wallHeight, size)
    glVertex3f(size, wallHeight, -size)
    glEnd()

def setupCamera():
    global camera_pos
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if followCamera:
        px, py, pz = playerPosition
        angle_rad = math.radians(playerAngle)
        lx = math.sin(angle_rad)
        lz = math.cos(angle_rad)
        gluLookAt(
            px, py + 80, pz, 
            px + lx * 100, py + 40, pz + lz * 100, 
            0, 1, 0 
        )
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

def increaseZombieDifficulty(num_new_zombies, speedMultiplier):
    global enemies
    for e in enemies:
        e[5] *= speedMultiplier
        if roundno > 3:
            e[6] += 1
            e[7] += 1  # Update max_hp
    for _ in range(num_new_zombies):
        x = random.randint(-GRID_LENGTH // 2, GRID_LENGTH // 2)
        z = -GRID_LENGTH
        scale = 2.0 if random.random() < 0.1 else 1.0
        direction = 0.02 * speedMultiplier
        hp = 4 if scale == 2.0 else 2
        if roundno > 3:
            hp += 1
        max_hp = hp
        enemies.append([x, 0, z, scale, direction, speedMultiplier, hp, max_hp])

def idle():
    global enemies, bullets, maxMissedBullets, playerLife, gameScore, playerPosition, gameOver, playerAngle, roundno, gamePaused, roundTransition
    if gameOver or gamePaused or roundTransition:
        glutPostRedisplay()
        return
    if gameScore == 10 and roundno == 1:
        roundno = 2
        roundTransition = True
    elif gameScore == 50 and roundno == 2:
        roundno = 3
        roundTransition = True
    elif gameScore == 100 and roundno == 3:
        roundno = 4
        roundTransition = True
    elif gameScore == 200 and roundno == 4:
        roundno = 5
        roundTransition = True
    for e in enemies:
        e[3] += e[4]
        if e[3] > 1.2 or e[3] < 0.8:
            e[4] *= -1
    removeBullets = []
    for i, b in enumerate(bullets):
        angle_rad = math.radians(b[3])
        b[0] += math.sin(angle_rad) * 20
        b[2] += math.cos(angle_rad) * 20
        if abs(b[0]) > GRID_LENGTH or abs(b[2]) > GRID_LENGTH:
            maxMissedBullets -= 1
            if maxMissedBullets <= 0:
                gameOver = True
                bullets = []
                enemies = []
                break
            else:
                removeBullets.append(i)
    bulletHit = []
    for bi, b in enumerate(bullets):
        for ei, e in enumerate(enemies):
            dist = math.sqrt((b[0] - e[0]) ** 2 + (b[2] - e[2]) ** 2)
            if dist < 25: 
                bulletHit.append(bi)
                e[6] -= 1
                if e[6] <= 0:
                    gameScore += 1
                    respawnEnemy(e)
                break
    removeBullets = list(set(removeBullets + bulletHit))
    removeBullets.sort(reverse=True)
    for i in removeBullets:
        if 0 <= i < len(bullets):
            bullets.pop(i)
    for e in enemies:
        dx = playerPosition[0] - e[0]
        dz = playerPosition[2] - e[2]
        length = math.sqrt(dx**2 + dz**2)
        if length > 1e-5:  
            e[0] += (dx / length) * e[5]  
            e[2] += (dz / length) * e[5]
        hitBox = math.sqrt((e[0] - playerPosition[0])**2 + (e[2] - playerPosition[2])**2)
        if hitBox < 30:
            playerLife -= 1
            respawnEnemy(e)
            if playerLife <= 0:
                gameOver = True
                enemies = []
    glutPostRedisplay()

def respawnEnemy(enemy):
    new_x = random.randint(-GRID_LENGTH-100, GRID_LENGTH-100)
    new_z = -GRID_LENGTH 
    enemy[0] = new_x
    enemy[1] = 25
    enemy[2] = new_z
    enemy[3] = 2.0 if random.random() < 0.1 else 1.0
    enemy[6] = 4 if enemy[3] == 2.0 else 2
    enemy[7] = enemy[6]  # Update max_hp
    if roundno > 3:
        enemy[6] += 1
        enemy[7] += 1

def keyboardListener(key, x, y):
    global playerPosition, playerAngle, bullets, playerLife, maxMissedBullets, gameScore, gameOver, enemies, followCamera, roundno, gamePaused, roundTransition, playerMaxLife
    if key == b'r' or key == b'R':
        playerPosition = [0, 0, 650]
        playerAngle = 180
        bullets = []
        playerLife = 5
        playerMaxLife = 5
        maxMissedBullets = 20
        roundno = 1
        gameScore = 0
        gameOver = False
        gamePaused = False
        roundTransition = False
        enemies = []
        numOfEnemies = 20
        i = 0
        while i < numOfEnemies:
            x = random.randint(-GRID_LENGTH - 20, GRID_LENGTH - 20)
            z = -GRID_LENGTH
            scale = 2.0 if random.random() < 0.1 else 1.0
            direction = 0.01
            hp = 4 if scale == 2.0 else 2
            max_hp = hp
            enemies.append([x, 0, z, scale, direction, 0.5, hp, max_hp])
            i += 1
    if gameOver:
        return
    if key == b'p' or key == b'P':
        gamePaused = not gamePaused
        return
    if roundTransition and key == b'\r':
        roundTransition = False
        increaseZombieDifficulty(5, roundno - 1)
        return
    if gamePaused or roundTransition:
        return
    if key == b'a' or key == b'A':
        playerPosition[0] -= movementSpeed
    elif key == b'd' or key == b'D':
        playerPosition[0] += movementSpeed
    elif key == b'n' or key == b'N':
        maxMissedBullets += 10
    playerPosition[0] = max(-GRID_LENGTH, min(GRID_LENGTH, playerPosition[0]))

def mouseListener(button, state, x, y):
    global gameOver
    if gameOver:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        px, py, pz = playerPosition
        bullets.append([px, py + 10, pz, playerAngle])
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        global followCamera
        followCamera = not followCamera

def specialKeyListener(key, x, y):
    global camera_pos, gameOver
    if gameOver or followCamera:
        return
    cam_x, cam_y, cam_z = camera_pos
    if key == GLUT_KEY_LEFT:
        cam_x = max(CAMERA_X_MIN, cam_x - 10)
    if key == GLUT_KEY_RIGHT:
        cam_x = min(CAMERA_X_MAX, cam_x + 10)
    if key == GLUT_KEY_UP:
        cam_y = min(CAMERA_Y_MAX, cam_y + 10)
    if key == GLUT_KEY_DOWN:
        cam_y = max(CAMERA_Y_MIN, cam_y - 10)
    camera_pos = (cam_x, cam_y, cam_z)
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid()
    draw_player()
    draw_bullets()
    draw_enemies()
    if gameOver:
        draw_text(10, 770, "Game Over! Press 'R' to restart.")
        draw_text(10, 740, f"Final Score: {gameScore}")
    elif roundTransition:
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex2f(300, 350)
        glVertex2f(700, 350)
        glVertex2f(700, 450)
        glVertex2f(300, 450)
        glEnd()
        glColor3f(0, 0, 0)
        draw_text2(400, 410, f"Congrats on clearing Round {roundno - 1}!")
        draw_text2(400, 380, "Press Enter to start the next round.")
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
    else:
        draw_text(10, 780, f"Round: {roundno}")
        draw_text(10, 750, f"Player HP: {playerLife}")
        draw_text(10, 720, f"Game score: {gameScore}")
        draw_text(10, 690, f"Bullet Missed left: {maxMissedBullets}")
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Zombie Survival")
    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()

if __name__ == "__main__":
    main()
