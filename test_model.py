import cv2
import time
from grabscreen import grab_screen
import numpy as np
from alexnet import alexnet
from directkeys import PressKey, ReleaseKey, KEYS
from pynput.mouse import Controller
import keyboard

WIDTH = 80
HEIGHT = 60
OUTPUTS = 32
LR = 0.005
EPOCH = 5
MODEL_NAME = 'pycsgo_test_data-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCH)
INPUT_STR = ['w','a','s','d','shift','1','2','3','4','5','alt','ctrl','b','f1','e','q','r']

model = alexnet(WIDTH, HEIGHT, LR, OUTPUTS)
model.load(MODEL_NAME)
inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mouse = Controller()
#lets order the outputs as: m1, s_up, s_down, keystroke[0], keystroke[1], ... , keystroke[16], is_mouse_dx > 1, ...

def define_screen():
    screen = grab_screen(region=(0, 40, 800, 600))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    return screen

def check_chages(moves, old_moves):
    for i in range(3, 22):
            if moves[i] != old_moves[i]:
                change(i, moves[i])

def change(input_to_change, change_to):
    inputs[input_to_change] = change_to

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

    return mouse_is_pressed

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
    # given 4 seconds to get into game
    for i in list(range(3))[::-1]:
        print(i + 1)
        time.sleep(1)

    # PressKey(KEYS[0])
    # time.sleep(1)
    # ReleaseKey(KEYS[0])

    old_moves = inputs
    mouse_is_pressed = False
    key_is_pressed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                      False, False, False]
    last_time = time.time()

    while (True):
        screen = define_screen()
        prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
        moves = list(np.around(prediction))
        check_chages(moves, old_moves)
        old_moves = moves

        mouse_change_bools = [inputs[0], inputs[1], inputs[2], inputs[20], inputs[21], inputs[22], inputs[23],
                              inputs[24], inputs[25], inputs[26], inputs[27], inputs[28], inputs[29], inputs[30],
                              inputs[31]]
        keyboard_chage_bools = inputs[3:20]

        mouse_is_pressed = mouse_play(mouse_is_pressed, mouse_change_bools)
        # keyboard_play(key_is_pressed, keyboard_chage_bools)
        print(prediction)