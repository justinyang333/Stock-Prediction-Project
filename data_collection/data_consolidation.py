import os
import pandas as pd
from datetime import datetime
import logging
from yaml import safe_load
import json
from concurrent.futures import ThreadPoolExecutor


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


def make_ticker_directories(dir_contents: list[str]) -> None:
    ticker_set = set()
    
    for f in dir_contents:
        
        if f.split("_")[0] not in ticker_set:
            ticker_set.add(f.split("_")[0])
            os.mkdir(f"../data/{f.split('_')[0]}")
        os.rename("../data/" + f, f"../data/{f.split('_')[0]}/{f.split('_')[-1][0:4]}")
    pass

def remove_small_data(minimum_files: int) -> None:
    for dir in os.listdir("../data/"):
        
        if len(os.listdir(f"../data/{dir}")) < minimum_files:
            
            for f in os.listdir(f"../data/{dir}/"):
                logging.warning(f"Removing '../data/{dir}/{f}'")
                os.remove(f"../data/{dir}/{f}")
                
            os.rmdir(f"../data/{dir}")
            logging.warning(f"Successfully removed '../data/{dir}'")

def remove_incomplete_data() -> None:
    
    for dir in os.listdir("../data/"):
        
        if (not check_consecutive_years(f"../data/{dir}")):
            
            for f in os.listdir(f"../data/{dir}/"):
                logging.warning(f"Removing '../data/{dir}/{f}'")
                os.remove(f"../data/{dir}/{f}")
                
            os.rmdir(f"../data/{dir}")
            logging.warning(f"Successfully removed '../data/{dir}'")



def create_year_span_mapping(dir_path: str):
    year_span: dict[str, list] = {}
    
    for dir in os.listdir(dir_path):
        key: str = f"{sorted(os.listdir(f'../data/{dir}'))[0][0:4]}-{sorted(os.listdir(f'../data/{dir}'))[-1][0:4]}"
        if (key not in year_span.keys()):
            year_span[key] = [dir]
        else:
            year_span[key].append(dir)
    
    return year_span
        
        

def check_consecutive_years(dir_path: str) -> bool:
    files = sorted(os.listdir(dir_path))
    consecutive_flag: bool = True
    year: int = int(files[0][0:4])
    
    for i in range(len(files)):
        consecutive_flag = (int(files[i][0:4]) == year)
        if (not consecutive_flag):
            return False
        year += 1
    
    return True



def combine_jsons_to_csv(dir_path: str, start: str, end: str) -> None:
    
    for dir in os.listdir(dir_path):
        df = pd.DataFrame()
        if (start+".json" in os.listdir(dir_path + f"/{dir}")) and (end+".json" in os.listdir(dir_path + f"/{dir}")):
            try:
                print(dir)
                for file in os.listdir(dir_path + f"/{dir}"):
                    df = pd.concat([df, pd.read_json(f"{dir_path}/{dir}/{file}")], axis=0)
                df.drop("s", axis=1, inplace=True)
                df.rename(columns={"o" : "Day Open Price", "c" : "Day Close Price", "h" : "Daily High Price", "l" : "Daily Low Price", "v" : "Volume", "t" : "Date"}, inplace=True)
                df["Date"] = pd.to_datetime(df["Date"], unit="s")
                df["Symbol"] = dir
                df.sort_values(by=["Date"], inplace=True)
                df.reset_index(inplace=True)
                df.to_csv(f"{dir_path}/{dir}.csv")
            except:
                print(f"Issue consolidating {dir}")
        

def remove_non_csvs(path: str):
    for element in os.listdir(path):
        if not element[-4:] == ".csv":
            for file in os.listdir(f"{path}/{element}"):
                os.remove(f"{path}/{element}/{file}")
            os.rmdir(f"{path}/{element}")
            

def join_csvs(path: str):
    df = pd.DataFrame()
    for file in os.listdir(path):
        print(file)
        df = pd.concat([df, pd.read_csv(f"{path}/{file}")])
    df.to_csv("./dataset.csv")


def data_time_window(dataset: pd.DataFrame):
    dataset.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "index"], inplace=True)
    early_mask = pd.to_datetime(dataset["Date"]) >= datetime.strptime("02/28/2009", "%m/%d/%Y")
    late_mask = pd.to_datetime(dataset["Date"]) < datetime.strptime("03/01/2020", "%m/%d/%Y")
    filtered_data = dataset[late_mask & early_mask]
    filtered_data.reset_index(inplace=True)
    filtered_data.index = filtered_data["Date"]
    filtered_data.drop(columns=["index"], inplace=True)
    return filtered_data

if __name__ == "__main__":
    setup_config()

    
    
    
    
    
    
    