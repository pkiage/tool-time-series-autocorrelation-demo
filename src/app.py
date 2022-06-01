from data.utils import *
from features.utils import *
from visualization.visualize import *
from app_utils import *


def main():

    st.title("Time Series Autocorrelation Demo")

    st.write("""
    Autocorrelation is the correlation of a single time series with a lag copy of itself.\n
    In the discrete case autocorrelation is also referred to as serial correlation.\n
    In general autocorrelation usually refers to the lag-one autocorrelation.
    """)

    st.title("Data")

    sample_data_selected = st.selectbox(
        'Select sample data:', data_set_options)

    data, graph_data = import_sample_data(
        sample_data_selected, data_set_options)

    with st.expander("Line Plot:"):
        time_series_line_plot(data)

    with st.expander("Box Plot:"):
        time_series_box_plot(graph_data)

    with st.expander("Dist Plot (histogram and violin plot):"):
        time_series_violin_and_box_plot(data)

    st.title("Time Series Autocorrelation")

    data_array = data.values.squeeze()

    data_series = pd.Series(data_array).dropna()

    st.header("Auto-Correlation Function (ACF)")

    st.write("""
    ACF shows the entire autocorrelation function for different lags (not just lag-one).\n
    Given the autocorrelation is a function of the lag any significant non-zero correlation imply the series can be forecast from the past.\n
    Lag 0 autocorrelation will always be 1 since the values (y-axis) are the same at the same time (x-axis) for the same time series.
    """)

    acf_type = st.radio(
        'Default ACF:', ('True', 'False'), key='acf_type')

    default_acf_selected = acf_type == 'True'

    if default_acf_selected:
        acf_array = create_standard_acf_array(data_series)

    if not default_acf_selected:
        [confidence_level,
         acf_nlags_selected,
         acf_fft_selected,
         acf_adjust_selected] = acf_settings()

        alpha_selected = (100-confidence_level)/100

        acf_array = acf(data_series,
                        alpha=alpha_selected,
                        nlags=acf_nlags_selected,
                        fft=acf_fft_selected,
                        adjusted=acf_adjust_selected)

    corr_presentation(acf_array)

    st.subheader("ACF Plot")

    if default_acf_selected:

        st.write('Given a confidence inverval of 95% (significance level of 0.05) there is a 5% chance that if true autocorrelation is zero, it will fall outside blue band.')

        create_standard_corr_plot(data_series, plot_pacf=False)

    if not default_acf_selected:

        st.write(
            f'Given a confidence inverval of {confidence_level}% (significance level of {alpha_selected}) there is a {alpha_selected*100}% chance that if true autocorrelation is zero, it will fall outside blue band.')

        create_acf_plot(data_series,
                        alpha_selected,
                        acf_nlags_selected,
                        acf_fft_selected)

    st.header("Partial Auto-Correlation Function (PACF)")

    st.write("Unlike ACF, PACF controls for other lags.")
    st.write(
        "PACF represents how significant adding lag n is when you already have lag n-1.")

    pacf_type = st.radio(
        'Default PACF:', ('True', 'False'), key='pacf_type')

    default_pacf_selected = pacf_type == 'True'

    if default_pacf_selected:
        pacf_array = create_standard_pacf_array(data_series)

    if not default_pacf_selected:
        [confidence_level,
         pacf_nlags_selected,
         pacf_calculation_method] = pacf_settings()

        alpha_selected = (100-confidence_level)/100

        pacf_array = pacf(data_series,
                          alpha=alpha_selected,
                          nlags=pacf_nlags_selected,
                          method=pacf_calculation_method)

    corr_presentation(pacf_array)

    st.subheader("PACF Plot")

    if default_pacf_selected:
        st.write('Given a confidence inverval of 95% (significance level of 0.05) there is a 5% chance that if true autocorrelation is zero, it will fall outside blue band.')
        create_standard_corr_plot(data_series, plot_pacf=True)

    if not default_pacf_selected:
        st.write(
            f'Given a confidence inverval of {confidence_level}% (significance level of {alpha_selected}) there is a {alpha_selected*100}% chance that if true autocorrelation is zero, it will fall outside blue band.')
        create_pacf_plot(data_series,
                         alpha_selected,
                         pacf_nlags_selected,
                         pacf_calculation_method)


if __name__ == "__main__":
    main()
