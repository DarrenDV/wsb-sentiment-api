import json
import re
import pandas as pd

def read_tickers_from_csv(file_path, ticker_column_index, full_name_column_index):
    tickers = []
    df = pd.read_csv(file_path, sep=',', header=0) # seperator is different for different files
    for index, row in df.iterrows():
        if len(row) <= max(ticker_column_index, full_name_column_index):
            print(f"Skipping row {index}: {row}")
            continue

        raw_ticker = str(row[ticker_column_index])
        # Remove leading digits from ticker
        cleaned_ticker = re.sub(r'^\d+', '', raw_ticker)

        ticker = {
            "ticker": cleaned_ticker,
            "full_name": row[full_name_column_index]
        }

        if any(t['full_name'] == ticker['full_name'] for t in tickers):
            continue

        tickers.append(ticker)

    return tickers

def write_tickers_to_json(tickers, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(tickers, json_file, indent=4)

if __name__ == "__main__":
    input_file_path = 'raw/Instrument_list_66.csv'  
    output_file_path = 'processed/lse_tickers.json'  
    ticker_column_index = 0 
    full_name_column_index = 1  

    tickers = read_tickers_from_csv(input_file_path, ticker_column_index, full_name_column_index)
    write_tickers_to_json(tickers, output_file_path)
    print(f"Tickers written to {output_file_path}")