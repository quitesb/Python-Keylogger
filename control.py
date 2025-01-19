from pynput.mouse import Controller

def controlmouse():
    mouse = Controller()
    
    mouse.position = (10, 20)


controlmouse()
