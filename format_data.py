import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data_1 = np.load('csgo_large_data.npy')
train_data_2 = np.load('csgo_large_data_2.npy')

train_data = []

for data in train_data_1:
    train_data.append(data)

for data in train_data_2:
    train_data.append(data)



df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[3].apply(str)))
final_data = []

#lets order the outputs as: dx, dy, m1, s_up, s_down, keystroke[0], keystroke[1], ... , keystroke[n]
for data in train_data:
    img = data[0]
    keystrokes = data[1]
    m1 = data[2]
    scroll_up = data[3]
    scroll_down = data[4]

    actions = [m1, scroll_up, scroll_down, keystrokes[0], keystrokes[1], keystrokes[2],
                    keystrokes[3], keystrokes[4], keystrokes[5], keystrokes[6], keystrokes[7], keystrokes[8],
                    keystrokes[9], keystrokes[10], keystrokes[11], keystrokes[12], keystrokes[13], keystrokes[14],
                    keystrokes[15], keystrokes[16], keystrokes[17], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                    data[12], data[13], data[14], data[15], data[16]]

    if m1:
        final_data.append([img, actions])
        print(len(final_data))

number_of_m1 = len(final_data)

for data in train_data:
    img = data[0]
    keystrokes = data[1]
    m1 = data[2]
    scroll_up = data[3]
    scroll_down = data[4]

    actions = [m1, scroll_up, scroll_down, keystrokes[0], keystrokes[1], keystrokes[2],
                    keystrokes[3], keystrokes[4], keystrokes[5], keystrokes[6], keystrokes[7], keystrokes[8],
                    keystrokes[9], keystrokes[10], keystrokes[11], keystrokes[12], keystrokes[13], keystrokes[14],
                    keystrokes[15], keystrokes[16], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                    data[12], data[13], data[14], data[15], data[16]]

    if not m1:
        final_data.append([img, actions])
        print(len(final_data))

    if len(final_data) > 2 * number_of_m1:
        break




shuffle(final_data)
np.save('large_formatted_half_shooting', final_data)



# for data in train_data:
#     img = data[0]
#     mouse_dx = data[1]
#     mouse_dy = data[2]
#     keystrokes = data[3]
#     m1 = data[4]
#     scroll_up = data[5]
#     scroll_down = data[6]
#
#     cv2.imshow('test', img)
#     print(keystrokes)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break

