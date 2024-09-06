from KrakenCancelOrdersForToken import  token, token_pair, buy_price, stop_loss, get_ticker_data, get_current_price, get_orders, id_matching_order, edit_open_order, cancel_matching_order
from KrakenCancelOrdersForToken import buy_check, buy_place, sell_check, sell_place, take_profit, take_profit_delta, get_order_price
from KrakenCancelOrdersForToken import check_balance, get_existing_balance, get_asset_data
from KrakenOhlcvDataUtilityCSV import get_low_data
from colorama import Fore, Style
from time import sleep
bought_price = None 
# TODO: Need to check SELL-place, sell check logic, check edit order, and price place, edit conditions

def get_status(check_balance, get_current_price, get_existing_balance, token_pair, buy_price, stop_loss, take_profit):
    current_price = get_current_price(token_pair)
    print(Fore.CYAN + f'Current Ticker Price = {current_price}' + Style.RESET_ALL)
    # Function below returns T/F is there is an existing balance of token. 
    existing_balance =  get_existing_balance(token)
    if existing_balance == True:
        print('Existing Balance, SELL')    
    else:
        print('No Balance, BUY.')

    orders = get_orders(token_pair)
    #print(orders)
    matching_order = id_matching_order(token_pair, orders)
    #print(f'matching order = {matching_order}')
    if matching_order == True:
        print('Open order Exists for Token, Check order')       
    elif matching_order == False:
        print('No Open order for Token, Create Order.')
        
    if existing_balance == True and matching_order == True:  
        status = 'Sell-Check'
    if existing_balance == True and matching_order == False:
        status = 'Sell-Place'
    if existing_balance == False and matching_order == True:
        status = 'Buy-Check'
    if existing_balance == False and matching_order == False:
        status = 'Buy-Place'
    return status

while True:
    # Main Loop - Monitor Orders & Balance until stopped
    print("")
    print(Fore.BLUE + '-------- Updating Status ---------' + Style.RESET_ALL)
    print(Fore.YELLOW + f'Buy Price = {buy_price}, Take Profit = {take_profit}, Stop Loss = {stop_loss}' + Style.RESET_ALL)   
    status = get_status(check_balance, get_current_price, get_existing_balance, token_pair, buy_price, stop_loss, take_profit)    
    #print(f'Status = {status}')
    # Actions to be performed in response to STATUS check.
    #get_orders(token_pair)
    orders = get_orders(token_pair)
    token_balance = check_balance(token)
    if status == 'Sell-Check':
        current_price = get_current_price(token_pair)
        if bought_price:
            buy_price = bought_price    # TODO: When buy order placed, buy_price will use that order_price.                       
            print('Previous buy order placed, buy_price = bought_price.')
        else:
            pass
        sell_check(current_price, orders, buy_price, take_profit_delta, token_balance)
    elif status == 'Sell-Place':
        sell_place(take_profit, token_pair, token_balance)
    elif status == 'Buy-Check':
        low_10_latest = get_low_data(token_pair)
        buy_price = low_10_latest
        # TODO: edit buy order to use low10 data
        buy_check(low_10_latest, orders, token_pair)
    elif status == 'Buy-Place':
        low_10_latest = get_low_data(token_pair)
        # TODO: Place buy order using low10 data
        buy_place(low_10_latest, token_pair)
    delay_interval = 240
    print(Fore.BLUE + f'------- Sleeping for {delay_interval} seconds before next status update --------' + Style.RESET_ALL)
    sleep(delay_interval) # Sleep delay before Running again.




