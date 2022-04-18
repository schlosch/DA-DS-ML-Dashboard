# General import section
import streamlit as st #streamlit backend

# Pandas profiling report
import pandas_profiling as pp
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
import streamlit.components.v1 as components

# Importing specific plots
from Visualization.visualization import Heatmap

def main(data_obj):
    """Data Preview main

    :param data_obj: DataObject instance
    :type data_obj: __main__.DataObject
    """
    st.header("DATA PREVIEW")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.subheader("Original dataframe")
        st.dataframe(data_obj.df)
        st.write(data_obj.df.shape)
        
    with col2:
        st.subheader("Dataframe description")
        st.dataframe(data_obj.df.describe())
    
    with col3:
        st.subheader("Data types")
        st.dataframe(data_obj.df.dtypes.astype(str))
        
    with col4:
        st.subheader("Correlation")
        st.dataframe(data_obj.df.corr())

    # Correlation matrix
    st.subheader("Correlation heatmap")
    Heatmap(data_obj)

    # Pandas profiling report
    ## Sidebar and checkbox
    st.sidebar.subheader("Pandas profiling report?")
    df_report = st.sidebar.checkbox("Show report")
    st.sidebar.write("Check this box to view a detailed report on your data. It can take time to load.")

    ## Report main body
    ### Generating and caching the report
    @st.experimental_memo
    def generate_report():
        report = pp.ProfileReport(data_obj.df)
        report_html = report.to_html()
        report.to_file("Data_Preview//Report.html")
        report.to_file("Data_Preview//Report.json")

        return report_html

    if df_report:
        with st.spinner("Generating report..."):
            with st.expander("Detailed report", expanded=True):
                components.html(generate_report(), height=1000, scrolling=True)

        with open("Data_Preview//Report.html", "rb") as file_html:
                btn_html = st.sidebar.download_button(label = "Download the report as HTML",
                                       data = file_html,
                                       file_name='Report.html',
                                       mime=None,
                                       )

        with open("Data_Preview//Report.json", "rb") as file_json:
                btn_json = st.sidebar.download_button(label = "Download the report as JSON",
                                       data = file_json,
                                       file_name='Report.json',
                                       mime=None,
                                       )

# Main
if __name__ == "__main__":
   main()