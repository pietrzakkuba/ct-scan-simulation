from tkinter import *
from tkinter import filedialog
import pydicom as dcm
import matplotlib.pyplot as plt
import simulation as sim
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from PIL import ImageTk, Image


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("CT Scan Simualation")
        self.wm_iconbitmap('gui/icon.ico')
        StartFrame(self).pack() 

class LoadedImageFrame(Frame):
    def __init__(self, master, path_to_file, is_dicom, step, emitters_detectors, _range):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors= emitters_detectors
        self._range = _range     
        self.image = sim.read_file(path_to_file, is_dicom)
        self.f_image = Figure(figsize=(5, 5), dpi=100)
        self.a_image = self.f_image.add_subplot(111)
        self.a_image.imshow(self.image, cmap='gray')
        self.canvas = FigureCanvasTkAgg(self.f_image, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.goBackButton()
        
        
    def goBack(self):
        self.destroy()
        MainFrame(self.master, self.path_to_file, self.step, self.emitters_detectors, self._range).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).pack()
        
class StartFrame(Frame):
    def __init__(self, master, path_to_file=''):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.selectLabel()
        self.selectEntry()
        self.selectButton()
        self.stepLabel()
        self.stepScale()
        self.emittersDetectorsLabel()
        self.emittersDetectorsScale()
        self.rangeLabel()
        self.rangeScale()
        self.examineButton()

        
    def selectLabel(self):
        self.select_label = Label(self, text='Select file:')
        self.select_label.grid(row=0, column=0, sticky='E', padx=10, pady=20)

    def selectEntry(self):
        self.select_entry = Entry(self, width=50)
        self.select_entry.insert(INSERT, self.path_to_file)
        self.select_entry.grid(row=0, column=1, padx=10, pady=10)

    def selectButton(self):
        self.select_button = Button(self, text='Browse files', command=self.fileDialog)
        self.select_button.grid(row=0, column=2, padx=10, pady=10)

    def fileDialog(self):
        self.path_to_file = filedialog.askopenfilename(initialdir='/', title='Select a file', filetype = (('All files', '*.*'), ('DICOM', '*.dcm'), ('JPEG', '*.jpg'), ('PNG', '*.png')))
        self.select_entry.delete(0, 'end')
        self.select_entry.insert(INSERT, self.path_to_file)

    def stepLabel(self):
        self.step_label = Label(self, text='Set step [degrees]')
        self.step_label.grid(row=1, column=0, sticky='E', padx=10, pady=10)
    
    def stepScale(self):
        self.step_scale_interval = lambda value : self.step_scale.config(label=(int(value) / 10))
        self.step_scale = Scale(self, from_=1, to=100, length=400, orient=HORIZONTAL, showvalue=False, command=self.step_scale_interval)
        self.step_scale.set(10)
        self.step_scale.grid(row=1, column=1, columnspan=2, padx=10, pady=10) 

    def emittersDetectorsLabel(self):
        self.emitters_detectors_label = Label(self, text='Set number of detectors')
        self.emitters_detectors_label.grid(row=2, column=0, sticky='E', padx=10, pady=10)

    def emittersDetectorsScale(self):
        self.emitters_detectors_interval = lambda value : self.emitters_detectors_scale.config(label=(int(value) * 2 + 1))
        self.emitters_detectors_scale = Scale(self, from_=1, to=150, length=400, orient=HORIZONTAL, showvalue=False, command=self.emitters_detectors_interval)
        self.emitters_detectors_scale.set(25)
        self.emitters_detectors_scale.grid(row=2, column=1, columnspan=2, padx=10, pady=10) 

    def rangeLabel(self):
        self.range_label = Label(self, text='Set range of the detectors-emitters set [degreess]')
        self.range_label.grid(row=3, column=0, sticky='E', padx=10, pady=10)

    def rangeScale(self):
        self.range_interval = lambda value : self.range_scale.config(label=int(value))
        self.range_scale = Scale(self, from_=1, to=180, length=400, orient=HORIZONTAL, showvalue=False, command=self.range_interval)
        self.range_scale.set(180)
        self.range_scale.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    def calculate(self):
        self.path_to_file = self.select_entry.get()
        self.step = self.step_scale.get() / 10
        self.emitters_detectors = self.emitters_detectors_scale.get() * 2 + 1
        self._range = self.range_scale.get()
        self.destroy()
        MainFrame(self.master, self.path_to_file, self.step, self.emitters_detectors, self._range).pack()


    def examineButton(self):
        self.examine_button = Button(self, text='Examine', command=self.calculate)
        self.examine_button.grid(row=4, column=1, padx=10, pady=20)

