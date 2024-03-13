## Rubik's Cube Simulator

This is a computer simulation of a Rubik's Cube, implemented in Python using Pygame and OpenGL. It allows users to interact with a virtual Rubik's Cube, rotating its layers using mouse clicks or keyboard inputs. 

### Features

- **Mouse Interaction**: Users can rotate the entire cube by clicking and dragging the mouse.
- **Keyboard Controls**: Various keyboard shortcuts are available for rotating specific layers of the cube, undoing moves, resetting the camera, shuffling the cube, and displaying help.
- **Animation**: Smooth animation is provided for cube rotations, enhancing the user experience.
- **Scrambling**: Users can shuffle the cube randomly for a new challenge.

### How to Use

- **Mouse Controls**:
  - Left-click and drag: Rotate the entire cube.
  - Right-click: Stop mouse rotation.

- **Keyboard Controls**:
  - **1 to 9**: Rotate layers of the cube clockwise.
  - **Q to O**: Rotate layers of the cube counterclockwise.
  - **Z**: Undo the last move.
  - **X**: Undo all moves.
  - **C**: Reset the camera.
  - **V**: Shuffle the cube.
  - **H**: Display help.

### Requirements

- Python 3.x
- Pygame
- PyOpenGL

### How to Run

1. Install Python (if not already installed).
2. Install Pygame and PyOpenGL using pip:
   ```
   pip install pygame PyOpenGL
   ```
3. Clone or download this repository.
4. Navigate to the directory containing the downloaded files.
5. Run the script `rubik.py` using Python:
   ```
   python rubik.py
   ```

### Autor

This project was created by Konrad Siemiątkowski. If you have any questions or suggestions, please feel free to contact me.
