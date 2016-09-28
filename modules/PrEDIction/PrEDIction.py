import numpy as np
import datetime
import pandas as pd
from modules.DBConnector import DBConnector
from . import PrEDIctionTSDC
from ..TimeUtils import TimeUtils

class PrEDIction:
    
    def __init__(self):
        self.number_of_clients_limit = 5
        self.timeUtils = TimeUtils()
        
    def set_number_of_clients_limit(self, clients):
        self.number_of_clients_limit = clients
        
    def get_data(self, query):
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'SOATEST')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data).transpose()[0].transpose()
        
        return return_data

    def get_clients(self, query):
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'SOATEST')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data[:self.number_of_clients_limit])
        
        return return_data

    def get_client_desc(self, client):
        if client[0] is None:
            client[0] = 'none'
            
        return client[0]

    def get_client_document_type(self, client):
        if client[1] is None:
            client[1] = 'none'

        return client[1]
    
    def get_client_id(self, client):
        if client[0] is None:
            client[0] = 'none'
        if client[1] is None:
            client[1] = 'none'

        return client[0] + '_' + client[1]

    def get_client_count(self, client):
        return client[2]
    
    def filter_weekends(self, data):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) != 'Saturday' and self.timeUtils.getWeekday(item) != 'Sunday' ):
                returnData.append(item)

        return returnData

    def filter_weekday(self, data, weekday):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) == weekday ):
                returnData.append(item)

        return returnData

    def pregroup_data(self, data, type):
        print( 'Pregrouping data with rule: ' + type )            
        data_frame = pd.DataFrame( data=np.ones(len(data)), index=data, columns = ['amount'] )        
        grouped = data_frame.groupby( pd.TimeGrouper(freq=type) ).count()
        return grouped

    def prefilter_data_by_weekday(self, data, weekday):
        print( 'Filtering data by weekday: ' + weekday )
        
        if weekday == 'All':
            filtered = data
        elif weekday == 'NoWeekends':
            no_weekends_array = np.bool_( (np.sum([[data.index.weekday == 0], [data.index.weekday == 1], [data.index.weekday == 2], [data.index.weekday == 3], [data.index.weekday == 4]], axis=0))[0] )
            filtered = data[no_weekends_array]            
        else:
            weekday_number = self.timeUtils.get_weekday_number(weekday)            
            filtered = data[data.index.weekday == weekday_number]

        return filtered

    def get_group_type(self, type):
        if 'H' in type:
            group_time_unit = 'H'
            fold_timespan = 'D'
        if 'D' in type:
            group_time_unit = 'D'
            fold_timespan = 'W'

        group_time_amount = int(type.strip(group_time_unit))
            
        return group_time_amount, group_time_unit, fold_timespan
    
    def group_data(self, data, group_type):

        id = 'grouped_by_' + group_type        
        print( 'Grouping data by: ' + group_type )

        temp_times = pd.to_datetime(data.index)
        times = []
        for _time in temp_times:
            times.append(datetime.datetime.strptime(str(_time), '%Y-%m-%d %H:%M:%S'))
        array_times = np.array(times)
        group_time_amount, group_time_unit, fold_timespan = self.get_group_type( group_type )
        
        if group_time_unit == 'H':
            dtimes = 0.5 * np.ones(len(array_times)) * datetime.timedelta(hours=group_time_amount)
        if group_time_unit == 'D':
            dtimes = 0.5 * np.ones(len(array_times)) * datetime.timedelta(days=group_time_amount)
            
        grouped_TSDC = PrEDIctionTSDC.PrEDIctionTSDC(id)
        if(times is not None):
            grouped_TSDC.set_time(array_times)
        if(dtimes is not None):
            grouped_TSDC.set_dtime(dtimes)
        if(data is not None):
            grouped_TSDC.set_mean(data.values)

        return grouped_TSDC

    def cumsum_folded_data(self, data, group_type):
        
        cumsum_data = data.groupby( pd.TimeGrouper(freq='D'))
        temp_cumsum_data = pd.DataFrame( data=cumsum_data['amount'].cumsum().values, index=data.index, columns = ['amount'] )
        return temp_cumsum_data
    
    def fold_data(self, data, group_type):

        id = 'folded_by_' + group_type
        print( 'Folding data by: ' + group_type )

        group_time_amount, group_time_unit, fold_timespan = self.get_group_type( group_type) 
        
        if group_time_unit == 'H':
            selector_values = data.index.hour
            selector_values_array_max = 24
            
        if group_time_unit == 'D':
            selector_values = data.index.weekday
            selector_values_array_max = 7            

        number_of_selector_values_array_bins = int(selector_values_array_max/group_time_amount)
        selector_values_array = np.int_(np.linspace(0, selector_values_array_max, number_of_selector_values_array_bins+1))
        array_times = np.array(selector_values_array[:-1])
        dtimes = np.ones(len(array_times)) * group_time_amount * 0.5
            
        folded_TSDC = PrEDIctionTSDC.PrEDIctionTSDC(id)
        
        if(array_times is not None):
            folded_TSDC.set_time(array_times)
        if(dtimes is not None):
            folded_TSDC.set_dtime(dtimes)
                
        mean = []
        std = []
        min_value = []
        max_value = []

        for i in range(len(selector_values_array)-1):
#            print('Bins range ' + str(selector_values_array[i])+'-'+str(selector_values_array[i+1]))
            selector = ((selector_values>=selector_values_array[i]) & (selector_values<selector_values_array[i+1]))
#            print( data[selector].values.transpose()[0] )
            if( len(data[selector].values.transpose()[0]) != 0 ):
                mean.append( data[selector].values.transpose()[0].mean() )
                std.append( data[selector].values.transpose()[0].std() )
                min_value.append( data[selector].values.transpose()[0].min() )
                max_value.append( data[selector].values.transpose()[0].max() )
                folded_TSDC.add_values(selector_values_array[i], data[selector].values.transpose()[0] )
            else:
                mean.append( 0 )
                std.append( 0 )
                min_value.append( 0 )
                max_value.append( 0 )
                
        folded_TSDC.set_mean( np.array(mean) )
        folded_TSDC.set_std( np.array(std) )
        folded_TSDC.set_min( np.array(min_value) )
        folded_TSDC.set_max( np.array(max_value) )
            
        return folded_TSDC
