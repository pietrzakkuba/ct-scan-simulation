import matplotlib.pyplot as plt
import math
import pydicom
import numpy as np
from bresenham import bresenham
import matplotlib.image as mpimg

class Position:
    def updateEmitter(self):
        self.x = r * math.cos(alpha)
        self.y = r * math.sin(alpha)

    def updateDetector(self, i, r, alpha):
        self.x = r * math.cos(alpha + math.pi - l / 2 + i * l / (n - 1))
        self.y = r * math.sin(alpha + math.pi - l / 2 + i * l / (n - 1))


step = 10   #krok
n = 5       #liczba detektorow
l = 30      #rozpietosc, pewnie trzeba ogarnac zeby bylo w radianach
alpha = 0   #kat ustawienia emitera, tez pewnie trzeba radiany

img = mpimg.imread("test/CT_ScoutView.jpg")
plt.imshow(img, cmap='gray')
plt.show()

height, width = img.shape
r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)    #obliczanie promienia okregu

emitter = Position()
detectors = [Position() for i in range(n)]

# for i in range(180 // step):
#     alpha = i * step    #aktualizacja biezacej pozycji emitera
#     emitter.updateEmitter()
#     for j in range(len(detectors)):
#         detectors[j].updateDetector(j, r, alpha)    #aktualizacja pozycji detektorow
#         #tu obliczenia emiter-detektor i do sinogramu
print(bresenham(-1,-4,3,2))