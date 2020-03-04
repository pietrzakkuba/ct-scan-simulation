import matplotlib.pyplot as plt
import math
import pydicom
import numpy as np
from bresenham import bresenham
import matplotlib.image as mpimg


class Position:
    def updateEmitter(self, alpha):
        self.x = r * math.cos(alpha)
        self.y = r * math.sin(alpha)

    def updateDetector(self, i, r, alpha):
        self.x = r * math.cos(alpha + math.pi - l / 2 + i * l / (n - 1))
        self.y = r * math.sin(alpha + math.pi - l / 2 + i * l / (n - 1))


step = 0.25  # krok
n = 40  # liczba detektorow
l = math.radians(30)  # rozpietosc, pewnie trzeba ogarnac zeby bylo w radianach
alpha = 0  # kat ustawienia emitera, tez pewnie trzeba radiany

img = mpimg.imread("test/CT_ScoutView.jpg")
plt.imshow(img, cmap='gray')
plt.show()

height, width = img.shape[:2]
r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)  # obliczanie promienia okregu

alpha = np.linspace(0., 180., int(180. / step), endpoint=False)
alpha = [math.radians(alpha[i]) for i in range(len(alpha))]

emitter = Position()
detectors = [Position() for i in range(n)]

sinogram = [[0 for i in range(n)] for j in range(len(alpha))]

for i in range(len(alpha)):
    emitter.updateEmitter(alpha[i])
    for j in range(len(detectors)):
        detectors[j].updateDetector(j, r, alpha[i])  # aktualizacja pozycji detektorow
        line = list(bresenham(int(emitter.x), int(emitter.y), int(detectors[j].x), int(detectors[j].y)))
        for pixel in line:
            if 0 <= pixel[0] < width and 0 <= pixel[1] < height:  # tu mozliwe znowu, ze pixel[0] z pixel[1] podmienic
                sinogram[i][j] += img[pixel[0]][pixel[1]]

            # mozliwe ze pojebane sa wspolrzedne x z y, w sensie np. zamienic pixel[0] z pixel[1] itp, ale to wyjdzie w praniu

maximum = max(map(lambda x: max(x), sinogram))

for i in range(len(sinogram)):
    sinogram[i] = sinogram[i] / maximum

plt.imshow(sinogram, cmap="gray")
plt.show()
