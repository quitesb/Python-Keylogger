from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener
import sys

def writefile(x,y):
    # after the movement, write in the file
    # used python 3.10.11 and pynput 1.7. 6 , as other versions may cause crash errors
    print('Position of current mouse: ({}, {})'.format(x, y))

# kill the mouse logger loop with x key if I need to , this usually dont be in a mouse logger
def kill(key):
    if  key.char == 'x':
        sys.exit()


# with to free memory
with Listener(on_move=writefile) as mouse_listener:
   # init the x key verification
    with KeyboardListener(on_press=kill) as keyboard_listener:
        keyboard_listener.join()