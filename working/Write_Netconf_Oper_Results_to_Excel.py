from xlrd import open_workbook
from tempfile import TemporaryFile
from xlwt import Workbook, easyxf
from xlwt import Style
import os, re

row_count_to_append_result = 0
active_sheet_name = ""
current_working_dir = os.getcwd()

write_to_book = Workbook()

class Results:
    def WriteResults(self, operation, datastore, node_name, sheetnum, sheetname, row_count_to_append_result, dataConfig, edit_config_response, filterData, get_config_response_output, clicommandData, telnet_cli_output):
        try:
            adding_sheet = write_to_book.add_sheet(sheetname, cell_overwrite_ok=True)

            adding_sheet.write(0, 0, "DataStore", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 1, "Node", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 2, "Operation", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 3, "dataConfig_Request_XML", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 4, "dataConfig_Response_From_Server", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 5, "filterData_Request_XML", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 6, "filterData_Response_From_Server", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 7, "clicommandData", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))
            adding_sheet.write(0, 8, "telnetCliOutput", Style.easyxf(
                'pattern: pattern solid, fore_colour green;' 'borders: left thick, right thick, top thick, bottom thick;' 'font:height 500;' 'align: wrap yes'))

            style = easyxf('borders: left thin, right thin, top thin, bottom thin;' 'align: wrap yes')

            adding_sheet.col(int(row_count_to_append_result) - 1).width = 15000
            adding_sheet.row(int(row_count_to_append_result)).height_mismatch = 1
            adding_sheet.row(int(row_count_to_append_result)).height = 3000

            row = adding_sheet.row(row_count_to_append_result)
            row.write(0, datastore, style)
            row.write(1, node_name, style)
            row.write(2, operation, style)
            row.write(3, dataConfig, style)
            row.write(4, str(edit_config_response), style)
            row.write(5, filterData, style)
            row.write(6, str(get_config_response_output), style)
            row.write(7, clicommandData, style)
            row.write(8, telnet_cli_output, style)

        # Here Exception will be caught when "write_to_book.add_sheet" is trying to add already existing sheet.
        # So instead of adding it, we are calling that existing sheet to performing our operations.
        except:
            adding_sheet = write_to_book.get_sheet(sheetnum)

            style = easyxf('borders: left thin, right thin, top thin, bottom thin;' 'align: wrap yes')

            adding_sheet.col(int(row_count_to_append_result) - 1).width = 15000
            adding_sheet.row(int(row_count_to_append_result)).height_mismatch = 1
            adding_sheet.row(int(row_count_to_append_result)).height = 3000

            row = adding_sheet.row(row_count_to_append_result)
            row.write(0, datastore, style)
            row.write(1, node_name, style)
            row.write(2, operation, style)
            row.write(3, dataConfig, style)
            if re.search("error: ", str(edit_config_response)):
                row.write(4, str(edit_config_response), Style.easyxf(
                    'pattern: pattern solid, fore_colour red;' 'borders: left thin, right thin, top thin, bottom thin;' 'align: wrap yes'))
            elif re.search("time out ", str(edit_config_response)):
                row.write(4, str(edit_config_response), Style.easyxf(
                    'pattern: pattern solid, fore_colour red;' 'borders: left thin, right thin, top thin, bottom thin;' 'align: wrap yes'))
            elif re.search("relevant data model content already exists", str(edit_config_response)):
                row.write(4, str(edit_config_response), Style.easyxf(
                    'pattern: pattern solid, fore_colour red;' 'borders: left thin, right thin, top thin, bottom thin;' 'align: wrap yes'))
            else:
                row.write(4, str(edit_config_response), style)
            row.write(5, filterData, style)
            row.write(6, str(get_config_response_output), style)
            row.write(7, clicommandData, style)
            row.write(8, telnet_cli_output, style)

        write_to_book.save(current_working_dir + "\RPC_XML_Data_Test_Results.xls")
        write_to_book.save(TemporaryFile())
