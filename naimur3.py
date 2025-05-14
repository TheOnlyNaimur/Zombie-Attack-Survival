# Import necessary OpenGL modules and libraries
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

# Player attributes
playerPosition = [0, 0, 620]  # Player's position
playerAngle = 180  # Player's angle
movementSpeed = 10  # Player's movement speed
roundno = 1  # Current round number

# Game state variables
bullets = []  # List of bullets
maxMissedBullets = 20  # Maximum missed bullets allowed
gameScore = 0  # Player's score

# Enemy attributes
enemies = []  # List of enemies
numOfEnemies = 20  # Initial number of enemies

# Game control flags
followCamera = False  # Toggle for follow camera
playerLife = 5  # Player's life
gameOver = False  # Game over flag
gamePaused = False  # Game paused flag
roundTransition = False  # Round transition flag

# Initialize enemies with randomized attributes
# 10% of enemies have scale 2.0 and increased health
# Remaining enemies have scale 1.0 and default health
i = 0
while i < numOfEnemies:
    x = random.randint(-GRID_LENGTH - 20, GRID_LENGTH - 20)
    z = -GRID_LENGTH
    scale = 2.0 if random.random() < 0.1 else 1.0  # 10% chance for scale 2.0, otherwise 1.0
    direction = 0.01
    hp = 2 if scale == 2.0 else 1  # Increase hp by 1 if scale is 2.0
    enemies.append([x, 25, z, scale, direction, 0.5, hp])
    i += 1

