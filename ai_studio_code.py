import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

st.set_page_config(page_title="PennyScan AI", layout="wide")

st.title("🚀 PennyScan: Beginner Trader Tool")
st.sidebar.header("Scan Settings")

# 1. User Inputs
ticker_symbol = st.sidebar.text_input("Enter Ticker (e.g., SNDL, IDEX, AMC)", "SNDL").upper()
risk_tolerance = st.sidebar.slider("Risk Tolerance (%)", 1, 10, 5)

if ticker_symbol:
    # 2. Get Data
    data = yf.download(ticker_symbol, period="60d", interval="1d")
    
    if not data.empty:
        # Calculate Technicals
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
        data['MA20'] = ta.sma(data['Close'], length=20)
        
        last_price = data['Close'].iloc[-1]
        last_rsi = data['RSI'].iloc[-1]
        atr = data['ATR'].iloc[-1]
        
        # 3. Analysis Logic
        st.subheader(f"Analysis for {ticker_symbol}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${last_price:.2f}")
        col2.metric("RSI (Strength)", f"{last_rsi:.2f}")
        col3.metric("Daily Volatility (ATR)", f"${atr:.2f}")

        # Recommendation Engine
        st.divider()
        st.header("💡 Trade Recommendation")
        
        recommendation = "NEUTRAL"
        reason = "No clear signal. Price is consolidating."
        
        # Simple Logic: Buy if Oversold (RSI < 30) or breaking above MA20
        if last_rsi < 35:
            recommendation = "LONG (BUY)"
            reason = "Stock is oversold (Low RSI). Potential bounce back."
        elif last_rsi > 70:
            recommendation = "SHORT (SELL)"
            reason = "Stock is overbought. Risk of a crash is high."
        
        st.success(f"Action: **{recommendation}**")
        st.info(f"Reason: {reason}")

        # 4. Risk Management (The most important part for beginners)
        st.divider()
        st.header("🛡️ Risk Management Plan")
        
        stop_loss = last_price - (atr * 1.5)
        take_profit = last_price + (atr * 3)
        risk_reward = (take_profit - last_price) / (last_price - stop_loss)

        c1, c2, c3 = st.columns(3)
        c1.error(f"Stop Loss: ${stop_loss:.2f}")
        c2.warning(f"Profit Target: ${take_profit:.2f}")
        c3.info(f"Risk/Reward Ratio: {risk_reward:.2f}")

        st.caption(f"Strategy: We set the Stop Loss based on 1.5x the ATR to avoid being 'shaken out' by normal penny stock noise.")

    else:
        st.error("Ticker not found. Please try again.")

# Disclaimer
st.sidebar.warning("DISCLAIMER: Penny stocks are high risk. This is a tool, not financial advice.")