import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Live Crypto Quant Analytics", layout="wide")
st.title("📈 Live Crypto Quant Analytics")

# -----------------------------
# Session storage
# -----------------------------
if "buffer" not in st.session_state:
    st.session_state.buffer = []

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Controls")

symbols = st.sidebar.multiselect(
    "Select Symbols",
    ["BTCUSDT", "ETHUSDT"],
    default=["BTCUSDT", "ETHUSDT"]
)

alert_threshold = st.sidebar.slider(
    "Z-Score Alert Threshold",
    1.0, 3.0, 2.0
)

# -----------------------------
# Auto refresh every second
# -----------------------------
st_autorefresh(interval=1000, key="refresh")

# -----------------------------
# Fetch LIVE prices
# -----------------------------
for sym in symbols:
    try:
        r = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={sym}",
            timeout=2
        ).json()

        st.session_state.buffer.append({
            "time": datetime.now(timezone.utc),
            "symbol": sym.lower(),
            "price": float(r["price"])
        })

    except Exception:
        pass

# Limit memory
st.session_state.buffer = st.session_state.buffer[-200:]

# -----------------------------
# MAIN UI
# -----------------------------
st.write(f"📊 Data points collected: {len(st.session_state.buffer)}")

if len(st.session_state.buffer) < 5:
    st.info("Collecting live data… please wait a few seconds.")
    st.stop()

df = pd.DataFrame(st.session_state.buffer)

st.subheader("Live Tick Data")
st.dataframe(df.tail(10))

# -----------------------------
# 🔥 FIX: TIME ALIGNMENT
# -----------------------------
df["time_bucket"] = df["time"].dt.floor("1s")

pivot = (
    df.pivot(index="time_bucket", columns="symbol", values="price")
      .sort_index()
      .ffill()
)

# Ensure both symbols exist
required = {"btcusdt", "ethusdt"}
if not required.issubset(pivot.columns) or len(pivot) < 3:
    st.info("Waiting for aligned BTC & ETH data…")
    st.stop()

# -----------------------------
# Analytics
# -----------------------------
pivot["spread"] = pivot["btcusdt"] - pivot["ethusdt"]

std = pivot["spread"].std()
if std == 0 or pd.isna(std):
    st.info("Waiting for spread variance…")
    st.stop()

pivot["zscore"] = (pivot["spread"] - pivot["spread"].mean()) / std

# -----------------------------
# Charts
# -----------------------------
# st.subheader("Price Chart")
# st.line_chart(pivot[["btcusdt", "ethusdt"]])

st.subheader("Price Distribution (Latest Snapshot)")

latest_prices = pivot[["btcusdt", "ethusdt"]].iloc[-1]

pie_df = pd.DataFrame({
    "Asset": ["BTCUSDT", "ETHUSDT"],
    "Price": latest_prices.values
})

st.vega_lite_chart(
    pie_df,
    {
        "mark": {"type": "arc", "innerRadius": 0},
        "encoding": {
            "theta": {"field": "Price", "type": "quantitative"},
            "color": {"field": "Asset", "type": "nominal"},
            "tooltip": [
                {"field": "Asset", "type": "nominal"},
                {"field": "Price", "type": "quantitative"}
            ],
        },
    },
)


st.subheader("Spread Chart")
st.line_chart(pivot["spread"])

st.subheader("Z-Score Chart")
st.line_chart(pivot["zscore"])

# -----------------------------
# Alert
# -----------------------------
latest_z = pivot["zscore"].iloc[-1]
if abs(latest_z) > alert_threshold:
    st.error(f"🚨 Z-score crossed: {latest_z:.2f}")
