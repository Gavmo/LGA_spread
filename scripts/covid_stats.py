"""Process the COVID data from data.gov.au"""

import re
import sys

import pandas as pd


def clean_lga(lga_name):
    """Set the LGA name to upper case and remove and of the (C) (A) from the name"""
    regexp = re.compile(r"^(.*?)(?:$|(?:\s\())")
    cap = re.search(regexp, lga_name)
    return cap.group(1).upper()


def get_covid_data(covid_data_file):
    c_19_data = pd.read_csv(covid_data_file)
    date_to_lga_df = c_19_data.pivot_table(index='notification_date',
                                           columns='lga_name19',
                                           values='lga_code19',
                                           aggfunc=pd.Series.count
                                           )
    # print(date_to_lga_df)
    # pd.set_option('max_columns', None)
    # print(date_to_lga_df.tail())
    return date_to_lga_df


if __name__ == '__main__':
    df = get_covid_data(sys.argv[1])
    print(clean_lga("Wingecarribee (A)"))
    [df.rename({x: clean_lga(x)}, axis='columns') for x in df.columns]
    print(df)
