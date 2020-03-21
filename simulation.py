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
            xpixel += round(width / 2)
            ypixel += round(height / 2)
            if 0 < xpixel < width and 0 < ypixel < height:
                sum += img[ypixel][xpixel]
        return sum

    def drawBresenham(self, rimg, sinogramval, width, height):
        line = list(bresenham(self.emitter.x, self.emitter.y, self.detector.x, self.detector.y))
        for pixel in line:
            xpixel, ypixel = pixel
            xpixel += round(width / 2)
            ypixel += round(height / 2)
            if 0 < xpixel < width and 0 < ypixel < height:
                rimg[ypixel][xpixel] += sinogramval
        return rimg

    def update(self, phase, r, l, n):
        self.emitter.x = round(r * math.cos(phase + l / 2 - self.id * l / n))
        self.emitter.y = round(r * math.sin(phase + l / 2 - self.id * l / n))
        self.detector.x = round(r * math.cos(phase + math.pi - l / 2 + self.id * l / n))
        self.detector.y = round(r * math.sin(phase + math.pi - l / 2 + self.id * l / n))


def normalize(image): #do wywalenia - 2 lepsze
    maximum = max(map(lambda x: max(x), image))
    for i in range(len(image)):
        image[i] = image[i] / maximum
    return image



def normalize2(image):
    return image / max(map(lambda x: max(x), image))

def createFilter(n):
    filtertab = []
    tab = [i for i in range(-n, n+1)]
    for i in tab:
        if i % 2:
            filtertab.append((-4 / (math.pi ** 2)) / (i ** 2))
        else:
            filtertab.append(0)
    filtertab[n]=1
    return filtertab

def applyFilter(sinogram, n):
    new_sinogram = []
    filterb = createFilter(n)
    for x in sinogram:
        new_sinogram.append(np.convolve(x, filterb, 'same'))
    return new_sinogram

def read_file(path):
    if path.split('.')[-1] == 'dcm':
        dataset = dcm.dcmread(path)
        dataset.file_meta.TransferSyntaxUID = dcm.uid.ImplicitVRLittleEndian
        img = dataset.pixel_array
        name = dataset.PatientName
        sex = dataset.PatientSex
        age = dataset.PatientAge
        date = dataset.StudyDate
        comment = dataset.ImageComments
    else:
        img = mpimg.imread(path)
        img = rgb2gray(img)
        name = None
        sex = None
        age = None
        date = None
        comment = None
    return (img, name, sex, age, date, comment)


def radon(img, step, n, l):
    l = math.radians(l)
    height, width = img.shape[:2]
    r = math.ceil(math.sqrt((height ** 2 + width ** 2)) / 2)  # obliczanie promienia okregu
    alpha = list(np.linspace(0., 180., int(180. / step), endpoint=False))
    alpha = list(map(lambda x: math.radians(x), alpha))
    chords = [Chord(i) for i in range(n)]
    sinogram = [[0 for i in range(n)] for j in range(len(alpha))]
    sinogram_resized_list = list()
    for i in range(len(alpha)):
        for j in range(len(chords)):
            chords[j].update(alpha[i], r, l, n)
            sinogram[i][j] = chords[j].calcBresenham(width, height, img)
        sinogram_resized = cv2.resize(np.float32(sinogram), (width, height), interpolation=cv2.INTER_LINEAR)
        sinogram_resized_list.append(sinogram_resized)
    sinogram = normalize2(sinogram)
    return (sinogram, sinogram_resized_list, alpha, r, l, height, width)


def iradon(sinogram, alpha, r, n, l, height, width):        
    rimg = np.zeros((height, width))
    rChords = [Chord(i) for i in range(n)]
    rimg_list = list()
    sinogram = applyFilter(sinogram, 20)
    for i in range(len(alpha)):
        for j in range(len(rChords)):
            rChords[j].update(alpha[i], r, l, n)
            rimg = rChords[j].drawBresenham(rimg, sinogram[i][j], width, height)
        rimg_list.append(rimg.copy())
    return rimg_list


def write_dicom_file(filename, image, name=None, sex=None, age=None, date=None, comment=None):
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"
    image = (normalize2(image) * 256).astype('uint8')
    ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.PixelData = image
    ds.PatientName = name
    ds.PatientSex = sex
    ds.PatientAge = age
    ds.StudyDate = date
    ds.ImageComments = comment
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.Rows = image.shape[0]
    ds.Columns = image.shape[1]
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    
    ds.save_as(filename)
