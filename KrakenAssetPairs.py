import requests
import pandas as pd
from kraken.spot import Market
# Function to get the list of tradable pairs and save to CSV
def get_tradable_pairs_and_save_to_csv():
    url = 'https://api.kraken.com/0/public/AssetPairs'
    response = requests.get(url)
    data = response.json()
    pairs = data['result']
    
    # Extract each pair's details into a list of dictionaries
    pairs_list = []
    for pair in pairs:
        pair_info = pairs[pair]
        pair_info['pair_name'] = pair  # Add the pair name to the dictionary
        pairs_list.append(pair_info)
    
    # Normalize the list of dictionaries
    df = pd.json_normalize(pairs_list)
    
    # Save the DataFrame to a CSV file
    csv_file_path = 'kraken_tradable_pairs.csv'
    df.to_csv(csv_file_path, index=False)
    print(f'DataFrame saved to {csv_file_path}')

    
    
# Call the function
#get_tradable_pairs_and_save_to_csv()
token_pair ='AAVEUSD'

def get_asset_data(token_pair):
    print('Get Asset Pair details, decimals, min order, etc.')
    data = Market().get_asset_pairs(pair=token_pair)
    # Check decimals pair vs. cost ???
    pair_decimals = data[token_pair]['pair_decimals']   # 0 - for prices in this pair
    cost_decimals = data[token_pair]['cost_decimals']   # 1 - cost of trades in pair (quote asset terms)
    lot_decimals = data[token_pair]['lot_decimals']     # 2 - volume (base asset terms)
    ordermin = data[token_pair]['ordermin']             # 3 - Min order size
    
    return pair_decimals, cost_decimals, lot_decimals, ordermin

#new_tuple = get_asset_data(token_pair)
#print(new_tuple[0]['AAVEUSD']['cost_decimals'])
#print(new_tuple[0])
#print(new_tuple[1])
#print(new_tuple[2])