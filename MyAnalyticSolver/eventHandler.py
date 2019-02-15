# Event Handler
from tkinter.filedialog import askopenfilename
from dataHandler import DataHandler

class EventHandler:
    
    def __init__(self, interface):
        self.interface = interface
        self.dh = DataHandler(self)

    def function(self):
        # dummy function
        pass

    def askOpenFileName(self):
        selectedFile = askopenfilename()
        self.interface.setFileName(selectedFile)

    def linearRegression(self):
        if self.interface.checkRequirements():
            # Update Running Label
            self.interface.setRunningName("Linear Regression")
            # Load Column Names from CSV
            variables_list = self.dh.loadCSV(self.interface.getFileName())
            # variables_list = ['loan_status', 'loan_amnt', 'int_rate', 'installment','loan_status2', 'loan_amnt2', 'int_rate2', 'installment2', 'loan_status3', 'loan_amnt3', 'int_rate3', 'installment3']
            # Create Linear Regression GUI
            self.interface.createLinearRegression(variables_list)
        else:
            self.interface.promptAlertForCSV()

    def addSelectedVariables(self):
        # Get Variables List Box
        variables_lb = self.interface.getVariablesLB()
        # Get selected text in variables list box
        variables_list = variables_lb.get(0,'end')
        selected_list = [variables_lb.get(i) for i in variables_lb.curselection()]
        nonselected_list = list(set(variables_list).difference(selected_list))
        # Add Selected to Selected List Box
        for selected in selected_list:
            self.interface.appendSelectedVariablesLB(selected)
        # Refresh Variables List Box
        self.interface.refreshVariablesLB(nonselected_list)

    def removeSelectedVariables(self):
        # Get Selected Variables List Box
        selected_lb = self.interface.getSelectedVariablesLB()
        # Get variable text in selected variables list box
        selected_list = selected_lb.get(0,'end')
        variables_list = [selected_lb.get(i) for i in selected_lb.curselection()]
        nonselected_list = list(set(selected_list).difference(variables_list))
        # Add variables to Varaibles List Box
        for variable in variables_list:
            self.interface.appendVariablesLB(variable)
        # Refresh Variables List Box
        self.interface.refreshSelectedVariablesLB(nonselected_list)
        
    def addCategoricalVariables(self):
        # Get Variables List Box
        variables_lb = self.interface.getVariablesLB()
        # Get selected text in variables list box
        variables_list = variables_lb.get(0,'end')
        categorical_list = [variables_lb.get(i) for i in variables_lb.curselection()]
        noncategorical_list = list(set(variables_list).difference(categorical_list))
        # Add Categorical to Categorical List Box
        for categorical in categorical_list:
            self.interface.appendCategoricalVariablesLB(categorical)
        # Refresh Variables List Box
        self.interface.refreshVariablesLB(noncategorical_list)

    def removeCategoricalVariables(self):
        # Get Categorical Variables List Box
        categorical_lb = self.interface.getCategoricalVariablesLB()
        # Get variable text in selected variables list box
        categorical_list = categorical_lb.get(0,'end')
        variables_list = [categorical_lb.get(i) for i in categorical_lb.curselection()]
        noncategorical_list = list(set(categorical_list).difference(variables_list))
        # Add variables to Varaibles List Box
        for variable in variables_list:
            self.interface.appendVariablesLB(variable)
        # Refresh Variables List Box
        self.interface.refreshCategoricalVariablesLB(noncategorical_list)
        
    def removeOutputVariables(self, __singlar=False):
        # Get Selected Output List Box
        output_lb = self.interface.getOutputVariablesLB()
        # Get variable text in output variables list box
        output_list = output_lb.get(0,'end')
    
        variables_list = []
        if(__singlar):
            # Output List remove the old item (should be one or empty)
            variables_list = output_list
        else:
            variables_list = [output_lb.get(i) for i in output_lb.curselection()]

        nonoutput_list = list(set(output_list).difference(variables_list))
        # Add variables to Varaibles List Box
        for variable in variables_list:
            self.interface.appendVariablesLB(variable)
        # Refresh Variables List Box
        self.interface.refreshOutputVariablesLB(nonoutput_list)

    def addOutputVariables(self, __singlar=False):
        variables_lb = self.interface.getVariablesLB()
        output_list = [variables_lb.get(i) for i in variables_lb.curselection()]
        
        # take the first curselected only
        if ((__singlar) and (len(output_list) > 0)):
            output_list = [output_list[0]]
            # Clean out Output Listbox by Removing Output Variable and Add back into Variable List Box
            self.removeOutputVariables(True)
        
        variables_list = variables_lb.get(0,'end')
        # Get the nonoutputs to refresh variable list box
        nonoutput_list = list(set(variables_list).difference(output_list))
        # Add output to Output List Box
        for output in output_list:
            self.interface.appendOutputVariablesLB(output)
        # Refresh Variables List Box
        self.interface.refreshVariablesLB(nonoutput_list)

