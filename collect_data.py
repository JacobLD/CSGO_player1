
import numpy as np
import cv2
import time
import os
from grabscreen import grab_screen
from pynput.mouse import Controller
from pynput import mouse
import keyboard
from multiprocessing import Process, Manager

WINDOWED_GAME_WIDTH = 800
WINDOWED_GAME_HEIGHT = 600
mouse_controller = Controller()
starting_mouse_pos = mouse_controller.position
last_time = time.time()
file_name = 'csgo_large_data_2.npy'


def timer(j):
    for i in list(range(j))[::-1]:
        print(i + 1)
        time.sleep(1)

def set_up_file(file_name):
    if os.path.isfile(file_name):
        print("File exists, loading previous data")
        return list(np.load(file_name))
    else:
        print('File does not exits, starting fresh')
        return []

def get_mouse_change_vector(previous_mouse_pos, current_mouse_pos):
    return_vector = (current_mouse_pos[0] - previous_mouse_pos[0], current_mouse_pos[1] - previous_mouse_pos[1])
    return return_vector

def show_game_window(screen):
    cv2.imshow('csgo', screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

def collect_keystrokes(paused):
    # in the order of
    # w,a,s,d,shift,1,2,3,4,5,alt,ctrl,b,f1,e,q,r,space *SPACE ADDED
    keys = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    paused_holder = paused

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'w' is pressed
            keys[0] = 1
        if keyboard.is_pressed('a'):  # if key 'a' is pressed
            keys[1] = 1
        if keyboard.is_pressed('s'):  # if key 's' is pressed
            keys[2] = 1
        if keyboard.is_pressed('d'):  # if key 'd' is pressed
            keys[3] = 1
        if keyboard.is_pressed('shift'):  # if key 'shift' is pressed
            keys[4] = 1
        if keyboard.is_pressed('1'):  # if key '1' is pressed
            keys[5] = 1
        if keyboard.is_pressed('2'):  # if key '2' is pressed
            keys[6] = 1
        if keyboard.is_pressed('3'):  # if key '3' is pressed
            keys[7] = 1
        if keyboard.is_pressed('4'):  # if key '4' is pressed
            keys[8] = 1
        if keyboard.is_pressed('5'):  # if key '5' is pressed
            keys[9] = 1
        if keyboard.is_pressed('alt'):  # if key 'alt' is pressed
            keys[10] = 1
        if keyboard.is_pressed('ctrl'):  # if key 'ctrl' is pressed
            keys[11] = 1
        if keyboard.is_pressed('b'):  # if key 'b' is pressed
            keys[12] = 1
        if keyboard.is_pressed('f1'):  # if key 'f1' is pressed
            keys[13] = 1
        if keyboard.is_pressed('e'):  # if key 'e' is pressed
            keys[14] = 1
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            keys[15] = 1
        if keyboard.is_pressed('r'):  # if key 'r' is pressed
            keys[16] = 1
        if keyboard.is_pressed('space'):  # if key 'r' is pressed
            keys[17] = 1
        if keyboard.is_pressed('f2'):
            if paused_holder:
                paused_holder = False
                print('UNPAUSED')
                timer(3)
            else:
                paused_holder = True
                print('PAUSED')
                timer(3)

        else:
            pass
    except:
        print('Non-insightful key pressed')

    return keys, paused_holder

def get_mouse_clicks(mouse_click):

    def on_click(x, y, button, pressed):
        if pressed:
            mouse_click.click = 1
        else:
            mouse_click.click = 0

        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))

    def on_scroll(x, y, dx, dy):
        if dy < 0:
            mouse_click.scroll_down = 1
        else:
            mouse_click.scroll_up = 1

        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

def define_screen():
    #screen = grab_screen(region=(0, 40, WINDOWED_GAME_WIDTH, WINDOWED_GAME_HEIGHT))
    screen = grab_screen(region=(0, 40, 800, 600))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    return screen

def process_mouse_vector(vector):
    # [1, 15, 50, -50, -15, -1]
    mouse_x = [0,0,0,0,0,0]
    mouse_y = [0,0,0,0,0,0]

    x = vector[0]
    y = vector[1]

    if x > 50:
        mouse_x[2] = 1
    elif x > 15:
        mouse_x[1] = 1
    elif x > 1:
        mouse_x[0] = 1
    elif x < -50:
        mouse_x[3] = 1
    elif x < -15:
        mouse_x[4] = 1
    elif x < -1:
        mouse_x[5] = 1

    if y > 50:
        mouse_y[2] = 1
    elif y > 15:
        mouse_y[1] = 1
    elif y > 1:
        mouse_y[0] = 1
    elif y < -50:
        mouse_y[3] = 1
    elif y < -15:
        mouse_y[4] = 1
    elif y < -1:
        mouse_y[5] = 1

    return mouse_x, mouse_y

def main(mouse_click):
    timer(3)
    starting_mouse_pos = mouse_controller.position
    last_time = time.time()
    mouse_click.click = 0
    paused = False

    while (True):
        mouse_click.scroll_up = 0
        mouse_click.scroll_down = 0

        screen = define_screen()
        current_mouse_pos = mouse_controller.position
        mouse_data = get_mouse_change_vector(starting_mouse_pos, current_mouse_pos)
        starting_mouse_pos = current_mouse_pos

        mouse_data = process_mouse_vector(mouse_data)
        keystrokes, paused = collect_keystrokes(paused)

        if not paused:
            training_data.append([screen, keystrokes, mouse_click.click, mouse_click.scroll_up, mouse_click.scroll_down,
                                  mouse_data[0][0], mouse_data[0][1], mouse_data[0][2],
                                  mouse_data[0][3], mouse_data[0][4], mouse_data[0][5], mouse_data[1][0],
                                  mouse_data[1][1],
                                  mouse_data[1][2], mouse_data[1][3], mouse_data[1][4], mouse_data[1][5]])

            # show_game_window(screen)
            # save training data
            if len(training_data) % 500 == 0:
                print('{} data points in {} seconds'.format(len(training_data), time.time() - last_time))
                last_time = time.time()
                np.save(file_name, training_data)


if __name__ == '__main__':
    training_data = set_up_file(file_name)
    manager = Manager()
    mouse_click = manager.Namespace()

    mouse_process = Process(target=get_mouse_clicks, args=(mouse_click,))

    mouse_process.start()
    main(mouse_click)
