import matplotlib.pyplot as plt
import math
import pydicom
import numpy as np
from bresenham import bresenham
import matplotlib.image as mpimg

class Position:
    def updateEmitter(self):
        self.x = int(r * math.cos(alpha))
        self.y = int(r * math.sin(alpha))

    def updateDetector(self, i, r, alpha):
        self.x = int(r * math.cos(alpha + math.pi - l / 2 + i * l / (n - 1)))
        self.y = int(r * math.sin(alpha + math.pi - l / 2 + i * l / (n - 1)))


step = 10   #krok
n = 5       #liczba detektorow
l = 30      #rozpietosc, pewnie trzeba ogarnac zeby bylo w radianach
alpha = 0   #kat ustawienia emitera, tez pewnie trzeba radiany

img = mpimg.imread("test/CT_ScoutView.jpg")
plt.imshow(img, cmap='gray')
plt.show()

height, width = img.shape[:2]
r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)    #obliczanie promienia okregu

emitter = Position()
detectors = [Position() for i in range(n)]

sinogram=[[0 for i in range(n)] for j in range(180//step)]

for i in range(180 // step):
    alpha = i * step    #aktualizacja biezacej pozycji emitera
    emitter.updateEmitter()
    for j in range(len(detectors)):
        detectors[j].updateDetector(j, r, alpha)    #aktualizacja pozycji detektorow
        line=list(bresenham(emitter.x, emitter.y, detectors[j].x, detectors[j].y))
        for pixel in line:
            sinogram[i][j]+=img[pixel[0]][pixel[1]]

            #mozliwe ze pojebane sa wspolrzedne x z y, w sensie np. zamienic pixel[0] z pixel[1] itp, ale to wyjdzie w praniu

print(sinogram)

maximum=0
for x in sinogram:
    if max(x)>maximum:
        maximum=max(x)

for i in range(len(sinogram)):
    sinogram[i]=sinogram[i]/maximum

print(sinogram[1])