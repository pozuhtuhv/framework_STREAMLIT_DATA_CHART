import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time

# SQLAlchemy 서버 연결
engine = create_engine('mysql+mysqlconnector://root:aaaaa@localhost/example_data')

def fetch_data(engine, data_range):
    query = "SELECT * FROM data_table ORDER BY timestamp_column DESC LIMIT "+str(data_range)
    df = pd.read_sql(query, engine)
    return df

# Streamlit app setting
def main():
    st.header("Live Chart", divider='blue')

    # Sidebar Dropbox area
    st.sidebar.title("Chart_Control")
    go_stop = st.sidebar.selectbox("Go_stop",["Go","Stop"]) # default "Go"
    data_range = st.sidebar.selectbox("Data_Range",["10","20","30","40","50","100"]) # query data range
    rerun_time = st.sidebar.selectbox("Rerun_Time (seconds)",["1","3","5","10"]) # chart rerun time

    while True:
        if go_stop == "Go":
            df = fetch_data(engine, data_range)

            # new chart
            st.header("Stream Data Chart")
            fig = px.line(df, x='timestamp_column', y='value_column')
            fig.update_layout(hovermode='x unified')  # tooltip set
            st.plotly_chart(fig)

            # data table view
            st.header("Live Data Table")
            st.dataframe(df)

            # update
            time.sleep(int(rerun_time))
            st.rerun()
        elif go_stop == "Stop":
            
            st.header("Select_box Value :red['Stop']")
            break
            
main()
