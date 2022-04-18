# General import section
import streamlit as st #streamlit backend
import pandas as pd

# PyCaret classification
from pycaret.classification import *

def main(data_obj):
    st.header("Auto ML with PyCaret")
    # Check for existing dataset 
    try:
        var_read = pd.read_csv("Smoothing_and_Filtering//Preprocessing dataset.csv")
        cl_df = var_read

    except:
        cl_df = data_obj.df
        st.error("""You did not smooth of filter the data.
                     Please go to 'Smoothing and filtering' and finalize your results.
                     Otherwise, the default dataset would be used!
                     """)
    # Show dataset
    st.dataframe(cl_df)
    st.write(cl_df.shape)
    st.download_button(label="Download data as CSV",
                    data=cl_df.to_csv(index=False),
                    file_name='Preprocessed Dataset.csv',
                    mime='text/csv')
    
    columns_list = list(cl_df.select_dtypes(exclude=['object']).columns)
    selected_column = st.selectbox("Selected column", columns_list)

    with st.container():
        st.subheader('PyCaret Classification')
        exp_clf01 = setup(data = cl_df,
                          target = selected_column,
                          session_id = 123,
                          silent=True,
                          fix_imbalance=True)
        with st.spinner("Training models..."):
            best = compare_models(n_select = 5, sort="MCC")
            st.write(pull())


# Main
if __name__ == "__main__":
   main()