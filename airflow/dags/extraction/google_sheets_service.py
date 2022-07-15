import pygsheets
import pandas as pd
from os.path import join, dirname
import extraction.config_helper as config_helper


def upload(data):
    worksheet = _get_worksheet()

    active_rows = len(worksheet.get_all_records())      # non-empty rows
    
    start_addr = (1, 1)     # Address of the top left corner where the data should be added
    include_head = True     # Copy header data into first row
    # If the sheet already contains data, set the start coordinates to the first empty row
    # and don't insert header row
    if active_rows > 1:
        start_addr = (active_rows+2, 1)
        include_head = False

    df = pd.DataFrame(data)

    # Add more rows to the sheet if needed (default wsh has only 1000 rows)
    _check_available_rows(worksheet, active_rows, len(df.index))

    worksheet.set_dataframe(df, start=start_addr, copy_index=False, copy_head=include_head)


def _get_worksheet():
    gdrive_configs = config_helper.get_config_section('gdrive')

    # Authenticate this application with a Google account
    gc = pygsheets.authorize(service_file=join(dirname(__file__), 'client_secrets.json'))

    file = gc.open(gdrive_configs.get('file_title'))
    return file.worksheet_by_title(gdrive_configs.get('sheet_title'))


def _check_available_rows(worksheet, active_rows, df_rows):
    worksheet_total_rows = worksheet.rows
    if worksheet_total_rows < (df_rows + active_rows + active_rows/10):
        worksheet.add_rows(int(worksheet_total_rows/4))
        print(f'Added {int(worksheet_total_rows/4)} to the worksheet. Before {worksheet_total_rows}, after {worksheet.rows}')
