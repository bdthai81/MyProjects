from tkinter import *
import tkinter.messagebox as mb
from eventHandler import EventHandler

class GraphicsInterface:
    
    def __init__(self, width, height):
        # initialize variables
        self.__interfaceWidth = width 
        self.__interfaceHeight = height
        self.__header_bg = 'silver'
        self.__ListBoxLabel_bg = 'gainsboro'
        # Create Interface Window Template
        self.root = Tk()
        self.root.title("My Analytic Solver")
        self.root.geometry('{}x{}'.format(self.__interfaceWidth, self.__interfaceHeight)) # set size to fit iphone size
        self.root.resizable(0,0) # this prevents from resizing the window
        # Create EventHandler object
        self.eh = EventHandler(self)
    
    def createMenu(self):
        # Creating a root menu to insert all the sub menus
        root_menu = Menu(self.root)
        self.root.config(menu = root_menu)
        # Creating sub menus in the root menu
        file_menu = Menu(root_menu) # it intializes a new sub menu in the root menu
        root_menu.add_cascade(label = "File", menu = file_menu) # it creates the name of the sub menu
        file_menu.add_command(label = "Open .csv file", command = self.eh.askOpenFileName)
        file_menu.add_separator() # it adds a line after the 'Open files' option
        file_menu.add_command(label = "Exit", command = self.root.destroy)
        # creting another sub menu
        predict_menu = Menu(root_menu)
        root_menu.add_cascade(label = "Predict", menu = predict_menu)
        predict_menu.add_command(label = "Linear Regression", command = self.eh.linearRegression)
        predict_menu.add_command(label = "Neural Network", command = self.eh.function)

    def createTemplate(self):
        # create all of the main containers
        header_frame = Frame(self.root, bg=self.__header_bg, width=self.__interfaceWidth, height=40, pady=3)
        content_frame = Frame(self.root, width=self.__interfaceWidth, height=60, pady=3)
        footer_frame = Frame(self.root, width=self.__interfaceWidth, height=40, pady=3)
        footer_frame2 = Frame(self.root, width=self.__interfaceWidth, height=40, pady=3)
        footer_frame3 = Frame(self.root, width=self.__interfaceWidth, height=40, pady=3)
        # layout all of the main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header_frame.grid(row=0, sticky="ew")
        content_frame.grid(row=1, sticky="nsew")
        footer_frame.grid(row=3, sticky="ew")
        footer_frame2.grid(row=4, sticky="ew")
        footer_frame3.grid(row=5, sticky="ew")

        # create the content widgets
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.cnt_left_frame = Frame(content_frame, width=int(self.__interfaceWidth*0.4), padx=2, pady=2)
        self.cnt_mid_frame = Frame(content_frame, width=int(self.__interfaceWidth*0.2), padx=2, pady=2)
        self.cnt_right_frame = Frame(content_frame, width=int(self.__interfaceWidth*0.4), padx=2, pady=2)

        self.cnt_left_frame.grid(row=0, column=0, sticky="nsew")
        self.cnt_mid_frame.grid(row=0, column=1, sticky="nsew")
        self.cnt_right_frame.grid(row=0, column=2, sticky="nsew")
        self.cnt_left_frame.grid_propagate(False)
        self.cnt_mid_frame.grid_propagate(False)
        self.cnt_right_frame.grid_propagate(False)

        # Create Labels in Header
        intro_label = Label(header_frame, text="Welcome to My Analytic Solver!", bg=self.__header_bg)
        intro_label.grid(row=0, sticky='nw')
        intro_label2 = Label(header_frame, text="Please open CSV file, then choose method to run", bg=self.__header_bg)
        intro_label2.grid(row=1, sticky='nw')

        # create the widgets for the footer3 frame
        file_label = Label(footer_frame3, text='File: ')
        self.filename_label = Label(footer_frame3, text=None, wraplength=300)
        running_label = Label(footer_frame3, text='Running: ')
        self.runningname_label = Label(footer_frame3, text=None)

        # layout the widgets in the footer3 frame
        file_label.grid(row=0, column=0, sticky='nw')
        self.filename_label.grid(row=0, column=1, sticky='nw')
        running_label.grid(row=1, column=0, sticky='nw')
        self.runningname_label.grid(row=1, column=1, sticky='nw')

    def promptAlertForCSV(self):    
        mb.showinfo("Alert Message", "Please select a .CSV file")
        self.eh.askOpenFileName()

    def setFileName(self, fileName):
        # take .csv file only
        if(fileName):
            if fileName[-4:] == '.csv':
                self.filename_label.config(text=fileName) # assign .csv file into fileName Label
            else:
                # Wrong file, redo
                self.promptAlertForCSV()
        else:
            pass # Cancel selected
    
    def getFileName(self):
        return self.filename_label['text']

    def setRunningName(self, running):
        self.runningname_label.config(text=running)

    def getRunningName(self):
        return self.runningname_label['text']

    def checkRequirements(self):
        # Check to make sure .CSV is selected
        # currently, just need .csv filename else returns default None=False
        return self.getFileName()
            
    def createLinearRegression(self, variables_list):
        # Weight template
        self.cnt_left_frame.grid_columnconfigure(0, weight=1)
        self.cnt_mid_frame.grid_columnconfigure(0, weight=1)
        self.cnt_right_frame.grid_columnconfigure(0, weight=1)
        self.cnt_left_frame.grid_rowconfigure(1, weight=1)
        self.cnt_mid_frame.grid_rowconfigure(0, weight=7)
        self.cnt_mid_frame.grid_rowconfigure(3, weight=14)
        self.cnt_mid_frame.grid_rowconfigure(6, weight=9)
        self.cnt_right_frame.grid_rowconfigure(1, weight=1)
        self.cnt_right_frame.grid_rowconfigure(3, weight=1)

        # Create Variables List
        __variable_label = Label(self.cnt_left_frame, text="Variables", bg=self.__ListBoxLabel_bg)
        __variable_label.grid(row=0, sticky='nwe')
        self.variables_lb = Listbox(self.cnt_left_frame, selectmode='extended')
        for variable in variables_list:
            self.variables_lb.insert('end', variable)
        self.variables_lb.grid(row=1, sticky='nwe')
        
        # Create Add Selected Button
        self.addSelected_btn = Button(self.cnt_mid_frame, text = ">>>", command = self.eh.addSelectedVariables)
        self.addSelected_btn.grid(row=1)

        # Create Remove Selected Button
        self.removeSelected_btn = Button(self.cnt_mid_frame, text = "<<<", command = self.eh.removeSelectedVariables)
        self.removeSelected_btn.grid(row=2)

        # Create Selected Variables List
        __selected_label = Label(self.cnt_right_frame, text="Selected", bg=self.__ListBoxLabel_bg)
        __selected_label.grid(row=0, sticky='nwe')
        self.selectedVariables_lb = Listbox(self.cnt_right_frame, selectmode='extended')
        self.selectedVariables_lb.grid(row=1, sticky='nwe')

        # Create Add Categorical Button
        self.addCategorical_btn = Button(self.cnt_mid_frame, text = ">>>", command = self.eh.addCategoricalVariables)
        self.addCategorical_btn.grid(row=4)

        # Create Remove Categorical Button
        self.removeCategorical_btn = Button(self.cnt_mid_frame, text = "<<<", command = self.eh.removeCategoricalVariables)
        self.removeCategorical_btn.grid(row=5)

        # Create Categorical Variables List
        __categorical_label = Label(self.cnt_right_frame, text="Categorical", bg=self.__ListBoxLabel_bg)
        __categorical_label.grid(row=2, sticky='nwe')
        self.categoricalVariables_lb = Listbox(self.cnt_right_frame, selectmode='extended')
        self.categoricalVariables_lb.grid(row=3, sticky='nwe')

        # Create Add Output Button
        self.addOutput_btn = Button(self.cnt_mid_frame, text = ">>>", command = lambda: self.eh.addOutputVariables(True))
        self.addOutput_btn.grid(row=7)

        # Create Remove Output Button
        self.removeOutput_btn = Button(self.cnt_mid_frame, text = "<<<", command = lambda: self.eh.removeOutputVariables(True))
        self.removeOutput_btn.grid(row=8)

        # Create Output Entry
        __output_label = Label(self.cnt_right_frame, text="Output", bg=self.__ListBoxLabel_bg)
        __output_label.grid(row=4, sticky='nwe')
        self.outputVariables_lb = Listbox(self.cnt_right_frame, height=10)
        self.outputVariables_lb.config(height=0)
        self.outputVariables_lb.grid(row=5, sticky='nwe')

    def getVariablesLB(self):
        return self.variables_lb
     
    def appendVariablesLB(self, variable):
        self.variables_lb.insert('end', variable)

    def refreshVariablesLB(self, variables_list):
        # Clear List Box 
        self.variables_lb.delete(0,'end')
        # Add variables_list
        for variable in variables_list:
            self.variables_lb.insert('end', variable)

    def getSelectedVariablesLB(self):
        return self.selectedVariables_lb

    def appendSelectedVariablesLB(self, selected):
        self.selectedVariables_lb.insert('end', selected)

    def refreshSelectedVariablesLB(self, selected_list):
        # Clear List Box 
        self.selectedVariables_lb.delete(0,'end')
        # Add selected_list
        for selected in selected_list:
            self.selectedVariables_lb.insert('end', selected)

    def getCategoricalVariablesLB(self):
        return self.categoricalVariables_lb

    def appendCategoricalVariablesLB(self, categorical):
        self.categoricalVariables_lb.insert('end', categorical)

    def refreshCategoricalVariablesLB(self, categorical_list):
        # Clear List Box 
        self.categoricalVariables_lb.delete(0,'end')
        # Add selected_list
        for categorical in categorical_list:
            self.categoricalVariables_lb.insert('end', categorical)

    def getOutputVariablesLB(self):
        return self.outputVariables_lb

    def appendOutputVariablesLB(self, output):
        self.outputVariables_lb.insert('end', output)

    def refreshOutputVariablesLB(self, output_list):
        # Clear List Box 
        self.outputVariables_lb.delete(0,'end')
        # Add selected_list
        for output in output_list:
            self.outputVariables_lb.insert('end', output)

    def close(self):
        self.root.destroy()

    def run(self):
        # Create Menu + Template
        self.createMenu()
        self.createTemplate()
        # Run listening for events
        self.root.mainloop()


# main
if __name__ == "__main__":
    inter = GraphicsInterface(375, 667) # base off iphone6/7: 375x667
    inter.run()