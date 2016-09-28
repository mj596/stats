class TimeUtils:

    import datetime
    import numpy as np
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    weekdays_inv = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    
    def __init__(self):
        pass
    
    def get_weekday_from_date(self, date):
        return self.weekdays[date.weekday()]

    def get_weekday_name(self, weekday):
        return self.weekdays[weekday]

    def get_weekday_number(self, weekday):
        return self.weekdays_inv[weekday]
