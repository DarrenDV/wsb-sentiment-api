import json
import os
def combine_tickers(input_directory, output_file_path):
    combined_tickers = []
    seen_symbols = set()

    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                tickers = json.load(file)
                for ticker in tickers:
                    symbol = ticker.get('ticker')
                    if symbol and symbol not in seen_symbols:
                        combined_tickers.append(ticker)
                        seen_symbols.add(symbol)

    with open(output_file_path, 'w') as output_file:
        json.dump(combined_tickers, output_file, indent=4)

if __name__ == "__main__":
    input_directory = 'processed'  
    output_file_path = 'combined_tickers.json'  

    combine_tickers(input_directory, output_file_path)
    print(f"Combined tickers written to {output_file_path}")

