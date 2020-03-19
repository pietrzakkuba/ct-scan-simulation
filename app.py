from tkinter import *
from tkinter import filedialog
import pydicom as dcm
import matplotlib.pyplot as plt
import simulation as sim
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from PIL import ImageTk, Image
from datetime import date

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("CT Scan Simualation")
        self.wm_iconbitmap('gui/icon.ico')
        StartFrame(self).pack() 

class LoadedImageFrame(Frame):
    def __init__(self, master, path_to_file, is_dicom, step, emitters_detectors, _range,
                 sinogram=None, sinogram_resized=None, alpha=None, r=None, l=None, height=None, width=None, final_image=None,
                 name=None, sex=None, age=None, date=None, comment=None):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors= emitters_detectors
        self.range = _range
        self.sinogram = sinogram
        self.sinogram_resized = sinogram_resized
        self.alpha = alpha
        self.r = r
        self.l = l
        self.height = height
        self.width = width
        self.final_image = final_image
        self.name = name
        self.sex = sex
        self.age = age
        self.date = date
        self.comment = comment   
        self.image = sim.read_file(path_to_file, is_dicom)
        self.f_image = Figure(figsize=(6, 6), dpi=100)
        self.a_image = self.f_image.add_subplot(111)
        self.a_image.imshow(self.image, cmap='gray')
        self.canvas = FigureCanvasTkAgg(self.f_image, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.goBackButton()
        
        
    def goBack(self):
        self.destroy()
        MainFrame(self.master, self.path_to_file, self.step, self.emitters_detectors, self.range,
                  self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width, self.final_image,
                  self.name, self.sex, self.age, self.date, self.comment
                  ).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).pack()
        
class SinogramFrame(Frame):
    def __init__(self, master, path_to_file, is_dicom, step, emitters_detectors, _range, 
                 sinogram=None, sinogram_resized=None, alpha=None, r=None, l=None, height=None, width=None, final_image=None,
                 name=None, sex=None, age=None, date=None, comment=None):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors= emitters_detectors
        self.range = _range
        self.sinogram = sinogram
        self.sinogram_resized = sinogram_resized
        self.alpha = alpha
        self.r = r
        self.l = l
        self.height = height
        self.width = width
        self.final_image = final_image
        self.name = name
        self.sex = sex
        self.age = age
        self.date = date
        self.comment = comment
        self.f_sinogram = Figure(figsize=(6, 6), dpi=100)
        self.a_sinogram = self.f_sinogram.add_subplot(111)
        if sinogram_resized is None:
            self.image = sim.read_file(self.path_to_file, is_dicom)
            self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width = sim.radon(self.image, self.step, self.emitters_detectors, self.range)
            self.a_sinogram.imshow(self.sinogram_resized, cmap='gray')
            self.canvas_sinogram = FigureCanvasTkAgg(self.f_sinogram, self)
            self.canvas_sinogram.draw()
            self.canvas_sinogram.get_tk_widget().pack()
        else:
            self.sinogram_resized = sinogram_resized
            self.a_sinogram.imshow(self.sinogram_resized, cmap='gray')
            self.canvas_sinogram = FigureCanvasTkAgg(self.f_sinogram, self)
            self.canvas_sinogram.draw()
            self.canvas_sinogram.get_tk_widget().pack()
            
        self.goBackButton()
        
    def goBack(self):
        self.destroy()
        MainFrame(
                self.master, 
                self.path_to_file, 
                self.step, 
                self.emitters_detectors, 
                self.range, 
                self.sinogram, 
                self.sinogram_resized, 
                self.alpha, 
                self.r, 
                self.l, 
                self.height, 
                self.width,
                self.final_image,
                self.name, self.sex, self.age, self.date, self.comment
            ).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).pack()
        
