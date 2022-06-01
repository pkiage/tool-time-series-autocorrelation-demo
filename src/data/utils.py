import pandas as pd
import statsmodels.api as sm
data_set_options = [
    'Earthquake time series',
    'Stationarized temperature time series',
    'Sunspots'
]


def import_sample_data(sample_data_selected, data_set_options):
    if sample_data_selected == data_set_options[0]:
        data = pd.read_csv('data/processed/earthquake.csv',
                           parse_dates=['date'], index_col='date')

    if sample_data_selected == data_set_options[1]:
        data = pd.read_csv('data/processed/stationary_temp_NY.csv',
                           parse_dates=['DATE'], index_col='DATE')

    if sample_data_selected == data_set_options[2]:
        dta = sm.datasets.sunspots.load_pandas().data
        dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
        del dta["YEAR"]
        data = dta

    graph_data = data.reset_index()
    graph_data.columns.values[0] = 'Date'
    return data, graph_data
