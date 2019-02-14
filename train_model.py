import numpy as np
import alexnet as alexnet

WIDTH = 80
HEIGHT = 60
OUTPUTS = 32
LR = 0.005
EPOCH = 8
MODEL_NAME = 'csgo-large_half_shooting-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCH)
print(MODEL_NAME)
model = alexnet.alexnet(WIDTH, HEIGHT, LR, OUTPUTS)

train_data = np.load('large_formatted_half_shooting.npy')
# print(train_data)

# ~20% of data
train = train_data[:-1000]
test = train_data[-1000:]



X = np.asarray([np.array(i[0]).flatten() for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = np.asarray([i[1] for i in train])
test_x = np.asarray([np.array(i[0]).flatten() for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_y = np.asarray([i[1] for i in test])

# X = np.array(i[0] for i in train).reshape(-1, WIDTH, HEIGHT, 1)
# Y = np.array(i[1] for i in train)
# test_x = np.array(i[0] for i in test).reshape(-1, WIDTH, HEIGHT, 1)
# test_y = np.array(i[1] for i in test)

model.fit(X, Y, n_epoch=EPOCH, validation_set=(test_x, test_y),
          snapshot_step=1000, show_metric=True, run_id=MODEL_NAME)

# tensorboard --logdir=foo:C:/Users/Aviox/PycharmProjects/CSGO/log

model.save(MODEL_NAME)
