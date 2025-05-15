# Zombie-Attack-Survival
A OpenGL Based 3D game 


# Zombie Survival Game

![Game Screenshot](screenshot.png) *(Upload a screenshot and replace this text)*

A 3D first-person shooter survival game built with Python, PyOpenGL, and GLUT. Battle waves of zombies in a post-apocalyptic environment with dynamic camera controls and procedural terrain.

## Features

- 🎮 **Dual Camera Modes**
  - Follow cam (3rd person)
  - Free-fly cam (overhead view)
- 🧟 **Tiered Enemy System**
  - Regular zombies (1 HP)
  - Elite zombies (2 HP, 10% spawn chance)
- 🌳 **Procedural Environment**
  - Grid-based terrain with safe/danger zones
  - Animated trees and abandoned buildings
- 🔫 **Weapon System**
  - Cannon with limited ammo
  - Bullet physics with boundary checks
- ⚙️ **Game State Management**
  - Round progression system
  - Score tracking
  - Lives system

## Installation

1. **Prerequisites**
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate glut```

Controls
Key	Action
WASD	Move player
Mouse Left	Fire cannon
Mouse Right	Toggle camera mode
Arrow Keys	Move free camera (overhead)
P	Pause game
R	Restart game
N	Add 10 bullets (cheat code)
Technical Details
Engine: OpenGL immediate mode rendering

Physics: Frame-based movement calculations

AI: Simple pathfinding (move toward player)

Rendering:

Depth-tested 3D objects

Alpha blending for transparency

Matrix transformations for entities

Folder Structure

```
├── Sec10_22101877-24141160-24141181_Spring2025.py  # Main game file
├── README.md                                       # This file
└── screenshot.png                                  # Game screenshot 
```


Future Improvements
Add texture mapping

Implement sound effects

Add particle systems

Optimize with vertex buffers

Created for educational purposes - Adapt and modify freely!


### Recommended Additions:
1. **Actual Screenshot**:
   - Take an in-game screenshot
   - Save as `screenshot.png` in repo root

2. **License File**:
   - Add a `LICENSE` file (MIT recommended for educational projects)

3. **Demo Video** (Optional):
   - Record gameplay and upload to YouTube
   - Add link under features section

This README highlights your game's technical merits while being accessible to both players and developers. The markdown formatting will render beautifully on GitHub.
