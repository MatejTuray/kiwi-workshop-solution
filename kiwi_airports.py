import logging
import os
import sys
import traceback

import pandas

from data import clean_data


def write_excel_dump(rows, headers):
    """
    Export data to excel file, openpyxl required
    :rows - individual airport data
    :headers - column headers
    """
    df = pandas.DataFrame(rows, columns=headers)
    print(df)
    df.to_excel("output.xlsx")
    print_separator()
    print("\n")
    print(F"Excel file saved in {os.path.dirname(os.path.abspath(__file__))}")

def print_separator():
    print(88 * "-")


def cli():
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--full":
            # Dump entire list of serializers
            rows = []
            for el in clean_data:
                rows.append(el.row)
            print_separator()
            write_excel_dump(rows, ["iata", "name", "icao", "lat", "lon", "city_name"])

        elif len(sys.argv) == 2 and sys.argv[1] == "--help":
            # Show help
            print_separator()
            print("Ways how to run the program\n")
            print("You can specify multiple options in the program:\n")
            print("--help - print help message")
            print("--cities - cities with airports")
            print("--coords - coordinates of each airport")
            print("--iata - IATA codes")
            print("--names - name of the airport")
            print("--icao - ICAO codes")
            print("--lat - latitude as a separate column")
            print("--lon - latitude as a separate column")
            print("--full - print every detail from each airport\n")
            print("You can mix and match flags to create your own table")
            print("When run without any option, only name and IATA code of airport is provided")

        elif len(sys.argv) >= 2 and ("--full" or "--help") not in sys.argv:
            # Display & output cols by single or multiple args
            # if wrong args are provided (full / help)
            # else block is executed
            rows = []
            headers = []
            for i in range(1, len(sys.argv)):
                headers.append(sys.argv[i].replace("--", ""))
            for el in clean_data:
                helper = []
                for j in headers:
                    helper.append(el.return_prop(sys.argv[headers.index(j) + 1].replace("--", "")))
                rows.append(helper)
            print_separator()
            write_excel_dump(rows, headers)

        else:
            # Default - return name and iata code of airport
            rows = []
            headers = ["iata", "name"]
            for el in clean_data:
                rows.append([el.iata, el.names])
            print_separator()
            write_excel_dump(rows, headers)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("Something went wrong or you provided invalid flags, try running the program with --help flag to learn"
              " more")


if __name__ == '__main__':
    cli()
