import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pydicom
from bresenham import bresenham

img = mpimg.imread('shepp-logan.png')
plt.imshow(img, cmap='gray')
print(img.shape)
plt.show()