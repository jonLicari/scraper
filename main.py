import os

import pandas as pd
from camelot import read_pdf

columns = ['Date', 'Name', 'Amount']


class FilteredTable(pd.DataFrame):
    '''Table for holding data filtered from the parsed pdf.'''
    def __init__(self, columns=None):
        super().__init__(columns=columns)

    def assign_row(self, row: list, index: int):
        '''Assign a new row to the dataframe at the specified index.'''
        super().loc[index] = row


def parse_data_from_input_file(pdf_path) -> list:
    '''Read the input file and parse data into tables.'''
    table_list = read_pdf(pdf_path, pages="2,3", flavor="stream")

    return table_list


def get_input_file_path() -> str:
    '''Return the filepath for the pdf to be parsed.'''
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #  TODO handle varying filenames

    return os.path.join(
        script_dir,
        "data",
        "onlineStatement_2023-02-18.pdf",
    )


def filter_tables(table) -> pd.DataFrame:
    '''Filter table data row-by-row and save to a new df.'''
    # New dataframe to read in filtered data to
    new_df = FilteredTable(columns=columns)

    # Iterate over the raw data table row-by-row and filter data
    for row in table.df.itertuples(index=False):
        filtered_row = []

        # save transaction date, ignore post date
        try:
            filtered_row.append(
                pd.to_datetime(row[0]+" 2023", format='%b %d %Y'))

        except Exception:
            continue

        filtered_row.append(row[2])

        try:
            filtered_row.append((row[4]))
        except Exception as error:
            print(row[4], "failed", error)
            continue

        # print(filtered_row)
        new_df.assign_row(row=filtered_row, index=len(new_df))

    return new_df


def print_to_terminal(table: pd.DataFrame) -> None:
    '''Print filtered table contents to the terminal.'''
    print(table)


if __name__ == "__main__":
    # Get the path to the PDF file
    input_datafile_path = get_input_file_path()

    # Parse the PDF into tables
    tables = parse_data_from_input_file(input_datafile_path)

    # Get the total number of tables
    table_count = tables.n

    # Filter tables
    for n in range(table_count):
        print("TABLE", n)
        print("Size = ", tables[n].shape)
        filtered_table: pd.DataFrame = filter_tables(tables[n])

        # Print to terminal
        print_to_terminal(filtered_table)
