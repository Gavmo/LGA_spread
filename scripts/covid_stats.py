"""Process the COVID data from data.gov.au"""

import sys

import pandas as pd


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
    get_covid_data(sys.argv[1])
