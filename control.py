# Using pynput lib to develop the keylogger features

# To import many objects from a lib, they need to be differentiated to avoid conflicts
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController

# to move the mouse pointer
def controlMouse():
    mouse = MouseController()

    # The position (0,0) is the upper-left corner of the screen.
    # Move (x pixels to the right, y pixels down)
    mouse.position = (1000,600)

    # Click with the left button
    # First the button name, second the number of clicks
    mouse.click(Button.left,1)

# to type with de keyboard
def controlKeyboard():
    keyboard = KeyboardController()

   # Types with the keyboard on the current line
    keyboard.type("Hello World!")

# this code will type in the next lines of the file
controlMouse()
controlKeyboard()


