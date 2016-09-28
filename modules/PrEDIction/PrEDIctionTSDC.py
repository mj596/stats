class PrEDIctionTSDC:

    def __init__(self, id):
        self.id = id
        self.time = None
        self.mean = None
        self.min = None
        self.max = None
        self.std = None
        self.dtime = None
        self.values = dict()
        
    def set_time(self, time):
        self.time = time

    def set_mean(self, mean):
        self.mean = mean

    def set_min(self, min):
        self.min = min

    def set_max(self, max):
        self.max = max

    def set_std(self, std):
        self.std = std

    def set_dtime(self, dtime):
        self.dtime = dtime

    def add_values(self, time, values):
        self.values[time] = values

    def get_time(self):
        return self.time

    def get_mean(self):
        return self.mean

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_std(self):
        return self.std

    def get_dtime(self):
        return self.dtime
        
    def get_values(self, time):
        return self.values.get(time)

    def get_values(self):
        return self.values
