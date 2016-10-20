class PrEDIctionPrinter:
    
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    import time
    import os
    

    weekdayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self):
        self.data = None
        self.filename = 'test_filename'
        self.folder = 'printer_out/test_folder'
        
    def add_data(self, tsdc):
        self.data = tsdc

    def clean(self):
        self.data = None

    def set_filename(self, filename):
        self.filename = filename

    def set_folder(self, folder):
        self.folder = 'printer_out/' + folder
        
    def print_foldedTS(self):
        
        self.plt.clf()

        with self.plt.style.context(('ggplot')):        
            if self.data.get_std() is not None:
                xtime = [self.datetime.datetime.strptime(elem, '%H:%M') for elem in self.data.get_time()]
                self.plt.errorbar(xtime, self.data.get_mean(), xerr=self.data.get_delta_time(), yerr=self.data.get_std(), fmt='ro', alpha=0.5)

            if self.data.get_min() is not None:
                self.plt.errorbar(xtime, self.data.get_min(), xerr=self.data.get_delta_time(), fmt='b-', alpha=0.5, label="min")
            if self.data.get_max() is not None:
                self.plt.errorbar(xtime, self.data.get_max(), xerr=self.data.get_delta_time(), fmt='b-', alpha=0.5, label="max")

            if self.data.get_values() is not None:
                for key in self.data.get_values():
                    values = self.data.get_values()[key]
#                    print(self.datetime.datetime.strptime(key, '%H:%M'))
#                    print(values)
                    key_array = [ self.datetime.datetime.strptime(key, '%H:%M') for i in range(len(values))]
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
            xtime = [self.datetime.datetime.strptime(elem, '%Y-%m-%d %H:%M') for elem in self.data.get_time()]
            histogram_width_in_days = 2*self.data.get_delta_time()[0].total_seconds()/(3600*24)
            self.plt.bar(xtime, self.data.get_mean(), width=histogram_width_in_days, alpha=0.5, label="mean")
                    
            self.plt.xticks(rotation=20, size=10)
                    
            self.plt.title(self.filename)
            self.plt.ylabel('Number of EDI transmissions')

        if not self.os.path.exists(self.folder):
            self.os.makedirs(self.folder + '/out/')
            
        self.plt.savefig(self.folder + '/out/' + self.filename+'.png', dpi=300)
