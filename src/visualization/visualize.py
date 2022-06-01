import pandas as pd
import streamlit as st
import plotly.express as px
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.tsaplots import acf, pacf
import numpy as np
import plotly.graph_objects as go


def streamlit_2columns_metrics_df_shape(df: pd.DataFrame):
    (
        column1name,
        column2name,
    ) = st.columns(2)

    with column1name:
        st.metric(
            label="Rows",
            value=df.shape[0],
            delta=None,
            delta_color="normal",
        )

    with column2name:
        st.metric(
            label="Columns",
            value=df.shape[1],
            delta=None,
            delta_color="normal",
        )


def show_inputted_dataframe(data):
    with st.expander("Input Dataframe:"):
        st.dataframe(data)
        streamlit_2columns_metrics_df_shape(data)


def time_series_line_plot(data):
    fig = px.line(
        data
    )
    st.plotly_chart(fig, use_container_width=True)


def time_series_scatter_plot(data):
    fig = px.scatter(data, trendline="ols")
    st.plotly_chart(fig, use_container_width=True)


def time_series_box_plot(data):
    fig = px.box(data, hover_data=['Date'], points="all")
    st.plotly_chart(fig, use_container_width=True)


def time_series_violin_and_box_plot(graph_data):
    fig = px.histogram(graph_data,
                       marginal="violin")
    st.plotly_chart(fig, use_container_width=True)


def streamlit_chart_setting_height_width(
    title: str,
    default_widthvalue: int,
    default_heightvalue: int,
    widthkey: str,
    heightkey: str,


):
    with st.expander(title):

        lbarx_col, lbary_col = st.columns(2)

        with lbarx_col:
            width_size = st.number_input(
                label="Width in inches:",
                value=default_widthvalue,
                key=widthkey,
            )

        with lbary_col:
            height_size = st.number_input(
                label="Height in inches:",
                value=default_heightvalue,
                key=heightkey,
            )
    return width_size, height_size


# zero 0-lag autocorrelation = True
# fft


def streamlit_autocorrelation_plot_settings():
    with st.expander('Autocorrelation Plot Settings:'):
        lag_col, alpha_col = st.columns(2)

        with lag_col:
            lags_selected = st.number_input(
                label="Lags:",
                value=15)

        with alpha_col:
            alpha_selected = st.number_input(
                label="Alpha:",
                value=0.05)

        zero_include_selected = st.radio(
            label="Include the 0-lag autocorrelation:",
            options=('True', 'False'))

        zero_include_selected = zero_include_selected == 'True'

        return [lags_selected,
                alpha_selected,
                zero_include_selected]


def streamlit_acf_plot_settings():
    fft_compute_selected = st.radio(
        label="Compute the ACF via FFT:",
        options=('False', 'True'))

    fft_compute_selected = fft_compute_selected == 'True'

    return fft_compute_selected


def plotly_corr(corr_array, upper_y, lower_y):
    fig = go.Figure()
    [fig.add_scatter(x=(x, x), y=(0, corr_array[0][x]), mode='lines', line_color='#3f3f3f')
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                    marker_size=12)
    fig.add_scatter(x=np.arange(
        len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines', fillcolor='rgba(32, 146, 230,0.3)',
                    fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_yaxes(zerolinecolor='#000000')
    return fig


def create_standard_corr_plot(series, plot_pacf=False):
    corr_array = pacf(series.dropna(), alpha=0.05) if plot_pacf else acf(
        series.dropna(), alpha=0.05)
    lower_y = corr_array[1][:, 0] - corr_array[0]
    upper_y = corr_array[1][:, 1] - corr_array[0]

    fig = plotly_corr(corr_array, upper_y, lower_y)

    title = 'Partial Autocorrelation' if plot_pacf else 'Autocorrelation'
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


def create_acf_plot(data_series,
                    alpha_selected,
                    acf_nlags_selected_plot,
                    acf_fft_selected_plot):

    corr_array = acf(data_series,
                     alpha=alpha_selected,
                     nlags=acf_nlags_selected_plot,
                     fft=acf_fft_selected_plot)

    lower = corr_array[1][:, 0] - corr_array[0]
    upper = corr_array[1][:, 1] - corr_array[0]
    fig = plotly_corr(corr_array, upper, lower)
    title = 'Autocorrelation'
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


def create_pacf_plot(data_series,
                     alpha_selected,
                     acf_nlags_selected,
                     pacf_calculation_method):

    corr_array = pacf(data_series,
                      alpha=alpha_selected,
                      nlags=acf_nlags_selected,
                      method=pacf_calculation_method)
    lower = corr_array[1][:, 0] - corr_array[0]
    upper = corr_array[1][:, 1] - corr_array[0]
    fig = plotly_corr(corr_array, upper, lower)
    title = 'Partial Autocorrelation'
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)
