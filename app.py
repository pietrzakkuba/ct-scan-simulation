from tkinter import *
from tkinter import filedialog

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("CT Scan Simualation")
        self.wm_iconbitmap('gui/icon.ico')
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
        self.path_to_file = filedialog.askopenfilename(initialdir='/', title='Select a file', filetype = (('JPEG', '*.jpg'), ('PNG', '*.png'), ('All files', '*.*')))
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
        print('Path to file:\t\t' + self.select_entry.get())
        print('Step:\t\t\t' + str(self.step_scale.get() / 10))
        print('Emitters/Detectos:\t' + str(self.emitters_detectors_scale.get() * 2 + 1))
        print('Range:\t\t\t' + str(self.range_scale.get()))

    def examineButton(self):
        self.examine_button = Button(self, text='Examine', command=self.calculate)
        self.examine_button.grid(row=4, column=1, padx=10, pady=20)



root = Root()
root.mainloop()
