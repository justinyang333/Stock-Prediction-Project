from yaml import safe_load
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import logging
import time
from datetime import datetime
import requests
import json

def parse_nasdaq(file_path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(file_path)
    df.drop(labels=["Last Sale", "Net Change", "% Change", "Market Cap", "Country"], inplace=True, axis=1)
    return df

def get_historical_data(symbol: str, headers: dict, start_year: str, end_year) -> None:
    try:
        logging.info(f"Attempting to gather data for {symbol}")
        r = requests.get(url=f"https://api.marketdata.app/v1/stocks/candles/D/{symbol}?from={start_year}-01-01&to={end_year}-01-01&limit=50000", headers=headers)
        logging.info(f"Request status: {r.status_code}")
        with open(f"../data/{symbol}_candle_history_{start_year}_to_{end_year}.json", "w") as output:
            json.dump(r.json(), output)
    except Exception as e:
        logging.error(f"Could not receive history for {symbol}")
        print(e)



if __name__ == "__main__":
    # Load in configuration yaml file
    with open("./collection-config.yaml", "r") as stream:
        config: dict = safe_load(stream)
        
    # Set the logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format=config["log-format"],
        datefmt=config["log-date-format"]
    )
    
    #Load request credentials
    with open("./credentials.json") as stream:
        headers: dict = json.load(stream)
    endpoint = "https://api.marketdata.app/v1/stocks/candles/D/{symbol}"
    
    #Extract symbols from text file
    stock_data = parse_nasdaq("./nasdaq_stock_export.csv")
    
    # get_historical_data("AAPL", headers)
    
    # with ThreadPoolExecutor(100) as tpe:
    #     _ = tpe.map(get_historical_data, stock_data["Symbol"].to_list(), [headers for _ in range(7731)], ["2010" for _ in range(7731)], ["2020" for _ in range(7731)])
    #     print([f.result() for f in _])
    
    with ThreadPoolExecutor(100) as tpe:
        _ = tpe.map(get_historical_data, stock_data["Symbol"].to_list(), [headers for _ in range(7731)], ["2005" for _ in range(7731)], ["2010" for _ in range(7731)])
        print([f.result() for f in _])
    
    print("Done.")