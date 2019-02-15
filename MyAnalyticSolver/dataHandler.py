# Data Handler
import pandas as pd
import numpy as np

class DataHandler:
    
    def __init__(self, event):
        self.event = event
    
    def loadCSV(self, csv_path):
        # Load the CSV File's data into a DataFrame and return the column's name as a list
        self.csv_df = pd.read_csv(csv_path)
        columns_list = list(self.csv_df.columns.values)
        return columns_list

