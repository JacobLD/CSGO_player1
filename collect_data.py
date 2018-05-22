
import numpy as np
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from getkeys import key_check
import os
from grabscreen import grab_screen
from pynput import mouse

MOUSE_COLLECTION_TIME = 0.05
mouse_data = []
starting_mouse_pos = mouse.Controller.position

file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print("File exists, loading previous data")
    training_data = list(np.load(file_name))
else:
    print('File does not exits, starting fresh')
    training_data = []

def get_mouse_change_vector():
    current_mouse_pos = mouse.Controller.position
    return_vector = [current_mouse_pos[0] - starting_mouse_pos[0], current_mouse_pos[1] - starting_mouse_pos[1]]
    starting_mouse_pos = current_mouse_pos
    return return_vector





def main():
    #given 4 seconds to get into game
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    while (True):
        screen = grab_screen(region=(0, 40, 800, 600))
        #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        #screen = cv2.resize(screen, (80,60))

        get_mouse_xy()
        training_data.append([screen, mouse_data])
        print('mouse data: {}'.format(mouse_data))

        cv2.imshow('csgo', screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if len(training_data) % 500 == 0:
            print('500 data points in {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            print(len(training_data))
            np.save(file_name, training_data)

main()

#helper functions

