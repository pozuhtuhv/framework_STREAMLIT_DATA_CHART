import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time

# SQLAlchemy 서버 연결
engine = create_engine('mysql+mysqlconnector://root:aaaaa@localhost/example_data')

def fetch_data(engine, data_range):
    query = "SELECT * FROM data_table ORDER BY timestamp_column DESC LIMIT "+data_range
    df = pd.read_sql(query, engine)
    return df

# Streamlit 앱 설정
def main():
    st.title("Live Chart")
    
    st.sidebar.title("Chart_Control")
    data_range = st.sidebar.selectbox("Data_Range",["10","20","30","40","50","100"])
    rerun_time = st.sidebar.selectbox("Rerun_Time (seconds)",["1","3","5","10"])

    while True:
        df = fetch_data(engine, data_range)

        # 차트 생성
        fig = px.line(df, x='timestamp_column', y='value_column', title='Stream Data Chart')
        fig.update_layout(hovermode='x unified')  # 툴팁 표시
        st.plotly_chart(fig)

        # 데이터 테이블
        st.title("Live Data Table")
        st.dataframe(df)

        # 업데이트
        time.sleep(int(rerun_time))
        st.rerun()

main()
