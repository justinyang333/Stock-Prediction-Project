from yaml import safe_load
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import logging
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json


def setup_config() -> None:
    # Allow global access
    global config, headers
    
    # Load in configuration yaml file
    with open("./collection-config.yaml", "r") as stream:
        config = safe_load(stream)
        
    # Set the logging configuration
    logging.basicConfig(
        level=logging.WARNING,
        format=config["log-format"],
        datefmt=config["log-date-format"]
    )
    
    #Load request credentials
    with open("./credentials.json") as stream:
        headers = json.load(stream)
    

def parse_nasdaq(file_path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(file_path)
    df.drop(labels=["Last Sale", "Net Change", "% Change", "Market Cap", "Country"], inplace=True, axis=1)
    df.set_index("Symbol", inplace=True)
    df["IPO Year"] = df["IPO Year"].fillna(2001)
    df["IPO Year"] = pd.to_datetime(df["IPO Year"], format="%Y")
    return df


def create_parameters(data: pd.DataFrame, symbol: str) -> tuple[list[str], list[str], list[str]]:
    ipo_date: datetime = data.loc[symbol]["IPO Year"]
    start_year: int = 2001 if int(ipo_date.year) <= 2001 else int(ipo_date.year)
    symbols = []
    start_dates = []
    end_dates = []
    for i in range(start_year, 2023):
        symbols.append(symbol)
        start_dates.append(f"{i}-01-01")
        end_dates.append(f"{i+1}-01-01")
    
    return (symbols, start_dates, end_dates)



def get_historical_data(symbol: str, headers: dict, start_date: str, end_date: str) -> None:
    try:
        logging.info(f"Attempting to gather data for {symbol}")
        r = requests.get(url=f"https://api.marketdata.app/v1/stocks/candles/D/{symbol}?from={start_date}&to={end_date}&limit=50000", headers=headers)
        json_contents = r.json()
        if json_contents == {"s": "no_data", "prevTime": None, "nextTime": None}:
            logging.warning(f"No data to retrieve for {symbol} in the year {start_date[0:4]}")
        else:
            with open(f"../data/{symbol}_history_{start_date[0:4]}.json", "w") as output:
                json.dump(r.json(), output)
    except Exception as e:
        logging.error(f"Could not receive history for {symbol}")
        logging.error(e)


if __name__ == "__main__":
    #Script configuration
    setup_config()
    
    #Extract symbols and IPO from csv
    stock_data: pd.DataFrame = parse_nasdaq("./nasdaq_stock_export.csv")
    
    timestamp = datetime.now()
    request_count = 0

    # Loop through all symbols, using thread pool for mass requesting
    for s in stock_data.index.to_list()[5000:]:
        repeated_symbol, start_dates, end_dates = create_parameters(data=stock_data, symbol=s)
        
        if (request_count >= 50_000 and (timestamp + relativedelta(days=1)) > datetime.now()):
            logging.warning(f"Request count is currently {request_count}, the start time was {timestamp.strftime('%Y-%m-%d %H:%M:%S')}.  Sleeping for 1 hour...")
            while ((timestamp + relativedelta(days=1)) > datetime.now()):
                time.sleep(5)
            timestamp = datetime.now()
            request_count = 0
        
        with ThreadPoolExecutor(100) as tpe:
            _ = tpe.map(get_historical_data, repeated_symbol, [headers for _ in range(len(repeated_symbol))], start_dates, end_dates)
            print([f for f in _])
        request_count += len(repeated_symbol)
    
    print(f"Done. Sent {request_count} over {(datetime.now() - timestamp).seconds / 3600} hours.")
