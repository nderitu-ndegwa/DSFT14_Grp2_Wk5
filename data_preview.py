import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import time 
import plotly

st.set_page_config(layout="wide")

#Exploration function(numerical summary)
def explore(df):
    st.write('data')
    st.write(df)

    #numerical summary
    df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
    numerical_cols = df_types[~df_types['Data Type'].isin(['object', 'bool'])].index.values

    df_types['Count'] = df.count()
    df_types['Unique Values'] = df.nunique()
    df_types['Min'] = df[numerical_cols].min()
    df_types['Max'] = df[numerical_cols].max()
    df_types['Average'] = df[numerical_cols].mean()
    df_types['Median'] = df[numerical_cols].median()
    df_types['St. Dev.'] = df[numerical_cols].std()  
    
  
    #Using the pandas profiler(Profile Report)
    pr = ProfileReport(df, explorative=True)
    st_profile_report(pr)


@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner= True,
          ttl = 60)

def get_df(file):

    # get extension and read file
    extension = file.name.split('.')[1]

    if extension.upper() == 'CSV':
        df = pd.read_csv(file)
    elif extension.upper() == 'XLSX':
        df = pd.read_excel(file, engine='openpyxl')
    elif extension.upper() == 'PICKLE':
        df = pd.read_pickle(file)  
    
    return df

def main():
    #time.sleep(30)
    st.title("Cancer prevalence in the US")

    file = st.file_uploader("Upload dataset in .csv or .xlsx format", type=['csv', 'xlsx'], key = "1")
    st.write(file)


    if not file:
        st.write("Check that you have uploaded a .csv or .xlsx file to proceed")
        return

    df = get_df(file)
    st.subheader('Map of the data')
    explore(df)
    
    plt.rcParams["figure.figsize"] = (100, 50)
    xy = incidence_rate_state[['State','All cancer types combined / Both sexes combined']]
    #xy.plot.bar(x = 'State',fontsize='100')
    plt.xlabel('State',fontsize='100')
    plt.ylabel('Number of Incidences',fontsize='100')
    plt.title('Number of Cancer Inccidences Per State',fontsize='100')
    st.bar_chart(xy)
    
main()
