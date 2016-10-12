from modules.PrEDIction import PrEDIction
from modules.PrEDIction import PrEDIctionTSDCPrinter

def process_client(client, document_type, data, prediction, printer):
    
#    grouping_options = ['1H', '2H', '4H', '1D']
#    grouping_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All', 'NoWeekends']

#    grouping_weekday_options = ['Monday']  
#    grouping_options = ['1H']
    
    grouping_weekday_options = []    
    grouping_options = []

    folding_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All', 'NoWeekends']
    folding_options = ['1H']

    cumsum_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All', 'NoWeekends']
    cumsum_options = ['1H']
    
#    folding_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'NoWeekends']
#    folding_options = ['1H']

    for weekday in grouping_weekday_options:
        for option in grouping_options:
            pregrouped_data = prediction.pregroup_data(data, option)
            prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
            grouped_data = prediction.group_data(prefiltered_data, option)
            printer.add_data(grouped_data)
            filename = client + '_' + document_type + '_grouped_' + option + '_' + weekday
            printer.set_filename(filename)
            printer.set_folder(client + '_' + document_type)
            printer.print_groupedTS()
            printer.clean()

    for weekday in folding_weekday_options:
        for option in folding_options:
            pregrouped_data = prediction.pregroup_data(data, option)
            prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
            folded_data = prediction.fold_data(prefiltered_data, option)
            printer.add_data(folded_data)
            filename = client + '_' + document_type + '_folded_' + option + '_' + weekday
            printer.set_filename(filename)
            printer.set_folder(client + '_' + document_type)
            printer.print_foldedTS()
            printer.clean()

    for weekday in cumsum_weekday_options:
        for option in cumsum_options:
            pregrouped_data = prediction.pregroup_data(data, option)
            prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
            cumsumed_data = prediction.cumsum_folded_data(prefiltered_data, option)
            folded_data = prediction.fold_data(cumsumed_data, option)
            printer.add_data(folded_data)
            filename = client + '_' + document_type + '_cumsum_' + option + '_' + weekday
            printer.set_filename(filename)
            printer.set_folder(client + '_' + document_type)
            printer.print_foldedTS()
            printer.clean()
            
def main():

    get_all_clients_query = 'SELECT EDI_CLIENT_DESC, APPLICATION, COUNT(*) \"COUNT\" FROM EDITT.EDITT_LEVEL1 WHERE MESSAGE_STATUS_DESC = \'FULLY_ACCEPTED\' GROUP BY EDI_CLIENT_DESC, APPLICATION ORDER BY COUNT DESC'
#    get_all_clients_query = 'SELECT * FROM (SELECT EDI_CLIENT_DESC, APPLICATION, COUNT(*) \"COUNT\" FROM EDITT.EDITT_LEVEL1 WHERE MESSAGE_STATUS_DESC = \'FULLY_ACCEPTED\' GROUP BY EDI_CLIENT_DESC, APPLICATION ORDER BY COUNT DESC) WHERE ROWNUM <= 1'

    prediction = PrEDIction()
    prediction.set_number_of_clients_limit(300)
    all_clients = prediction.get_clients(get_all_clients_query)
    for client in all_clients:
        print('Working on client ' + prediction.get_client_id(client) + ' - got ' + str(prediction.get_client_count(client)) + ' from DB' )
 
        if prediction.get_client_desc(client) is 'none':
            query = 'SELECT TRANSMISSION_DATE FROM EDITT.EDITT_LEVEL1 WHERE APPLICATION = \'' + prediction.get_client_document_type(client) + '\' ORDER BY TRANSMISSION_DATE DESC'
        else:
            query = 'SELECT TRANSMISSION_DATE FROM EDITT.EDITT_LEVEL1 WHERE EDI_CLIENT_DESC = \'' + prediction.get_client_desc(client) + '\' AND APPLICATION = \'' + prediction.get_client_document_type(client) + '\' ORDER BY TRANSMISSION_DATE DESC'

        data = prediction.get_data(query)
        printer = PrEDIctionTSDCPrinter()

        process_client(prediction.get_client_desc(client), prediction.get_client_document_type(client), data, prediction, printer)
    
if __name__ == '__main__':
    main()
