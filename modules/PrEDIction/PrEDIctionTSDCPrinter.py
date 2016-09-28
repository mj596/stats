class PrEDIctionTSDCPrinter:
    
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    import time
    import os

    weekdayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self):
        self.data = None
        self.filename = 'test_filename'
        self.folder = 'test_folder'
        
    def add_data(self, tsdc):
        self.data = tsdc

    def clean(self):
        self.data = None

    def set_filename(self, filename):
        self.filename = filename

    def set_folder(self, folder):
        self.folder = folder
        
    def print_foldedTS(self):
        
        self.plt.clf()

        with self.plt.style.context(('ggplot')):        
            if self.data.get_std() is not None:
                self.plt.errorbar(self.data.get_time(), self.data.get_mean(), xerr=self.data.get_dtime(), yerr=self.data.get_std(), fmt='ro', alpha=0.5, label="std dev")
                if len(self.data.get_time()) == 7:
                    self.plt.xticks(self.data.get_time(), self.weekdayLabels)

            if self.data.get_min() is not None:
                self.plt.errorbar(self.data.get_time(), self.data.get_min(), xerr=self.data.get_dtime(), fmt='b.', alpha=0.5, label="min")
            if self.data.get_max() is not None:
                self.plt.errorbar(self.data.get_time(), self.data.get_max(), xerr=self.data.get_dtime(), fmt='b.', alpha=0.5, label="max")
            if self.data.get_values() is not None:
                for key in self.data.get_values():
                    values = self.data.get_values()[key]
                    key_array = self.np.ones(len(values)) * int(key)
                    self.plt.plot(key_array, values, 'go', alpha=0.1)

            self.plt.xticks(rotation=20, size=10)
            self.plt.title(self.filename)
            self.plt.ylabel('Number of EDI transmissions')

        if not self.os.path.exists(self.folder):
            self.os.makedirs(self.folder)
            
        self.plt.savefig(self.folder + '/' + self.filename+'.png', dpi=300)
        
    def print_groupedTS(self):
        self.plt.clf()
        
        with self.plt.style.context(('ggplot')):
            # get size of a bar
            dtime_hours = self.np.int(2*self.np.int(self.data.get_dtime()[0].total_seconds())/3600)
            bar_width = dtime_hours/24

            # choose between plot types
            if dtime_hours < 1:
                self.plt.plot(self.data.get_time(), self.data.get_mean(), 'bo', alpha=0.5, label="mean")
                self.plt.plot(self.data.get_time(), self.data.get_mean(), 'b-', alpha=0.1, label="mean")
            else:
                self.plt.bar(self.data.get_time(), self.data.get_mean(), width=bar_width, alpha=0.5, label="mean")
                    
            self.plt.xticks(rotation=20, size=10)
                    
            self.plt.title(self.filename)
            self.plt.ylabel('Number of EDI transmissions')

        if not self.os.path.exists(self.folder):
            self.os.makedirs(self.folder)
            
        self.plt.savefig(self.folder + '/' + self.filename+'.png', dpi=300)
