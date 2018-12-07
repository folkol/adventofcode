import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)
data = np.random.random((2, 2, 2))

np.meshgrid()
fig, ax = plt.subplots()

for i in range(len(data)):
    ax.cla()
    ax.imshow(data[i])
    ax.set_title("frame {}".format(i))
    # Note that using time.sleep does *not* work here!
    plt.pause(0.1)