class MainFrame(Frame):
    def __init__(self, master, path_to_file, step, emitters_detectors, _range):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors = emitters_detectors
        self.range = _range
        if self.path_to_file.split('.')[-1] == 'dcm':
            self.is_dicom = True
        else:
            self.is_dicom = False

        self.showLoadedImageButton()
        self.backButton()
        self.generateSinogramButton()
        self.patientInfo()

    def showLoadedImage(self):
        self.destroy()
        LoadedImageFrame(self.master, self.path_to_file, self.is_dicom, self.step, self.emitters_detectors, self.range).pack()

    def showLoadedImageButton(self):
        self.loaded_image_button = Button(self, text='Show loaded image', command=self.showLoadedImage)
        self.loaded_image_button.grid(row=0, column=0, padx=0, pady=0)       
        

    def back(self):
        self.destroy()
        StartFrame(self.master, self.path_to_file).pack()
        
    def backButton(self):
        self.back_button = Button(self, text='Back', command=self.back)
        self.back_button.grid(row=1, column=0, padx=10, pady=10)

    def generateSinogram(self):
        self.image = sim.read_file(self.path_to_file, self.is_dicom)
        self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width = sim.radon(self.image, self.step, self.emitters_detectors, self.range)
        self.f_sinogram = Figure(figsize=(3, 3), dpi=100)
        self.a_sinogram = self.f_sinogram.add_subplot(111)
        self.a_sinogram.imshow(self.sinogram_resized, cmap='gray')
        self.canvas_sinogram = FigureCanvasTkAgg(self.f_sinogram, self)
        self.canvas_sinogram.draw()
        self.canvas_sinogram.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)

    def generateSinogramButton(self):
        self.calculate_sinogram_button = Button(self, text='Calculate', command=self.calculate)
        self.calculate_sinogram_button.grid(row=2, column=0, padx=10, pady=10)
        
    def patientInfo(self):
        self.about_label = Label(self, text='About Patient')
        self.about_label.grid(row=0, column=3, padx=10, pady=10) 
        
        self.name_label = Label(self, text='Name:')
        self.name_label.grid(row=1, column=2, padx=10, pady=10, sticky='E')
        self.sex_label = Label(self, text='Sex:')
        self.sex_label.grid(row=2, column=2, padx=10, pady=10, sticky='E')
        self.age_label = Label(self, text='Age:')
        self.age_label.grid(row=3, column=2, padx=10, pady=10, sticky='E')
        self.date_label = Label(self, text='Study date:')
        self.date_label.grid(row=4, column=2, padx=10, pady=10, sticky='E')
        self.comment_label = Label(self, text='Comment:')
        self.comment_label.grid(row=5, column=2, padx=10, pady=10, sticky='E')
        
        self.name_entry = Entry(self, width=50)
        self.name_entry.grid(row=1, column=3, padx=10, pady=10, sticky='W')
        self.sex_entry = Entry(self, width=50)
        self.sex_entry.grid(row=2, column=3, padx=10, pady=10, sticky='W')
        self.age_entry = Entry(self, width=10)
        self.age_entry.grid(row=3, column=3, padx=10, pady=10, sticky='W')
        self.date_entry = Entry(self, width=50)
        self.date_entry.grid(row=4, column=3, padx=10, pady=10, sticky='W')
        self.comment_entry = Text(self, width=50, height=10)
        self.comment_entry.grid(row=5, column=3, padx=10, pady=10, sticky='W')

            
            
      

root = App()
root.mainloop()
