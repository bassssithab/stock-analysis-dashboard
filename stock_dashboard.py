# ---------------------------
# STEP 1: Import Libraries
# ---------------------------
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO  # <-- For handling HTML tables
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------
# STEP 2: Fetch Tesla Stock Data (Question 1)
# ---------------------------
print("Fetching Tesla stock data...")
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print("\nTesla Stock Data:")
print(tesla_data.head())

# ---------------------------
# STEP 3: Scrape Tesla Revenue (Question 2)
# ---------------------------
print("\nScraping Tesla revenue data...")
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
headers = {"User-Agent": "Mozilla/5.0"}  # Add headers to mimic a browser
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Loop through tables to find "Quarterly Revenue"
tables = soup.find_all("table")
found = False
for table in tables:
    if "Quarterly Revenue" in str(table):
        tesla_revenue = pd.read_html(StringIO(str(table)))[0]  # Use StringIO here
        tesla_revenue.columns = ["Date", "Revenue"]
        tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]
        tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"])
        print("\nTesla Revenue Data:")
        print(tesla_revenue.tail())
        found = True
        break
if not found:
    print("Error: Tesla revenue table not found!")
    exit()

# ---------------------------
# STEP 4: Fetch GameStop Stock Data (Question 3)
# ---------------------------
print("\nFetching GameStop stock data...")
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
print("\nGameStop Stock Data:")
print(gme_data.head())

# ---------------------------
# STEP 5: Scrape GameStop Revenue (Question 4)
# ---------------------------
print("\nScraping GameStop revenue data...")
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
headers = {"User-Agent": "Mozilla/5.0"}  # Add headers to mimic a browser
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Loop through tables to find "Quarterly Revenue"
tables = soup.find_all("table")
found = False
for table in tables:
    if "Quarterly Revenue" in str(table):
        gme_revenue = pd.read_html(StringIO(str(table)))[0]  # Use StringIO here
        gme_revenue.columns = ["Date", "Revenue"]
        gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]
        gme_revenue["Revenue"] = pd.to_numeric(gme_revenue["Revenue"])
        print("\nGameStop Revenue Data:")
        print(gme_revenue.tail())
        found = True
        break
if not found:
    print("Error: GameStop revenue table not found!")
    exit()

# ---------------------------
# STEP 6: Dashboard (Questions 5 & 6)
# ---------------------------
def create_dashboard(stock_data, revenue_data, title):
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    revenue_data['Date'] = pd.to_datetime(revenue_data['Date'])
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name="Stock Price"), secondary_y=False)
    fig.add_trace(go.Scatter(x=revenue_data['Date'], y=revenue_data['Revenue'], name="Revenue"), secondary_y=True)
    fig.update_layout(title=title, xaxis_title="Date")
    fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Revenue (USD Millions)", secondary_y=True)
    fig.show()

# Generate dashboards
print("\nGenerating Tesla Dashboard...")
create_dashboard(tesla_data, tesla_revenue, "Tesla Stock vs Revenue")

print("\nGenerating GameStop Dashboard...")
create_dashboard(gme_data, gme_revenue, "GameStop Stock vs Revenue")
