from tkinter import *
from tkinter import filedialog
import pydicom as dcm
import matplotlib.pyplot as plt
import simulation as sim
import matplotlib.pyplot as plt

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("CT Scan Simualation")
        self.wm_iconbitmap('gui/icon.ico')
        StartFrame(self).pack() 

class StartFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
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
        self.path_to_file = ''
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
            self.is_dicon = False

        self.showOriginalButton()
        self.calculateButton()


    def showOriginal(self):
        self.image = sim.read_file(self.path_to_file, self.is_dicon)
        plt.imshow(self.image, cmap="gray")
        plt.show()

    def showOriginalButton(self):
        self.show_original_button = Button(self, text='Show original picture', command=self.showOriginal)
        self.show_original_button.grid(row=0, column=0, padx=10, pady=10)

    def calculate(self):
        self.image = sim.read_file(self.path_to_file, self.is_dicon)
        self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width = sim.radon(self.image, self.step, self.emitters_detectors, self.range)
        sim.iradon(self.image, self.sinogram, self.alpha, self.r, self.emitters_detectors, self.l, self.height, self.width)

    def calculateButton(self):
        self.calculate_sinogram_button = Button(self, text='Calculate', command=self.calculate)
        self.calculate_sinogram_button.grid(row=1, column=0, padx=10, pady=10)
        

root = App()
root.mainloop()
