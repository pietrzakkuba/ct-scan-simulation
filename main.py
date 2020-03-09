import matplotlib.pyplot as plt
import math
import pydicom
import numpy as np
from bresenham import bresenham
import matplotlib.image as mpimg
from skimage.color import rgb2gray
import cv2

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0


class Chord:
    def __init__(self, id):
        self.emitter = Position()
        self.detector = Position()
        self.id = id

    def calcBresenham(self):
        sum = 0
        line = list(bresenham(self.emitter.x, self.emitter.y, self.detector.x, self.detector.y))
        for pixel in line:
            xpixel, ypixel = pixel
            xpixel += width // 2
            ypixel += height // 2
            if 0 < xpixel < width and 0 < ypixel < height:
                sum += img[ypixel][xpixel]
        return sum

    def update(self, phase):
        self.emitter.x = round(r * math.cos(phase + l / 2 - self.id * l / n))
        self.emitter.y = round(r * math.sin(phase + l / 2 - self.id * l / n))
        self.detector.x = round(r * math.cos(phase + math.pi - l / 2 + self.id * l / n))
        self.detector.y = round(r * math.sin(phase + math.pi - l / 2 + self.id * l / n))


def normalize(image):
    maximum = max(map(lambda x: max(x), image))
    for i in range(len(image)):
        image[i] = image[i] / maximum
    return image


def normalize2(image):
    maximum = max(map(lambda x: max(x), image))
    image = image / maximum
    return image


step = 2  # krok w stopniach
n = 101  # liczba detektorow
l = math.pi / 2  # rozpietosc

d = l / n  # przesuniecie fazowe miedzy emiterami/detektorami
# Kwadraty2

img = mpimg.imread("test/Kwadraty2.jpg")
img = rgb2gray(img)
plt.imshow(img, cmap='gray')
plt.show()

height, width = img.shape[:2]
r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)  # obliczanie promienia okregu

alpha = list(np.linspace(0., 180., int(180. / step), endpoint=False))
alpha = list(map(lambda x: math.radians(x), alpha))

chords = [Chord(i) for i in range(n)]

sinogram = [[0 for i in range(n)] for j in range(len(alpha))]

for i in range(len(alpha)):
    for j in range(len(chords)):
        chords[j].update(alpha[i])
        sinogram[i][j] = chords[j].calcBresenham()

sinogram=normalize2(sinogram)

maximum = max(map(lambda x: max(x), sinogram))
for i in range(len(sinogram)):
    sinogram[i] = sinogram[i] / maximum

plt.imshow(sinogram, cmap="gray")
plt.show()

sinogram_resized = cv2.resize(np.float32(sinogram), (width, height), interpolation=cv2.INTER_LINEAR)
plt.axis('off')
plt.imshow(sinogram_resized, cmap="gray")
plt.show()
