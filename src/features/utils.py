import numpy as np
from statsmodels.graphics.tsaplots import acf, pacf
import pandas as pd
import streamlit as st


def create_standard_acf_array(data_series):
    return acf(data_series, alpha=0.05)


def create_standard_pacf_array(data_series):
    return pacf(data_series, alpha=0.05)


def calculate_corr_significance_intervals(corr_array):
    lower = corr_array[1][:, 0] - corr_array[0]
    upper = corr_array[1][:, 1] - corr_array[0]
    return lower, upper


def corr_significance_analysis(significance_values, acf_array):
    corr_significance_check = abs(acf_array) - abs(significance_values)

    signficant_non_zero_index = np.where(corr_significance_check > 0)

    significant_non_zero_correlations = acf_array[signficant_non_zero_index]

    df = pd.DataFrame(
        {'Lag': np.array(signficant_non_zero_index).squeeze(),
         'Significant non-zero autocorrelation value': significant_non_zero_correlations,
         'Autocorrelation absolute value': np.abs(significant_non_zero_correlations)
         })

    significant_non_zero_correlations_count = df.shape[0]

    return df, significant_non_zero_correlations_count


def corr_analysis(corr_array):
    lower, upper = calculate_corr_significance_intervals(
        corr_array)

    corr_array_1 = corr_array[0]

    df, significant_non_zero_correlations_count = corr_significance_analysis(
        lower, corr_array_1)

    return corr_array_1, df, significant_non_zero_correlations_count


def acf_settings():
    with st.expander('ACF Settings:'):

        acf_nlags_selected_col, acf_confidence_selected_col = st.columns(2)

        with acf_nlags_selected_col:
            acf_nlags_selected = st.number_input(
                'Number of non-zero lags:',  key='acf_nlags_selected', value=1)

        with acf_confidence_selected_col:
            confidence_interval = st.slider(
                'Confidence interval (%)', min_value=0, max_value=99, value=95)

        acf_adjust_selected_col, acf_fft_selected_col = st.columns(2)
        with acf_adjust_selected_col:
            acf_adjust_selected = st.radio(
                'Adjusted:', ('False', 'True'), key='acf_adjust_selected')

        with acf_fft_selected_col:
            acf_fft_selected = st.radio(
                'Compute ACF via FFT:', ('True', 'False'), key='acf_fft_selected')

        acf_adjust_selected = acf_adjust_selected == 'True'

        acf_fft_selected = acf_fft_selected == 'True'

        return [confidence_interval,
                acf_nlags_selected,
                acf_fft_selected,
                acf_adjust_selected]


pacf_calculation_methods = [
    # Yule-Walker with sample-size adjustment in denominator for acovf. Default.
    'yw', 'ywadjusted',
    # Yule-Walker without adjustment. Default.
    'ywm', 'ywmle',
    # regression of time series on lags of it and on constant.
    'ols',
    #  regression of time series on lags using a single common sample to estimate all pacf coefficients.
    'ols-inefficient',
    # regression of time series on lags with a bias adjustment.
    'ols-adjusted',
    # Levinson-Durbin recursion with bias correction.
    'ld', 'ldadjusted',
    # Levinson-Durbin recursion without bias correction.
    'ldb', 'ldbiased']


def pacf_settings():
    with st.expander('PACF Settings:'):

        pacf_nlags_selected_col, pacf_confidence_selected_col = st.columns(2)

        with pacf_nlags_selected_col:
            pacf_nlags_selected = st.number_input(
                'Number of non-zero lags:',  key='ppacf_nlags_selected', value=1)

        with pacf_confidence_selected_col:
            confidence_interval = st.slider(
                'Confidence interval (%)', min_value=0, max_value=99, value=95, key='pacf_confidence_selected_col')

        pacf_calculation_method = st.selectbox(
            label='Method for calculation', options=pacf_calculation_methods)
        return [confidence_interval,
                pacf_nlags_selected,
                pacf_calculation_method]
