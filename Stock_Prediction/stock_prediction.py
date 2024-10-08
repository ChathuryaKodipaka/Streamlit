import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(page_title="Tesla Stock EDA App", page_icon="🚗", layout="wide")

# Display the centered title using markdown
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>Tesla Stock EDA App</h1>", unsafe_allow_html=True)

# Display the image centered with st.image
# st.image("/Users/chathurya/Desktop/tesla_logo.jpg", width=150)

# Display subtitle
st.markdown("<h4 style='text-align: center; color: #34495E;'>Explore Tesla's stock performance with interactive charts and insights.</h4>", unsafe_allow_html=True)

# Select stock symbol and time frame with enhanced visuals
stock_symbol = 'TSLA'
time_frame = st.radio(
    "Select Time Frame", 
    ['1 Year', '5 Years', '10 Years'], 
    index=1, 
    horizontal=True,
    help="Choose the time frame to visualize the stock data."
)

# Fetch stock data based on selected time frame
time_period = {'1 Year': '1y', '5 Years': '5y', '10 Years': '10y'}
ticker_data = yf.Ticker(stock_symbol)
ticker_df = ticker_data.history(period='1d', interval='1d', start='2013-01-01', end='2023-12-31') if time_frame == '10 Years' else ticker_data.history(period=time_period[time_frame])

# Calculate moving averages
ticker_df['MA20'] = ticker_df['Close'].rolling(window=20).mean()
ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()

# Display chart for Closing Price with Moving Averages
st.subheader(f"{stock_symbol} Stock Closing Price with Moving Averages ({time_frame})")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Close'], mode='lines', name='Closing Price', line=dict(color='#1f77b4')))  # Blue
fig1.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['MA20'], mode='lines', name='20-Day MA', line=dict(color='#2ca02c')))  # Green
fig1.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['MA50'], mode='lines', name='50-Day MA', line=dict(color='#d62728')))  # Red
fig1.update_layout(
    title='Closing Price with Moving Averages', 
    xaxis_title='Date', 
    yaxis_title='Price (USD)',
    template='plotly_dark',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig1, use_container_width=True)

# Display chart for Daily Volume
st.subheader(f"{stock_symbol} Daily Trading Volume ({time_frame})")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=ticker_df.index, y=ticker_df['Volume'], marker_color='#8e44ad', name='Volume'))  # Purple
fig2.update_layout(
    title='Daily Trading Volume', 
    xaxis_title='Date', 
    yaxis_title='Volume',
    template='plotly_dark',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig2, use_container_width=True)


