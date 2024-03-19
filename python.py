from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import yfinance as yf
import pandas as pd

healthcare_tickers = ['JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'VRTX', 'REGN', 'BMY', 'AMGN', 'GILD']
technology_tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'INTC', 'ADBE', 'CSCO', 'NFLX']
real_estate_tickers = ['AMT', 'SPG', 'PLD', 'CCI', 'EQIX', 'WELL', 'DLR', 'PSA', 'AVB', 'O']
energy_tickers = ['XOM', 'CVX', 'BP', 'COP', 'SLB', 'EOG', 'KMI', 'VLO']
consumer_discretionary_tickers = ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'DIS', 'SBUX', 'BKNG', 'LVS', 'CMG']

tickers_by_sector = [healthcare_tickers, technology_tickers, real_estate_tickers, energy_tickers, consumer_discretionary_tickers]
sectors = ['Health Care', 'Information Technology', 'Real Estate', 'Energy Sector', 'Consumer Discretionary']

all_weights = {}  # สร้างตัวแปร all_weights เป็น Dictionary เปล่า
cleaned_weights = {}
for sector, tickers in zip(sectors, tickers_by_sector):
    try:
        stock_data = yf.download(tickers, start=pd.Timestamp.today() - pd.DateOffset(years=1), end=pd.Timestamp.today())
        df = stock_data['Adj Close']

        mu = expected_returns.mean_historical_return(df)
        Sigma = risk_models.sample_cov(df)

        ef = EfficientFrontier(mu, Sigma)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        # print(f"--- Sector: {sector} ---")
        # print(cleaned_weights)
        # ef.portfolio_performance(verbose=True)
        # print("\n")

        # เก็บข้อมูลน้ำหนักของแต่ละหุ้นในภูมิภาคลงในตัวแปร all_weights
        all_weights[sector] = cleaned_weights
        print(all_weights)
        # if sector not in all_weights:
        #      all_weights[sector] = cleaned_weights
        # else:
        #      for ticker, weight in cleaned_weights.items():
        #         all_weights[sector][ticker] += weight
        #         # print(all_weights)
    
    except Exception as e:
        print(f"Error occurred while processing sector {sector}: {e}")


print("All weights for each sector:", all_weights)
all_weights['Information Technology']['TSLA']
all_weights['Information Technology']
total_weights_sum = sum(all_weights.values())
total_weights_sum
final_weights = {ticker: weight / total_weights_sum for ticker, weight in all_weights.items()}
final_weights
print("\nFinal weights for the overall portfolio:", final_weights)


##################################################################################

# สร้างตัวแปรสำหรับเก็บน้ำหนักของแต่ละ sector
sector_weights = {}

# รวมน้ำหนักของหุ้นในแต่ละ sector เข้าด้วยกัน
for sector, tickers in zip(sectors, tickers_by_sector):
    try:
        stock_data = yf.download(tickers, start=pd.Timestamp.today() - pd.DateOffset(years=1), end=pd.Timestamp.today())
        df = stock_data['Adj Close']

        mu = expected_returns.mean_historical_return(df)
        Sigma = risk_models.sample_cov(df)

        ef = EfficientFrontier(mu, Sigma)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        # เก็บน้ำหนักของแต่ละ sector
        sector_weights[sector] = cleaned_weights

    except Exception as e:
        print(f"Error occurred while processing sector {sector}: {e}")

# ปรับสัดส่วนของน้ำหนักให้เท่ากับ 1
sector_weights

total_weights = sum(sum(weights.values()) for weights in sector_weights.values())
total_weights
final_weights = {ticker: sum(weights.get(ticker, 0) for weights in sector_weights.values()) / total_weights for ticker in set.union(*[set(weights.keys()) for weights in sector_weights.values()])}

print("Final weights for the overall portfolio:", final_weights)
list_values = []

list_values = final_weights.values()
sum(list_values)