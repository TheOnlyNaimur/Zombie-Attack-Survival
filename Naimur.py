from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import sys


WINDOW_WIDTH = 1000 # Window settings
WINDOW_HEIGHT = 800


camera_pos = [0, 500, 500] # Camera
fovY = 120 # Field of view in Y direction
camera_mode = 0  # 0 = default 3rd person, 1 = gun follow


player_angle = 0
player_pos = [0, 0, 60]  # Now using explicit position instead of polar coordinates
bullets = []
enemies = []
score = 0
lives = 5
missed = 0
cheat_mode = False
cheat_vision = False
auto_aim = False
game_over = False  
cheat_rotation = 0
last_bullet_frame = 0  
frame_count = 0

# Constants
BULLET_SPEED = 10
ENEMY_COUNT = 5
GRID_LENGTH = 600
PLAYER_SPEED = 10
ROTATION_SPEED = 5
ENEMY_SPEED = 0.1 
CHEAT_BULLET_INTERVAL = 100  
CHEAT_ROTATION_SPEED = 5  
AUTO_AIM_ANGLE_THRESHOLD = 15 # Angle threshold for auto-aiming
AUTO_AIM_CAMERA_OFFSET = 1.5  # How much to look ahead when auto-aiming



class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def update(self):
        self.x += BULLET_SPEED * math.cos(math.radians(self.angle))
        self.y += BULLET_SPEED * math.sin(math.radians(self.angle))


class Enemy:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.z = 0
        self.scale = 1.0
        self.grow = True

    def update(self):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        mag = math.sqrt(dx ** 2 + dy ** 2)
        if mag > 0:
            self.x += dx / mag * ENEMY_SPEED
            self.y += dy / mag * ENEMY_SPEED

        # Animate scale
        if self.grow:
            self.scale += 0.01
            if self.scale >= 1.3:
                self.grow = False
        else:
            self.scale -= 0.01
            if self.scale <= 0.7:
                self.grow = True


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
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


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])


    if game_over:
      glRotatef(90, 1, 0, 0)  # Rotate to lie down
      glTranslatef(0, 0, -30)  # position
    else:
        glRotatef(player_angle, 0, 0, 1)  # Normal rotation


    # Head (Black Sphere)
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 55)
    glutSolidSphere(15, 20, 20)
    glPopMatrix()

    # Body (Small Cuboid)
    glColor3f(0, 1, 1)
    glPushMatrix()
    glScalef(1, 1, 2.7)
    glutSolidCube(30)
    glPopMatrix()

    # Arms and Cannon
    glColor3f(0.96, 0.76, 0.44)
    # Left arm
    glPushMatrix()
    glTranslatef(9, -17, 25)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 20, 20)
    glPopMatrix()

    # Cannon 
    glColor3f(1, 1, 0)
    glPushMatrix()
    glTranslatef(0, 0, 25)  # Center of body
    glTranslatef(9, 0, 0)  # Extend forward
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 30, 20, 20)
    glPopMatrix()

    # Right arm
    glColor3f(0.96, 0.76, 0.44)
    glPushMatrix()
    glTranslatef(9, 17, 25)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 20, 20)
    glPopMatrix()

    # Legs
    glColor3f(0, 0, 1)
    # Left leg
    glPushMatrix()
    glTranslatef(0, 17, -65)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 5, 5, 40, 20, 20)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0, -17, -65)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 5, 5, 40, 20, 20)
    glPopMatrix()

    glPopMatrix()


def draw_enemies():
    global lives
    for enemy in enemies:
        enemy.update()

        # Collision detection
        dx = enemy.x - player_pos[0]
        dy = enemy.y - player_pos[1]
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist < 30:
            enemy.reset()
            lives -= 1

        # Draw the enemy
        glPushMatrix()
        glTranslatef(enemy.x, enemy.y, enemy.z + 30)
        glScalef(enemy.scale, enemy.scale, enemy.scale)

        # Body 
        glColor3f(1, 0, 0)
        glutSolidSphere(25, 20, 20)

        # Head 
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, 35)
        glutSolidSphere(15, 20, 20)

        glPopMatrix()


