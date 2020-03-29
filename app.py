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
        self.title("CT Scan Simulation")
        self.wm_iconbitmap('gui/icon.ico')
        self.path_to_file = ''
        self.step = None
        self.emitters_detectors = None
        self.range = None
        self.original_image = None
        self.sinogram = None
        self.sinogram_resized = list()
        self.final_image = list()
        self.final_image_filtered = list()
        self.final_image_rmse = list()
        self.final_image_filtered_rmse = list()
        self.alpha = None
        self.r = None
        self.l = None
        self.height = None
        self.width = None
        self.name = None
        self.sex = None
        self.age = None
        self.date = None
        self.comment = None
        self.check_variable = BooleanVar()
        self.check_variable.set(False)
        self.check_variable_save = BooleanVar()
        self.check_variable_save.set(False)
        StartFrame(self).pack() 

class LoadedImageFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.f_image = Figure(figsize=(6, 6), dpi=100)
        self.a_image = self.f_image.add_subplot(111)
        self.a_image.imshow(self.master.original_image, cmap='gray')
        self.canvas = FigureCanvasTkAgg(self.f_image, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.goBackButton()
        
    def goBack(self):
        self.destroy()
        MainFrame(self.master).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).pack()
        
class SinogramFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.f_sinogram = Figure(figsize=(6, 6), dpi=100)
        self.a_sinogram = self.f_sinogram.add_subplot(111)
        self.canvas_sinogram = FigureCanvasTkAgg(self.f_sinogram, self)
        self.image_widget = self.canvas_sinogram.get_tk_widget()
        if self.master.sinogram_resized == list():
            (
                self.master.sinogram, 
                self.master.sinogram_resized, 
                self.master.alpha, 
                self.master.r, 
                self.master.l, 
                self.master.height, 
                self.master.width
             ) = sim.radon(self.master.original_image, self.master.step, self.master.emitters_detectors, self.master.range)
        self.scale()
        self.showImage()
        self.goBackButton()
        self.setImageButton()
        
    def showImage(self):
        self.image_widget.grid_forget()
        self.step = int(self.scale.get() * (len(self.master.sinogram_resized) / 100)) - 1
        self.a_sinogram.imshow(self.master.sinogram_resized[self.step], cmap='gray')
        self.canvas_sinogram.draw()
        self.image_widget.grid(row=0, column=1)              
        
    
    def scale(self):
        self.scale = Scale(self, from_=1, to=100, length=600, orient=VERTICAL, showvalue=True)
        self.scale.set(100)
        self.scale.grid(row=0, column=0)
    
    def goBack(self):
        self.destroy()
        MainFrame(self.master).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).grid(row=1, column=1)
        
    def setImageButton(self):
        Button(self, text='Set progress', command=self.showImage).grid(row=1, column=0)
        
class FinalImageFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.f_final_image = Figure(figsize=(6, 6), dpi=100)
        self.a_final_image = self.f_final_image.add_subplot(111)
        self.canvas_final_image = FigureCanvasTkAgg(self.f_final_image, self)
        self.image_widget = self.canvas_final_image.get_tk_widget()
        if not self.master.check_variable.get():
            if not len(self.master.final_image):
                self.master.final_image, self.master.final_image_rmse = sim.iradon(
                    self.master.original_image,
                    self.master.sinogram,
                    self.master.alpha,
                    self.master.r,
                    self.master.emitters_detectors,
                    self.master.l,
                    self.master.height,
                    self.master.width,
                    False
                    )
            self.image = self.master.final_image
        else:
            if not len(self.master.final_image_filtered):
                self.master.final_image_filtered, self.master.final_image_filtered_rmse = sim.iradon(
                    self.master.original_image,
                    self.master.sinogram,
                    self.master.alpha,
                    self.master.r,
                    self.master.emitters_detectors,
                    self.master.l,
                    self.master.height,
                    self.master.width,
                    True
                    )
            self.image = self.master.final_image_filtered
        self.scaling()
        self.goBackButton()
        self.showImage()
        self.setImageButton()
        
        
    def scaling(self):
        self.scale = Scale(self, from_=1, to=100, length=600, orient=VERTICAL, showvalue=True)
        self.scale.set(100)
        self.scale.grid(row=0, column=0)


    def showImage(self):
        self.image_widget.grid_forget()
        self.step = int(self.scale.get() * (len(self.image) / 100)) - 1
        fixedImage=sim.fixNegative(self.image[self.step])
        self.a_final_image.imshow(fixedImage, cmap='gray')
        self.canvas_final_image.draw()
        self.image_widget.grid(row=0, column=1)  
        
    def goBack(self):
        self.destroy()
        MainFrame(self.master).pack()
        
    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).grid(row=1, column=1)
        
    def setImageButton(self):
        Button(self, text='Set progress', command=self.showImage).grid(row=1, column=0)
        
class RMSEFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.f_image = Figure(figsize=(6, 6), dpi=100)
        self.a_image = self.f_image.add_subplot(111)
        self.a_image.imshow(self.master.original_image, cmap='gray')
        print(self.master.final_image_rmse, self.master.final_image_filtered_rmse)
        self.canvas = FigureCanvasTkAgg(self.f_image, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.goBackButton()

    def goBack(self):
        self.destroy()
        MainFrame(self.master).pack()

    def goBackButton(self):
        Button(self, text='Back', command=self.goBack).grid(row=1, column=0)
        
class StartFrame(Frame):
    def __init__(self, master, from_main=False):
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
        if from_main:
            self.refresh()
        
    def refresh(self):
        self.master.original_image = None
        self.master.sinogram = None
        self.master.sinogram_resized = list()
        self.master.final_image = list()
        self.master.final_image_filtered = list()
        self.master.final_image_rmse = list()
        self.master.final_image_filtered_rmse = list()
        self.master.check_variable.set(False)
        self.master.check_variable_save.set(False)
        self.master.alpha = None
        self.master.r = None
        self.master.l = None
        self.master.height = None
        self.master.width = None
        self.master.name = None
        self.master.sex = None
        self.master.age = None
        self.master.date = None
        self.master.comment = None 
        
    def selectLabel(self):
        self.select_label = Label(self, text='Select file:')
        self.select_label.grid(row=0, column=0, sticky='E', padx=10, pady=20)

    def selectEntry(self):
        self.select_entry = Entry(self, width=50)
        self.select_entry.insert(INSERT, self.master.path_to_file)
        self.select_entry.grid(row=0, column=1, padx=10, pady=10)

    def selectButton(self):
        self.select_button = Button(self, text='Browse files', command=self.fileDialog)
        self.select_button.grid(row=0, column=2, padx=10, pady=10)

    def fileDialog(self):
        self.master.path_to_file = filedialog.askopenfilename(initialdir='./test', title='Select a file', filetype = (('All files', '*.*'), ('DICOM', '*.dcm'), ('JPEG', '*.jpg'), ('PNG', '*.png')))
        self.select_entry.delete(0, 'end')
        self.select_entry.insert(INSERT, self.master.path_to_file)

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
        self.emitters_detectors_scale = Scale(self, from_=1, to=720, length=400, orient=HORIZONTAL, showvalue=False, command=self.emitters_detectors_interval)
        self.emitters_detectors_scale.set(25)
        self.emitters_detectors_scale.grid(row=2, column=1, columnspan=2, padx=10, pady=10) 

    def rangeLabel(self):
        self.range_label = Label(self, text='Set range of the detectors-emitters set [degreess]')
        self.range_label.grid(row=3, column=0, sticky='E', padx=10, pady=10)

    def rangeScale(self):
        self.range_interval = lambda value : self.range_scale.config(label=int(value))
        self.range_scale = Scale(self, from_=1, to=270, length=400, orient=HORIZONTAL, showvalue=False, command=self.range_interval)
        self.range_scale.set(180)
        self.range_scale.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    def calculate(self):
        self.master.path_to_file = self.select_entry.get()
        self.master.step = self.step_scale.get() / 10
        self.master.emitters_detectors = self.emitters_detectors_scale.get()
        self.master.range = self.range_scale.get()
        self.destroy()
        MainFrame(self.master, True).pack()


    def examineButton(self):
        self.examine_button = Button(self, text='Examine', command=self.calculate)
        self.examine_button.grid(row=4, column=1, padx=10, pady=20)

class MainFrame(Frame):
    def __init__(self, master, from_start=False):
        Frame.__init__(self, master)
        self.patientInfo()
        self.showLoadedImageButton()
        self.backButton()
        self.generateSinogramButton()
        self.generateFinalImageButton()
        self.saveButton()
        self.filterCheckbox()
        self.saveCheckbox()
        self.analysisButton()
        if from_start:
            (
                self.master.original_image,
                self.master.name,
                self.master.sex,
                self.master.age,
                self.master.date,
                self.master.comment
            ) = sim.read_file(self.master.path_to_file)
        self.setPatientInfo()
        
    def filterCheckbox(self):
        self.checkbox = Checkbutton(self, text='Apply convolution filter', variable=self.master.check_variable, command=self.generateFinalImageButtonForget)
        self.checkbox.grid(row=4, column=0, padx=10, pady=10, sticky='W')

    def saveCheckbox(self):
        self.checkbox = Checkbutton(self, text='Use filtered image on save', variable=self.master.check_variable_save, command=self.saveButtonForget)
        self.checkbox.grid(row=6, column=3, padx=10, pady=10, sticky='W')

    def showLoadedImage(self):
        self.save()
        self.destroy()
        LoadedImageFrame(self.master).pack()

    def showLoadedImageButton(self):
        self.loaded_image_button = Button(self, text='Show loaded image', command=self.showLoadedImage)
        self.loaded_image_button.grid(row=1, column=0, padx=10, pady=10, sticky='W')       

    def analysisButton(self):
        self.analysis_button=Button(self, text='Show RMSE Analysis', command=self.showRMSEAnalysis)
        self.analysis_button.grid(row=6, column=0, padx=10, pady=10, sticky='W')

    def showRMSEAnalysis(self):
        self.save()
        self.destroy()
        RMSEFrame(self.master).pack()
        

    def back(self):
        self.destroy()
        StartFrame(self.master, True).pack()
        
    def backButton(self):
        self.back_button = Button(self, text='Back', command=self.back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='W')

    def generateSinogram(self):
        self.save()
        self.destroy()
        SinogramFrame(self.master).pack()

    def generateSinogramButton(self):
        if self.master.sinogram_resized == list():
            self.calculate_sinogram_button = Button(self, text='Generate sinogram', command=self.generateSinogram)
        else:
            self.calculate_sinogram_button = Button(self, text='Show sinogram', command=self.generateSinogram)
        self.calculate_sinogram_button.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        
    def generateFinalImage(self):
        self.save()
        self.destroy()
        FinalImageFrame(self.master).pack()

    def generateFinalImageButton(self):
        if not self.master.check_variable.get():
            if self.master.sinogram is None:
                self.calculate_final_image_button = Button(self, text='Generate final image\n(without filtering)', command=self.generateFinalImage, state='disabled')
            elif self.master.final_image == list():
                self.calculate_final_image_button = Button(self, text='Generate final image\n(without filtering)', command=self.generateFinalImage)
            else:
                self.calculate_final_image_button = Button(self, text='Show final image\n(without filtering)', command=self.generateFinalImage)
        else:
            if self.master.sinogram is None:
                self.calculate_final_image_button = Button(self, text='Generate final image\n(with filtering)', command=self.generateFinalImage, state='disabled')
            elif self.master.final_image_filtered == list():
                self.calculate_final_image_button = Button(self, text='Generate final image\n(with filtering)', command=self.generateFinalImage)
            else:
                self.calculate_final_image_button = Button(self, text='Show final image\n(with filtering)', command=self.generateFinalImage)
        self.calculate_final_image_button.grid(row=3, column=0, padx=10, pady=10, sticky='W')
          
    def generateFinalImageButtonForget(self):
        self.calculate_final_image_button.grid_forget()
        self.generateFinalImageButton()
    
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
        for item in [self.master.name, self.master.sex, self.master.age, self.master.date, self.master.comment]:
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
        self.master.name = self.name_entry.get(1.0, END)[:-1]
        self.master.sex = self.sex_entry.get(1.0, END)[:-1]
        self.master.age = self.age_entry.get(1.0, END)[:-1]
        self.master.date = self.date_entry.get(1.0, END)[:-1]
        self.master.comment = self.comment_entry.get(1.0, END)[:-1]
        
    def saveDicom(self):
        self.save()    
        self.file_to_save = filedialog.asksaveasfile(mode='w', defaultextension='.dcm')
        if self.file_to_save is not None:
            if not self.master.check_variable_save.get():
                sim.write_dicom_file(self.file_to_save.name, self.master.final_image[-1], self.master.name, self.master.sex, self.master.age, self.master.date, self.master.comment)
            else:
                sim.write_dicom_file(self.file_to_save.name, self.master.final_image_filtered[-1], self.master.name, self.master.sex, self.master.age, self.master.date, self.master.comment)
                                
    def saveButton(self):
        if not self.master.check_variable_save.get():
            if not len(self.master.final_image):
                self.save_button = Button(self, text='Save as DICOM\n(unfiltered image)', command=self.saveDicom, state='disabled')
            else:
                self.save_button = Button(self, text='Save as DICOM\n(unfiltered image)', command=self.saveDicom)
        else:
            if not len(self.master.final_image_filtered):
                self.save_button = Button(self, text='Save as DICOM\n(filtered image)', command=self.saveDicom, state='disabled')
            else:
                self.save_button = Button(self, text='Save as DICOM\n(filtered image)', command=self.saveDicom)
        self.save_button.grid(row=6, column=3, padx=10, pady=10, sticky='E')
      
    def saveButtonForget(self):
        self.save_button.grid_forget()
        self.saveButton()


root = App()
root.mainloop()
