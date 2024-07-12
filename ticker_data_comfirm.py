import streamlit as st
import polars as pl
import plotly.express as px
import yfinance as yf
from datetime import date

ticker_symbol = 'TQQQ'
ticker = yf.Ticker(ticker_symbol)

startdate = str(date.today())
endtdate = str(date.today())

raw_data = ticker.history(period='1d', start=startdate,end=endtdate)

df = pl.DataFrame(raw_data.reset_index())

df = df.drop(df.columns[-2:])

# print(df)

dividends_data = df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
# print(dividends_data)

line_dividends_data = dividends_data.filter(pl.col("Dividends") != 0.0)
# print(line_dividends_data)