def draw_bullets():
    global missed, score
    for b in bullets[:]:
        b.update()
        # Draw cube
        glPushMatrix()
        glTranslatef(b.x, b.y, b.z)
        glColor3f(0, 1, 1)
        glutSolidCube(10)
        glPopMatrix()

        # Check off screen
        if abs(b.x) > GRID_LENGTH or abs(b.y) > GRID_LENGTH:
            bullets.remove(b)
            missed += 1
            continue

        # Check collision with enemies
        for e in enemies:
            dx = e.x - b.x
            dy = e.y - b.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < 30:
                bullets.remove(b)
                e.reset()
                score += 1
                break


def draw_grid():
    glBegin(GL_QUADS)
    subdivisions = 8
    step = GRID_LENGTH * 2 / subdivisions

    for i in range(subdivisions):
        for j in range(subdivisions):
            x_start = -GRID_LENGTH + i * step
            x_end = x_start + step
            y_start = -GRID_LENGTH + j * step
            y_end = y_start + step

            if (i + j) % 2 == 0:
                glColor3f(0.5, 0, 0.5)
            else:
                glColor3f(1, 1, 1)
            
            glVertex3f(x_start, y_start, 0)
            glVertex3f(x_end, y_start, 0)
            glVertex3f(x_end, y_end, 0)
            glVertex3f(x_start, y_end, 0)
    glEnd()


def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == 0:
        # Third person view
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  0, 0, 0,
                  0, 0, 1)
    else:
        # First person view
        eye_x = player_pos[0] + 30 * math.cos(math.radians(player_angle))
        eye_y = player_pos[1] + 30 * math.sin(math.radians(player_angle))
        eye_z = player_pos[2] + 50
        
        # when auto-aiming
        look_factor = AUTO_AIM_CAMERA_OFFSET if (cheat_mode and auto_aim) else 1.0
        center_x = eye_x + 50 * look_factor * math.cos(math.radians(player_angle))
        center_y = eye_y + 50 * look_factor * math.sin(math.radians(player_angle))
        center_z = eye_z
        
        gluLookAt(eye_x, eye_y, eye_z,
                  center_x, center_y, center_z,
                  0, 0, 1)

def keyboardListener(key, x, y):
    global player_angle, player_pos, cheat_mode, auto_aim, game_over, last_bullet_frame, frame_count
    
    if game_over and key == b'r':
        reset_game()
        return
        
    if key == b'w':  # Move forward 
        player_pos[0] += PLAYER_SPEED * math.cos(math.radians(player_angle))
        player_pos[1] += PLAYER_SPEED * math.sin(math.radians(player_angle))
    if key == b's':  # Move backward 
        player_pos[0] -= PLAYER_SPEED * math.cos(math.radians(player_angle))
        player_pos[1] -= PLAYER_SPEED * math.sin(math.radians(player_angle))
    if key == b'a' and not cheat_mode:  
        player_angle += ROTATION_SPEED
    if key == b'd' and not cheat_mode:  
        player_angle -= ROTATION_SPEED
    if key == b'c':  # Toggle cheat mode
        cheat_mode = not cheat_mode
        last_bullet_frame = frame_count
        if not cheat_mode:
            auto_aim = False  # Disable auto-aim 
    if key == b'v' and cheat_mode:  # Toggle auto-aim 
        auto_aim = not auto_aim

    # Boundary checking
    player_pos[0] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[0]))
    player_pos[1] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[1]))


def specialKeyListener(key, x, y):
    global camera_pos
    if key == GLUT_KEY_LEFT:
        camera_pos[0] -= 20
    if key == GLUT_KEY_RIGHT:
        camera_pos[0] += 20
    if key == GLUT_KEY_UP:
        camera_pos[2] += 20
    if key == GLUT_KEY_DOWN:
        camera_pos[2] -= 20


def mouseListener(button, state, x, y):
    global camera_mode, bullets
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Calculate bullet 
        bullet_x = player_pos[0] + 70 * math.cos(math.radians(player_angle))
        bullet_y = player_pos[1] + 70 * math.sin(math.radians(player_angle))
        bullet_z = player_pos[2] + 25  # Height of cannon
        
        bullets.append(Bullet(bullet_x, bullet_y, bullet_z, player_angle))
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = (camera_mode + 1) % 2


