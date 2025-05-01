from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import math
import random

camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 600
rand_var = 423

playerPosition = [0, 0, 0]
playerAngle = 0 
movementSpeed = 10
rotationSpeed = 5

bullets = [] 
missedBullets = 0
gameScore = 0

enemies = []  
numOfEnemies = 5

cheatMode = False
auto_camera = False
followCamera = False
playerLife = 5
gameOver = False

i=0
while i<numOfEnemies:
    x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
    z = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
    scale = 1.0
    direction = 0.01
    enemies.append([x, 0, z, scale, direction])
    i+=1

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

def draw_enemies():
    for e in enemies:
        glPushMatrix()
        glTranslatef(e[0], e[1], e[2])
        glScalef(e[3], e[3], e[3])
        glColor3f(1, 0, 0)
        glutSolidSphere(20, 10, 10)
        glTranslatef(0, 25, 0)
        glColor3f(0.8, 0, 0)
        glutSolidSphere(15, 10, 10)
        glPopMatrix()

def draw_grid():
    step = 60
    size = GRID_LENGTH
    toggle = True
    for x in range(-size, size, step):
        for z in range(-size, size, step):
            glBegin(GL_QUADS)
            if toggle:
                glColor3f(0.2, 0.4, 1.0)  
            else:
                glColor3f(1.0, 1.0, 0.2)
            glVertex3f(x, 0, z)
            glVertex3f(x + step, 0, z)
            glVertex3f(x + step, 0, z + step)
            glVertex3f(x, 0, z + step)
            glEnd()
            toggle = not toggle
        toggle = not toggle

    wallHeight = 100

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(size, 0, -size)
    glVertex3f(size, wallHeight, -size)
    glVertex3f(-size, wallHeight, -size)
    glEnd()

    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(size, wallHeight, size)
    glVertex3f(-size, wallHeight, size)
    glEnd()

    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(-size, 0, size)
    glVertex3f(-size, wallHeight, size)
    glVertex3f(-size, wallHeight, -size)
    glEnd()

    glColor3f(0.0, 0.5, 1.0)
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
            px, py + 60, pz, 
            px + lx * 100, py + 40, pz + lz * 100, 
            0, 1, 0 
        )
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)


def idle():
    global enemies, bullets, missedBullets, playerLife, gameScore, playerPosition, gameOver, playerAngle, cheatMode

    if gameOver:
        glutPostRedisplay()
        return

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
            missedBullets += 1
            removeBullets.append(i)

    bulletHit = []
    for bi, b in enumerate(bullets):
        for ei, e in enumerate(enemies):
            dist = math.sqrt((b[0] - e[0]) ** 2 + (b[2] - e[2]) ** 2)
            if dist < 25: 
                bulletHit.append(bi)
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
            e[0] += (dx / length) * 0.25  
            e[2] += (dz / length) * 0.25
        hitBox = math.sqrt((e[0] - playerPosition[0])**2 + (e[2] - playerPosition[2])**2)
        if hitBox < 30:
            playerLife -= 1
            respawnEnemy(e)
            if playerLife <= 0:
                gameOver = True
                enemies = []
    if cheatMode and not gameOver:
        playerAngle += 2 
        playerAngle %= 360 

        if random.random() < 0.2: 
            px, py, pz = playerPosition
            bullets.append([px, py + 10, pz, playerAngle])


    glutPostRedisplay()
def respawnEnemy(enemy):
    while True:
        new_x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
        new_z = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
        dist = math.sqrt((new_x - playerPosition[0]) ** 2 + (new_z - playerPosition[2]) ** 2)
        if dist > 100:  
            break
    enemy[0] = new_x
    enemy[2] = new_z


def keyboardListener(key, x, y):
    global playerPosition,playerAngle, bullets, playerLife, missedBullets, gameScore, gameOver, enemies,cheatMode, followCamera
    if key == b'r':
        playerPosition = [0, 0, 0]
        playerAngle = 0
        bullets = []
        playerLife = 5
        missedBullets = 0
        gameScore = 0
        gameOver = False
        enemies = []
        numOfEnemies = 5
        i = 0
        while i<numOfEnemies:
            x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
            z = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
            scale = 1.0
            direction = 0.01
            enemies.append([x, 0, z, scale, direction])
            i+=1
    if gameOver:
        return
    if key == b'w':
        rad = math.radians(playerAngle)
        playerPosition[0] += math.sin(rad) * movementSpeed
        playerPosition[2] += math.cos(rad) * movementSpeed
    elif key == b's':
        rad = math.radians(playerAngle)
        playerPosition[0] -= math.sin(rad) * movementSpeed
        playerPosition[2] -= math.cos(rad) * movementSpeed
    elif key == b'a':
        playerAngle += rotationSpeed
    elif key == b'd':
        playerAngle -= rotationSpeed
    elif key == b'c':
        cheatMode = not cheatMode
    elif key == b'v':
        followCamera = not followCamera


    playerPosition[0] = max(-GRID_LENGTH, min(GRID_LENGTH, playerPosition[0]))
    playerPosition[2] = max(-GRID_LENGTH, min(GRID_LENGTH, playerPosition[2]))

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
    if gameOver:
        return
    
    cam_x, cam_y, cam_z = camera_pos
    if key == GLUT_KEY_LEFT:
        cam_x -= 10
    if key == GLUT_KEY_RIGHT:
        cam_x += 10
    if key == GLUT_KEY_UP:
        cam_y += 10
    if key == GLUT_KEY_DOWN:
        cam_y -= 10
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
    else:
        draw_text(10, 770, f"Player life Remaining: {playerLife}")
        draw_text(10, 740, f"Game score: {gameScore}")
        draw_text(10, 710, f"Player Bullet Missed: {missedBullets}")
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glEnable(GL_DEPTH_TEST)
    glutMainLoop()

if __name__ == "__main__":
    main()
