import os

from camelot import read_pdf


def scrape_dollar_amounts(pdf_path):
    tables = read_pdf(pdf_path, flavor="stream")
    dollar_amounts = []

    for table in tables:
        for row in table.df.itertuples(index=False):
            for cell in row:
                if isinstance(cell, str) and "$" in cell:
                    dollar_amounts.append(cell)

    return dollar_amounts


if __name__ == "__main__":
    # Get the path to the PDF file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_datafile_path = os.path.join(
        script_dir,
        "data",
        "onlineStatement.pdf",  # TODO handle varying filenames
    )

    # Scrape dollar amounts from the PDF
    dollar_amounts = scrape_dollar_amounts(input_datafile_path)

    # Print the scraped dollar amounts
    print("Scraped Dollar Amounts:")
    for amount in dollar_amounts:
        print(amount)