class FinalImageFrame(Frame):
    def __init__(self, master, path_to_file, is_dicom, step, emitters_detectors, _range, 
                 sinogram, sinogram_resized, alpha, r, l, height, width, final_image,
                 name=None, sex=None, age=None, date=None, comment=None):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors= emitters_detectors
        self.range = _range
        self.sinogram = sinogram
        self.sinogram_resized = sinogram_resized
        self.alpha = alpha
        self.r = r
        self.l = l
        self.height = height
        self.width = width
        self.final_image = final_image
        self.name = name
        self.sex = sex
        self.age = age
        self.date = date
        self.comment = comment
        self.f_final_image = Figure(figsize=(6, 6), dpi=100)
        self.a_final_image = self.f_final_image.add_subplot(111)
        if self.final_image is None:
            self.image = sim.read_file(path_to_file, is_dicom)
            self.final_image = sim.iradon(self.image, self.sinogram, self.alpha, self.r, self.emitters_detectors, self.l, self.height, self.width)
            self.a_final_image.imshow(self.final_image, cmap='gray')
            self.canvas_final_image = FigureCanvasTkAgg(self.f_final_image, self)
            self.canvas_final_image.draw()
            self.canvas_final_image.get_tk_widget().pack()
        else:
            self.a_final_image.imshow(self.final_image, cmap='gray')
            self.canvas_final_image = FigureCanvasTkAgg(self.f_final_image, self)
            self.canvas_final_image.draw()
            self.canvas_final_image.get_tk_widget().pack()
        self.goBackButton()
        
    def goBack(self):
        self.destroy()
        MainFrame(self.master, self.path_to_file, self.step, self.emitters_detectors, self.range,
                  self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width, self.final_image,
                  self.name, self.sex, self.age, self.date, self.comment).pack()
        
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
        self.path_to_file = filedialog.askopenfilename(initialdir='.', title='Select a file', filetype = (('All files', '*.*'), ('DICOM', '*.dcm'), ('JPEG', '*.jpg'), ('PNG', '*.png')))
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
        self.emitters_detectors_interval = lambda value : self.emitters_detectors_scale.config(label=(int(value)))
        self.emitters_detectors_scale = Scale(self, from_=1, to=300, length=400, orient=HORIZONTAL, showvalue=False, command=self.emitters_detectors_interval)
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
    def __init__(self, master, path_to_file, step, emitters_detectors, _range, 
            sinogram=None, sinogram_resized=None,  alpha=None, r=None, l=None, height=None, width=None, final_image=None,
            name=None, sex=None, age=None, date=None, comment=None
                ):
        Frame.__init__(self, master)
        self.path_to_file = path_to_file
        self.step = step
        self.emitters_detectors = emitters_detectors
        self.range = _range
        self.sinogram = sinogram
        self.sinogram_resized = sinogram_resized
        self.final_image = final_image
        self.alpha = alpha
        self.r = r
        self.l = l
        self.height = height
        self.width = width
        self.final_image = final_image
        self.name = name
        self.sex = sex
        self.age = age
        self.date = date
        self.comment = comment
        self.patientInfo()
        if self.path_to_file.split('.')[-1] == 'dcm':
            self.is_dicom = True
        else:
            self.is_dicom = False

        self.showLoadedImageButton()
        self.backButton()
        self.generateSinogramButton()
        self.generateFinalImageButton()
        self.saveButton()
        self.setPatientInfo()

    def showLoadedImage(self):
        self.save()
        self.destroy()
        LoadedImageFrame(self.master, self.path_to_file, self.is_dicom, self.step, self.emitters_detectors, self.range,
                         self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width, self.final_image,
                         self.name, self.sex, self.age, self.date, self.comment
                         ).pack()

    def showLoadedImageButton(self):
        self.loaded_image_button = Button(self, text='Show loaded image', command=self.showLoadedImage)
        self.loaded_image_button.grid(row=1, column=0, padx=10, pady=10, sticky='W')       
        
    def back(self):
        self.destroy()
        StartFrame(self.master, self.path_to_file).pack()
        
    def backButton(self):
        self.back_button = Button(self, text='Back', command=self.back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='W')

    def generateSinogram(self):
        self.save()
        self.destroy()
        SinogramFrame(
            self.master, self.path_to_file, self.is_dicom, self.step, self.emitters_detectors, self.range, 
            self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width, self.final_image,
            self.name, self.sex, self.age, self.date, self.comment
            ).pack()

    def generateSinogramButton(self):
        if self.sinogram_resized is None:
            self.calculate_sinogram_button = Button(self, text='Generate sinogram', command=self.generateSinogram)
        else:
            self.calculate_sinogram_button = Button(self, text='Show sinogram', command=self.generateSinogram)
        self.calculate_sinogram_button.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        
    def generateFinalImage(self):
        self.save()
        self.destroy()
        FinalImageFrame(
            self.master, self.path_to_file, self.is_dicom, self.step, self.emitters_detectors, self.range,
            self.sinogram, self.sinogram_resized, self.alpha, self.r, self.l, self.height, self.width, self.final_image,
            self.name, self.sex, self.age, self.date, self.comment
                        ).pack()

    def generateFinalImageButton(self):
        if self.sinogram is None:
            self.calculate_final_image_button = Button(self, text='Generate final image', command=self.generateFinalImage, state='disabled')
        elif self.final_image is None:
            self.calculate_final_image_button = Button(self, text='Generate final image', command=self.generateFinalImage)
        else:
            self.calculate_final_image_button = Button(self, text='Show final image', command=self.generateFinalImage)
        self.calculate_final_image_button.grid(row=3, column=0, padx=10, pady=10, sticky='W')
        
        
    def today(self):
        self.date_entry.delete(1.0, END)
        self.date_entry.insert(END, str(date.today()))
        
    
    def patientInfo(self):
        self.about_label = Label(self, text='About Patient')
        self.about_label.grid(row=0, column=3, padx=10, pady=10, sticky='W') 
        
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
        
        self.name_entry = Text(self, width=40, height=1)
        self.name_entry.grid(row=1, column=3, padx=10, pady=10, sticky='W')
        self.sex_entry = Text(self, width=40, height=1)
        self.sex_entry.grid(row=2, column=3, padx=10, pady=10, sticky='W')
        self.age_entry = Text(self, width=10, height=1)
        self.age_entry.grid(row=3, column=3, padx=10, pady=10, sticky='W')
        self.date_entry = Text(self, width=30, height=1)
        self.date_entry.grid(row=4, column=3, padx=10, pady=10, sticky='W')
        self.date_button = Button(self, text='Today', command=self.today)
        self.date_button.grid(row=4, column=3, padx=10, pady=10, sticky='E')
        self.comment_entry = Text(self, width=40, height=10)
        self.comment_entry.grid(row=5, column=3, padx=10, pady=10, sticky='W')
        
    def setPatientInfo(self):
        self.patientInfo = []
        for item in [self.name, self.sex, self.age, self.date, self.comment]:
            if item is None:
                self.patientInfo.append('')
            else:
                self.patientInfo.append(item)
        self.name_entry.delete(1.0, END)
        self.sex_entry.delete(1.0, END)
        self.age_entry.delete(1.0, END)
        self.date_entry.delete(1.0, END)
        self.comment_entry.delete(1.0, END)
        self.name_entry.insert(END, self.patientInfo[0])
        self.sex_entry.insert(END, self.patientInfo[1])
        self.age_entry.insert(END, self.patientInfo[2])
        self.date_entry.insert(END, self.patientInfo[3])
        self.comment_entry.insert(END, self.patientInfo[4])

    def save(self):
        self.name = self.name_entry.get(1.0, END)[:-1]
        self.sex = self.sex_entry.get(1.0, END)[:-1]
        self.age = self.age_entry.get(1.0, END)[:-1]
        self.date = self.date_entry.get(1.0, END)[:-1]
        self.comment = self.comment_entry.get(1.0, END)[:-1]
        
    def saveDicom(self):
        self.save()
        self.file_to_save = filedialog.asksaveasfile(mode='w', defaultextension='.dcm').name
        sim.write_dicom_file(self.file_to_save, self.final_image, self.name, self.sex, self.age, self.date, self.comment)

        
        
        
    def saveButton(self):
        if self.final_image is None:
            save_button = Button(self, text='Save as DICOM', command=self.saveDicom, state='disabled')
        else:
            save_button = Button(self, text='Save as DICOM', command=self.saveDicom)
        save_button.grid(row=6, column=3, padx=10, pady=10, sticky='W')
      

root = App()
root.mainloop()