def idle():
    global cheat_rotation, player_angle, bullets, player_pos, game_over, frame_count, last_bullet_frame
    
    if game_over:
        glutPostRedisplay()
        return
    frame_count += 1

    if cheat_mode:
        # Continuous rotation
        cheat_rotation = (cheat_rotation + CHEAT_ROTATION_SPEED) % 360
        player_angle = cheat_rotation
        
        # Auto-aim at nearest enemy
        if auto_aim and enemies:
            closest_enemy = None
            min_angle_diff = 180
            for enemy in enemies:
                dx = enemy.x - player_pos[0]
                dy = enemy.y - player_pos[1]
                angle_to_enemy = math.degrees(math.atan2(dy, dx))
                angle_diff = abs((player_angle - angle_to_enemy + 180) % 360 - 180)
                
                if angle_diff < min_angle_diff:
                    min_angle_diff = angle_diff
                    closest_enemy = enemy
            
            # Snap to enemy if within threshold
            if closest_enemy and min_angle_diff < AUTO_AIM_ANGLE_THRESHOLD:
                dx = closest_enemy.x - player_pos[0]
                dy = closest_enemy.y - player_pos[1]
                player_angle = math.degrees(math.atan2(dy, dx))
        
        # Auto-fire bullets
        
        if frame_count - last_bullet_frame >= CHEAT_BULLET_INTERVAL / 16:  # Assuming ~60fps
            bullet_x = player_pos[0] + 70 * math.cos(math.radians(player_angle))
            bullet_y = player_pos[1] + 70 * math.sin(math.radians(player_angle))
            bullet_z = player_pos[2] + 25
            bullets.append(Bullet(bullet_x, bullet_y, bullet_z, player_angle))
            last_bullet_frame = frame_count
    
    glutPostRedisplay()


def showScreen():
    

    global game_over  
    
    
    if not game_over and (lives <= 0 or missed >= 10):
        game_over = True


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setup_camera()
    draw_grid()
    draw_player()

    if not game_over:
      draw_enemies()   

    draw_bullets()
    draw_grid_borders()

    draw_text(10, 770, f"Score: {score}")
    draw_text(10, 740, f"Lives: {lives}  Missed: {missed}")
    if cheat_mode:
        draw_text(10, 710, "CHEAT MODE ACTIVE")
        if auto_aim:
            draw_text(10, 680, "AUTO AIM: ON") 
    if lives <= 0 or missed >= 10:
        draw_text(400, 400, "Game Over! Press 'R' to restart.")

    glutSwapBuffers()


def draw_grid_borders():
    border_height = 100  
    border_thickness = 30  

    glBegin(GL_QUADS)
    
    # North wall (Blue)
    glColor3f(0, 0, 1)
    # Bottom edge
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    # Top edge
    glVertex3f(GRID_LENGTH, GRID_LENGTH, border_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, border_height)

    # South wall (Green)
    glColor3f(0, 1, 0)
    # Bottom edge
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    # Top edge
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, border_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, border_height)

    # West wall (Blue)
    glColor3f(0, 0, 1)
    # Bottom edge
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # Top edge
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, border_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, border_height)

    # East wall (Green)
    glColor3f(0, 1, 0)
    # Bottom edge
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    # Top edge
    glVertex3f(GRID_LENGTH, GRID_LENGTH, border_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, border_height)

    glEnd()


def reset_game():
    global bullets, enemies, score, lives, missed, player_pos, player_angle, game_over,frame_count
    bullets.clear()
    enemies.clear()
    for _ in range(ENEMY_COUNT):
        enemies.append(Enemy())
    score = 0
    lives = 5
    missed = 0
    player_pos = [0, 0, 60]
    player_angle = 0
    game_over = False  # Reset game 
    frame_count = 0  # Reset frame count for cheat mode bullet firing


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy - CSE423")
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    reset_game()
    glutMainLoop()


if __name__ == "__main__":
    main()