def draw_text2(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    # Draw text in 2D overlay mode
    glDisable(GL_DEPTH_TEST)

    # Save current matrix modes
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore matrix state
    glPopMatrix()  # MODELVIEW
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    # Draw text in 2D overlay mode with default white color
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
    # Render the player model with body, head, cannon, eyes, and legs
    glPushMatrix()
    glTranslatef(playerPosition[0], playerPosition[1], playerPosition[2])
    glRotatef(playerAngle, 0, 1, 0)

    # Body (cuboid)
    glPushMatrix()
    glScalef(1, 2, 1)
    glColor3f(0.5, 0.5, 1)
    glutSolidCube(30)
    glPopMatrix()

    # Head (sphere)
    glPushMatrix()
    glTranslatef(0, 35, 0)
    glColor3f(1, 0.8, 0.6)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()

    # Eyes (two small black spheres on head)
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(-5, 38, 12)  # Left eye
    glutSolidSphere(2, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(5, 38, 12)  # Right eye
    glutSolidSphere(2, 10, 10)
    glPopMatrix()

    # Cannon (cylinder)
    glPushMatrix()
    glTranslatef(0, 10, 15)  
    glColor3f(0, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 10)
    glPopMatrix()



    glPopMatrix()


def draw_bullets():
    # Render all bullets in the game
    global bullets
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        glColor3f(0, 0, 0)
        glutSolidCube(10)
        glPopMatrix()


def draw_zombie(x, y, z, scale):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)

    # Torso
    glPushMatrix()
    glColor3f(0.3, 0.6, 0.3)  # Dirty green
    glScalef(1.1, 1.5, 0.5)
    glutSolidCube(20)
    glPopMatrix()



    # Head
    glPushMatrix()
    glTranslatef(0, 25, 0)
    glColor3f(0.4, 0.8, 0.4)  # Greenish zombie face
    glutSolidSphere(10, 10, 10)
    glPopMatrix()

    # Eyes
    glPushMatrix()
    glTranslatef(-3, 28, 8)
    glColor3f(1, 0, 0)  # Black eyes
    glutSolidSphere(1.5, 5, 5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3, 28, 8)
    glColor3f(1, 0, 0)
    glutSolidSphere(1.5, 5, 5)
    glPopMatrix()

    # Arms (left and right)
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

    # Legs (left and right)
    glPushMatrix()
    glColor3f(0.05, 0.2, 0.05)  # Dark green legs
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
    # Render all enemies with their attributes
    for e in enemies:
        draw_zombie(e[0], e[1], e[2], e[3])






def drawBuilding(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    # Building body (cuboid)
    glColor3f(0.4, 0.4, 0.4)  # Dull gray for abandoned look
    glPushMatrix()
    glScalef(60, 280, 60)  # Width, height (180 units), depth
    glutSolidCube(1)
    glPopMatrix()
    # Windows (semi-transparent quads on all four sides, 8 per face at top)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.8, 0.5, 0.9)  # Yellowish, 70% transparent
    # Front face (z = 30)
    glBegin(GL_QUADS)
    # Left side, top row (y=140 to 160)
    glVertex3f(-20, 100, 30.1)  # Slightly offset to avoid z-fighting
    glVertex3f(-20, 120, 30.1)
    glVertex3f(-5, 120, 30.1)
    glVertex3f(-5, 100, 30.1)
    # Left side, bottom row (y=120 to 140)
    glVertex3f(-20, 80, 30.1)
    glVertex3f(-20, 100, 30.1)
    glVertex3f(-5, 100, 30.1)
    glVertex3f(-5, 80, 30.1)
    # Right side, top row (y=140 to 160)
    glVertex3f(5, 100, 30.1)
    glVertex3f(5, 120, 30.1)
    glVertex3f(20, 120, 30.1)
    glVertex3f(20, 100, 30.1)
    # Right side, bottom row (y=120 to 140)
    glVertex3f(5, 80, 30.1)
    glVertex3f(5, 100, 30.1)
    glVertex3f(20, 100, 30.1)
    glVertex3f(20, 80, 30.1)
    glEnd()
    # Back face (z = -30)
    glBegin(GL_QUADS)
    # Left side, top row
    glVertex3f(-20, 100, -30.1)
    glVertex3f(-20, 120, -30.1)
    glVertex3f(-5, 120, -30.1)
    glVertex3f(-5, 100, -30.1)
    # Left side, bottom row
    glVertex3f(-20, 80, -30.1)
    glVertex3f(-20, 100, -30.1)
    glVertex3f(-5, 100, -30.1)
    glVertex3f(-5, 80, -30.1)
    # Right side, top row
    glVertex3f(5, 100, -30.1)
    glVertex3f(5, 120, -30.1)
    glVertex3f(20, 120, -30.1)
    glVertex3f(20, 100, -30.1)
    # Right side, bottom row
    glVertex3f(5, 80, -30.1)
    glVertex3f(5, 100, -30.1)
    glVertex3f(20, 100, -30.1)
    glVertex3f(20, 80, -30.1)
    glEnd()
    # Left face (x = -30)
    glBegin(GL_QUADS)
    # Back side, top row
    glVertex3f(-30.1, 100, -20)
    glVertex3f(-30.1, 120, -20)
    glVertex3f(-30.1, 120, -5)
    glVertex3f(-30.1, 100, -5)
    # Back side, bottom row
    glVertex3f(-30.1, 80, -20)
    glVertex3f(-30.1, 100, -20)
    glVertex3f(-30.1, 100, -5)
    glVertex3f(-30.1, 80, -5)
    # Front side, top row
    glVertex3f(-30.1, 100, 5)
    glVertex3f(-30.1, 120, 5)
    glVertex3f(-30.1, 120, 20)
    glVertex3f(-30.1, 100, 20)
    # Front side, bottom row
    glVertex3f(-30.1, 80, 5)
    glVertex3f(-30.1, 100, 5)
    glVertex3f(-30.1, 100, 20)
    glVertex3f(-30.1, 80, 20)
    glEnd()
    # Right face (x = 30)
    glBegin(GL_QUADS)
    # Back side, top row
    glVertex3f(30.1, 100, -20)
    glVertex3f(30.1, 120, -20)
    glVertex3f(30.1, 100, -5)
    glVertex3f(30.1, 120, -5)
    # Back side, bottom row
    glVertex3f(30.1, 80, -20)
    glVertex3f(30.1, 100, -20)
    glVertex3f(30.1, 100, -5)
    glVertex3f(30.1, 80, -5)
    # Front side, top row
    glVertex3f(30.1, 100, 5)
    glVertex3f(30.1, 120, 5)
    glVertex3f(30.1, 120, 20)
    glVertex3f(30.1, 100, 20)
    # Front side, bottom row
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
    # Draw tree trunk (cylinder)
    glColor3f(0.25, 0.12, 0.05)  # Darkish brown
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)  # Rotate to make cylinder vertical
    gluCylinder(gluNewQuadric(), 10, 10, 70, 10, 10)  # Height 70
    glPopMatrix()
    # Draw tree top (sphere)
    glColor3f(0.05, 0.15, 0.05)  # Green
    glPushMatrix()
    glTranslatef(0, 70, 0)  # Positioned at top of trunk
    glutSolidSphere(40, 10, 10)
    glPopMatrix()
    glPopMatrix()



def drawTrees():
    # Ensure clean OpenGL state
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    # Define tree positions - placed near walls but slightly in front
    offset_from_wall = 50  # Distance in front of the wall
    tree_spacing = 160     # Space between trees
    
    # Positions along left and right walls (slightly in front)
    left_wall_trees = [(-GRID_LENGTH + offset_from_wall, z) 
                      for z in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    
    right_wall_trees = [(GRID_LENGTH - offset_from_wall, z) 
                       for z in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    
    # Positions along top wall (enemy spawn area)
    top_wall_trees = [(x, -GRID_LENGTH + offset_from_wall) 
                     for x in range(-GRID_LENGTH + 100, GRID_LENGTH - 100, tree_spacing)]
    
    all_tree_positions = left_wall_trees + right_wall_trees + top_wall_trees
    
    # Manually define building positions (2 on left wall, 2 on right wall)
    building_positions = [
        (-650, 80),    # Left wall, z=80
        (-650, 420),   # Left wall, z=420
        (-650, -320),   # Left wall, z=420
        (650, -260),   # Right wall, z=-260
        (650, 120),   # Left wall, z=420
        (650, 420)     # Right wall, z=420
    ]
    
    # Manually define regular tree positions (4 at top wall)
    regular_tree_positions = [

        (-650, 280),    # Left wall, z=80
        (-650, -120), 
         (-650, -30),   # Left wall, z=420
        (-650, -480),   # Left wall, z=420
        (650, -160),   # Right wall, z=-260
        (650, 220),   # Left wall, z=420
        (650, 330),     # Right wall, z=420

       # Top wall trees
        (-30, -650),
        (-80, -650),
        (-150, -650),    
        (-200, -650), 
        (-220, -650), 
        (-270, -650), 
        (-320, -650),  
        (-390, -650),  
        (-460, -650), 
        (-550, -650), 
        (-630, -650),
        (80, -650),
        (180, -650),  
        (200, -650), 
        (270, -650), 
        (320, -650),  
        (390, -650),  
        (460, -650), 
        (550, -650), 
        (630, -650),     # Top wall, x=80
  
    ]
    
    # Remove building and regular tree positions from dead tree positions
    dead_tree_positions = [pos for pos in all_tree_positions if pos not in building_positions and pos not in regular_tree_positions]

    # Enable blending for proper transparency handling
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Draw dead trees
    for x, z in dead_tree_positions:
        glPushMatrix()
        glTranslatef(x, 0, z)
        
        # Generate a static rotation seed based on position
        random.seed(x * 1000 + z)  # Unique seed per tree position
        tree_rotation = random.uniform(0, 360)  # Static rotation

        # Trunk - Dark, twisted wood
        glColor3f(0.2, 0.1, 0.05)  # Dark brown, almost black
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)  # Rotate to stand upright
        gluCylinder(gluNewQuadric(), 8, 6, 80, 10, 10)  # Slight taper
        glPopMatrix()

        # Broken jagged top
        glPushMatrix()
        glTranslatef(0, 80, 0)  # Position at top of trunk
        glRotatef(tree_rotation, 0, 1, 0)  # Apply static rotation
        gluCylinder(gluNewQuadric(), 6, 0, 15, 6, 6)  # Jagged tip
        glPopMatrix()

        # Branches - Twisted, skeletal remains
        branch_length = 40

        # Branch 1 (left, twisted)
        glPushMatrix()
        glTranslatef(0, 60, 0)
        glRotatef(-45, 0, 0, 1)  # Tilt left
        glRotatef(30, 1, 0, 0)   # Tilt forward
        glRotatef(random.uniform(-20, 20), 0, 1, 0)  # Static small twist
        gluCylinder(gluNewQuadric(), 3, 1, branch_length, 6, 6)
        glPopMatrix()

        # Branch 2 (right, jagged)
        glPushMatrix()
        glTranslatef(0, 70, 0)
        glRotatef(45, 0, 0, 1)  # Tilt right
        glRotatef(20, 1, 0, 0)   # Tilt forward
        glRotatef(random.uniform(-15, 15), 0, 1, 0)  # Static small twist
        gluCylinder(gluNewQuadric(), 4, 1, branch_length * 0.8, 6, 6)
        glPopMatrix()

        # Branch 3 (backward, broken)
        glPushMatrix()
        glTranslatef(0, 50, 0)
        glRotatef(180, 0, 1, 0)  # Point backward
        glRotatef(-15, 1, 0, 0)  # Tilt slightly down
        glRotatef(random.uniform(-15, 15), 0, 1, 0)  # Static small twist
        gluCylinder(gluNewQuadric(), 3, 0.5, branch_length * 0.7, 6, 6)
        glPopMatrix()


        # **New Branch 4 (Lower Left)**
        glPushMatrix()
        glTranslatef(0, 40, 0)
        glRotatef(-60, 0, 0, 1)  # Tilt left
        glRotatef(25, 1, 0, 0)   # Tilt forward
        glRotatef(random.uniform(-20, 20), 0, 1, 0)  # Random twist
        gluCylinder(gluNewQuadric(), 2.5, 1, branch_length * 0.6, 6, 6)
        glPopMatrix()

        # **New Branch 5 (Lower Right)**
        glPushMatrix()
        glTranslatef(0, 45, 0)
        glRotatef(60, 0, 0, 1)  # Tilt right
        glRotatef(30, 1, 0, 0)   # Tilt forward
        glRotatef(random.uniform(-15, 15), 0, 1, 0)  # Random twist
        gluCylinder(gluNewQuadric(), 2.5, 1, branch_length * 0.7, 6, 6)
        glPopMatrix()

        # **New Branch 6 (Twisted Top)**
        glPushMatrix()
        glTranslatef(0, 75, 0)
        glRotatef(random.uniform(0, 360), 0, 1, 0)  # Random rotation
        glRotatef(-30, 1, 0, 0)  # Tilt downward slightly
        gluCylinder(gluNewQuadric(), 3, 0.5, branch_length * 0.5, 6, 6)
        glPopMatrix()

        # Optional: Glowing red eyes hidden in the tree
        if random.random() > 0.7:  # 30% chance
            glPushMatrix()
            glTranslatef(random.uniform(-5, 5), 50, random.uniform(-5, 5))
            glColor3f(1, 0, 0)  # Red glowing eyes
            glutSolidSphere(2, 5, 5)
            glPopMatrix()

        glPopMatrix()
    
    # Draw regular trees
    for x, z in regular_tree_positions:
        drawRegularTree(x, z)
    
    # Draw buildings
    for x, z in building_positions:
        drawBuilding(x, 0, z)
    
    glDisable(GL_BLEND)
    
    # Restore OpenGL state
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)

def draw_grid():
    # Render the game grid and walls with alternating colors
    step = 50
    size = GRID_LENGTH
    for x in range(-size, size, step):
        for z in range(-size, size, step):
            glBegin(GL_QUADS)
            # Set light green color for the range 700 to 600
            if 550 <= z <= 700:
                glColor3f(0.6, 1.0, 0.6)  # Light green
            else:
                glColor3f(0.2, 0.2, 0.0)  # Yellowp 
            glVertex3f(x, 0, z)
            glVertex3f(x + step, 0, z)
            glVertex3f(x + step, 0, z + step)
            glVertex3f(x, 0, z + step)
            glEnd()

    drawTrees()  # Call drawTrees to render trees

    wallHeight = 0

        # Enable blending for wall transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.53, 0.81, 0.92, 0.7)  # Light blue color for walls
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(size, 0, -size)
    glVertex3f(size, wallHeight, -size)
    glVertex3f(-size, wallHeight, -size)
    glEnd()

    glColor4f(0.3, 0.3, 0.3, 0.7) # Dark gray color for walls
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
    # Configure the camera perspective and position
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
    # Increase difficulty by adding new zombies and adjusting attributes
    global enemies
    # Increase speed of existing zombies and health after round 3
    for e in enemies:
        e[5] *= speedMultiplier
        if roundno > 3:
            e[6] += 1  # Increase health by 1 after round 3

    # Respawn new zombies with randomized scale and hp
    for _ in range(num_new_zombies):
        x = random.randint(-GRID_LENGTH // 2, GRID_LENGTH // 2)
        z = -GRID_LENGTH
        scale = 2.0 if random.random() < 0.1 else 1.0  # 10% chance for scale 2.0, otherwise 1.0
        direction = 0.02 * speedMultiplier  # Higher speed for new zombies
        hp = 2 if scale == 2.0 else 1  # Set health based on scale
        if roundno > 3:
            hp += 1  # Increase health by 1 after round 3
        enemies.append([x, 0, z, scale, direction, speedMultiplier, hp])

def idle():
    # Main game loop for updating game state
    # Handles enemy movement, bullet updates, and collision detection
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
                e[6] -= 1  # Reduce enemy health
                if e[6] <= 0:  # Enemy dies when health is 0
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
    # Respawn an enemy with randomized attributes
    new_x = random.randint(-GRID_LENGTH-100, GRID_LENGTH-100)
    new_z = -GRID_LENGTH 
    enemy[0] = new_x
    enemy[1] = 25
    enemy[2] = new_z
    enemy[3] = 2.0 if random.random() < 0.1 else 1.0  # Randomize scale
    enemy[6] = 2 if enemy[3] == 2.0 else 1  # Reset health based on scale
    if roundno > 3:
        enemy[6] += 1  # Increase health by 1 after round 3

def keyboardListener(key, x, y):
    # Handle keyboard input for player actions and game controls
    global playerPosition, playerAngle, bullets, playerLife, maxMissedBullets, gameScore, gameOver, enemies, followCamera, roundno, gamePaused, roundTransition

    if key == b'r' or key == b'R':
        playerPosition = [0, 0, 650]
        playerAngle = 180
        bullets = []
        playerLife = 5
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
            scale = 2.0 if random.random() < 0.1 else 1.0  # 10% chance for scale 2.0, otherwise 1.0
            direction = 0.01
            hp = 2 if scale == 2.0 else 1  # Increase hp by 1 if scale is 2.0
            enemies.append([x, 0, z, scale, direction, 0.5, hp])
            i += 1

    if gameOver:
        return

    if key == b'p' or key == b'P':
        gamePaused = not gamePaused
        return

    if roundTransition and key == b'\r':  # Enter key
        roundTransition = False
        increaseZombieDifficulty(5, roundno - 1)
        return

    if gamePaused or roundTransition:
        return

    if key == b'a' or key == b'A':
        playerPosition[0] -= movementSpeed
    elif key == b'd' or key == b'D':
        playerPosition[0] += movementSpeed
    elif key == b'n' or key == b'N':  #cheat code
        maxMissedBullets += 10

    playerPosition[0] = max(-GRID_LENGTH, min(GRID_LENGTH, playerPosition[0]))

def mouseListener(button, state, x, y):
    # Handle mouse input for shooting and toggling camera mode
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
    # Handle special key input for camera movement
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
    # Render the game screen with all elements and UI
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
        # Draw white background square
        glDisable(GL_DEPTH_TEST)

        # Switch to orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # White background
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex2f(300, 350)
        glVertex2f(700, 350)
        glVertex2f(700, 450)
        glVertex2f(300, 450)
        glEnd()

        # Black text
        glColor3f(0, 0, 0)
        draw_text2(400, 410, f"Congrats on clearing Round {roundno - 1}!")
        draw_text2(400, 380, "Press Enter to start the next round.")

        # Restore matrices
        glPopMatrix()  # MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()  # PROJECTION
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)

    else:
        draw_text(10, 780, f"Round: {roundno}")
        draw_text(10, 750, f"Player HP: {playerLife}")
        draw_text(10, 720, f"Game score: {gameScore}")
        draw_text(10, 690, f"Bullet Missed left: {maxMissedBullets}")
    glutSwapBuffers()

def main():
    # Initialize the game and start the main loop
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
