from directkeys import PressKey, ReleaseKey, KEYS, W
from pynput.mouse import Controller
import time

INPUT_STR = ['w', 'a', 's', 'd', 'shift', '1', '2', '3', '4', '5', 'alt', 'ctrl', 'b', 'f1', 'e', 'q', 'r']
key_is_pressed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                      False, False, False]
mouse_is_pressed = False
mouse_change = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
mouse = Controller()

inputs = []

for i in range(17):
    inputs.append(0)

inputs[0] = 1

def forward():
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)

def scroll_up():
    mouse.scroll(0, 1)

def scroll_down():
    mouse.scroll(0, -1)


def mouse_play(mouse_is_pressed, change):

    dx = 0
    dy = 0

    if change[1]:
        scroll_up()
        print('Scrolling up')
    if change[2]:
        scroll_down()
        print('Scrolling down')

    if change[3]:
        dx = 1
    elif change[4]:
        dx = 15
    elif change[5]:
        dx = 50
    elif change[6]:
        dx = -50
    elif change[7]:
        dx = -15
    elif change[8]:
        dx = -1

    if change[9]:
        dy = 1
    elif change[10]:
        dy = 15
    elif change[11]:
        dy = 50
    elif change[12]:
        dy = -50
    elif change[13]:
        dy = -15
    elif change[14]:
        dy = -1

    mouse.move(dx, dy)

    # click
    if change[0]:
        if mouse_is_pressed:
            mouse.release()
            print('Stopping firing')
            return False
        else:
            mouse.press()
            print('Firing')
            return True

def keyboard_play(key_is_pressed, change):
    for i in range(len(change)):
        if change[i]:
            if key_is_pressed[i]:
                print('Released {}'.format(INPUT_STR[i]))
                ReleaseKey(KEYS[i])
                key_is_pressed[i] = not key_is_pressed[i]
            else:
                print('Pressed: {} | SCANCODE: {}'.format(INPUT_STR[i], KEYS[i]))
                PressKey(KEYS[i])
                key_is_pressed[i] = not key_is_pressed[i]


if __name__ == '__main__':
    for i in list(range(3))[::-1]:
        print(i + 1)
        time.sleep(1)
    forward()
    # keyboard_play(key_is_pressed, inputs)
    mouse_play(mouse_is_pressed, mouse_change)
    time.sleep(1)
    mouse_play(mouse_is_pressed, mouse_change)
