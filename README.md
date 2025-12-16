# Live Crypto Quant Analytics Dashboard

## Overview
This project is a real-time cryptocurrency analytics dashboard developed using **Python** and **Streamlit**.  
It ingests live price data from **Binance’s public REST API**, performs quantitative analysis, and visualizes the results through an interactive web interface.

The primary objective of this project is to demonstrate **real-time data ingestion**, **spread analysis**, and **z-score–based anomaly detection** between two crypto assets.

---

## Key Features
- Live price ingestion from Binance (REST API)
- Near real-time updates (1-second polling)
- Interactive symbol selection
- Spread calculation between BTCUSDT and ETHUSDT
- Z-score computation for statistical anomaly detection
- Configurable alert threshold
- Live data table and charts
- Timezone-aware UTC timestamps
- Robust handling of real-time data synchronization

---

## Technology Stack
- **Python 3**
- **Streamlit** – Web UI framework
- **Pandas** – Data manipulation and analytics
- **Requests** – API communication
- **Binance Public REST API**
- **streamlit-autorefresh** – Automated UI refresh

---

## Data Source
Live market prices are fetched from Binance using the public REST endpoint: https://api.binance.com/api/v3/ticker/price


- No API key required  
- Free and publicly accessible  
- Suitable for real-time analytics prototyping  

---

## How the Application Works
1. The application polls Binance’s REST API every second.
2. Latest prices for selected symbols are stored in memory.
3. All timestamps are recorded in UTC.
4. Prices are aligned using 1-second time buckets.
5. Spread and z-score analytics are computed.
6. Results are displayed as live charts and tables.
7. Alerts are triggered when the z-score crosses a defined threshold.

---

## Running the Application

### Install Dependencies
pip install streamlit pandas requests streamlit-autorefresh

### Run the App
streamlit run app.py


### Open the browser at:
http://localhost:8501

### Dashboard Components
- Controls Panel
Symbol selection (BTCUSDT, ETHUSDT)

- Z-score alert threshold slider
Live Tick Data
Recent price updates with timestamps

- Charts
Price chart (BTCUSDT & ETHUSDT)
Spread chart
Z-score chart

