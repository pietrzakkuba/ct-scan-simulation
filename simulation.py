import matplotlib.pyplot as plt
import math
import pydicom as dcm
from pydicom.dataset import Dataset, FileDataset
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

    def calcBresenham(self, width, height, img):
        sum = 0
        line = list(bresenham(self.emitter.x, self.emitter.y, self.detector.x, self.detector.y))
        for pixel in line:
            xpixel, ypixel = pixel
            xpixel += width // 2
            ypixel += height // 2
            if 0 < xpixel < width and 0 < ypixel < height:
                sum += img[ypixel][xpixel]
        return sum

    def drawBresenham(self, rimg, sinogramval, width, height):
        line = list(bresenham(self.emitter.x, self.emitter.y, self.detector.x, self.detector.y))
        for pixel in line:
            xpixel, ypixel = pixel
            xpixel += width // 2
            ypixel += height // 2
            if 0 < xpixel < width and 0 < ypixel < height:
                rimg[ypixel][xpixel] += sinogramval

    def update(self, phase, r, l, n):
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


def read_file(path, is_dicom=False):
    if not is_dicom:
        img = mpimg.imread(path)
        img = rgb2gray(img)
    else:
        dataset = dcm.dcmread(path)
        dataset.file_meta.TransferSyntaxUID = dcm.uid.ImplicitVRLittleEndian
        img = dataset.pixel_array
    return img


def radon(img, step, n, l):
    l = math.radians(l)
    height, width = img.shape[:2]
    r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)  # obliczanie promienia okregu
    alpha = list(np.linspace(0., 180., int(180. / step), endpoint=False))
    alpha = list(map(lambda x: math.radians(x), alpha))
    chords = [Chord(i) for i in range(n)]
    sinogram = [[0 for i in range(n)] for j in range(len(alpha))]
    for i in range(len(alpha)):
        for j in range(len(chords)):
            chords[j].update(alpha[i], r, l, n)
            sinogram[i][j] = chords[j].calcBresenham(width, height, img)
    sinogram=normalize2(sinogram)

    sinogram_resized = cv2.resize(np.float32(sinogram), (width, height), interpolation=cv2.INTER_LINEAR)
    return sinogram, sinogram_resized, alpha, r, l, height, width


def iradon(img, sinogram, alpha, r, n, l, height, width):        
    rimg = img
    rimg.fill(0)

    rChords = [Chord(i) for i in range(n)]
    for i in range(len(alpha)):
        for j in range(len(rChords)):
            rChords[j].update(alpha[i], r, l, n)
            rChords[j].drawBresenham(rimg, sinogram[i][j], width, height)

    rimg=normalize2(rimg)
    return rimg


def write_dicom_file(filename, image, name=None, sex=None, age=None, date=None, comment=None):
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"
        
        ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        ds.PixelData = image
        ds.PatientName = name
        ds.PatientSex = sex
        ds.PatientAge = age
        ds.StudyDate = date
        # TODO 
        ds.BitsAllocated = None
        ds.Rows = None
        ds.Columms = None
        ds.PixelRepresentation = None
        ds.SamplesPerPixel = None
        ds.PhotometricInterpretation = None
        # TODO
        ds.is_little_endian = True
        ds.is_implicit_VR = True
        print(ds)
        
        ds.save_as(filename)
