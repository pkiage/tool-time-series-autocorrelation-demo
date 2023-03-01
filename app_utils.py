import streamlit as st
from src.features.utils import corr_analysis


def corr_presentation(acf_array):
    [acf_array_1,
     df,
     significant_non_zero_correlations_count] = corr_analysis(acf_array)

    with st.expander('Autocorrelations:'):
        st.write(acf_array_1)

    with st.expander('Significant Autocorrelations:'):
        st.metric(label='Total significant autocorrelations:',
                  value=significant_non_zero_correlations_count)

        st.dataframe(df)
