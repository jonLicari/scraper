import os

import pandas as pd
from camelot import read_pdf

columns = ["Date", "Description", "Amount"]


class FilteredTable(pd.DataFrame):
    """Table for holding data filtered from the parsed pdf."""

    def __init__(self, columns=None):
        super().__init__(columns=columns)

    def assign_row(self, row: list, index: int) -> int:
        """Assign a new row to the dataframe at the specified index."""
        if index >= 0:
            super().loc[index] = row
            return 0

        raise IndexError("Index must not be negative")


def parse_data_from_input_file(pdf_path) -> list:
    """Read the input file and parse data into tables."""
    table_list = read_pdf(pdf_path, pages="2,3", flavor="stream")

    return table_list


def get_input_file_path() -> str:
    """Return the filepath for the pdf to be parsed."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #  TODO handle varying filenames

    return os.path.join(
        script_dir,
        "data",
        "onlineStatement_2023-02-18.pdf",
    )


def validate_tables(table, new_df: pd.DataFrame) -> None:
    """Filter table data row-by-row and save to a new df."""
    # Find the number of columns in the table
    _, num_columns = table.shape

    # Iterate over the raw data table row-by-row and filter data
    for row in table.df.itertuples(index=False):
        filtered_row = []
        column_index = 0

        # save transaction date, ignore post date
        try:
            filtered_row.append(
                pd.to_datetime(row[column_index] + " 2023", format="%b %d %Y")
            )
        except Exception:
            continue

        # Ignore the Processing Date, save the description
        column_index = 1
        if row[column_index] == "":
            column_index = 2
            filtered_row.append(row[column_index])
        else:
            try:
                pd.to_datetime(row[column_index] + " 2023", format="%b %d %Y")
                column_index = 2
                if "PAYMENT THANK YOU" in row[column_index]:
                    continue
                filtered_row.append(row[column_index])
            except Exception:
                if "PAYMENT THANK YOU" in row[column_index]:
                    continue
                filtered_row.append(row[column_index])

        # Validate and save the amount
        column_index = column_index + 1
        error_f = False
        for i in range(column_index, num_columns):
            try:
                float(row[i])
                filtered_row.append((row[i]))
                error_f = False
                break
            except Exception:
                error_f = True

        if error_f is True:
            continue

        new_df.assign_row(row=filtered_row, index=len(new_df))


def print_to_terminal(table: pd.DataFrame) -> None:
    """Print filtered table contents to the terminal."""
    print(table)


if __name__ == "__main__":
    # Get the path to the PDF file
    input_datafile_path = get_input_file_path()

    # Parse the PDF into tables
    tables = parse_data_from_input_file(input_datafile_path)

    # New dataframe to read in filtered data to
    filtered_df = FilteredTable(columns=columns)

    # Filter tables
    for n in range(tables.n):
        validate_tables(tables[n], filtered_df)

    # Print to terminal
    print_to_terminal(filtered_df)
