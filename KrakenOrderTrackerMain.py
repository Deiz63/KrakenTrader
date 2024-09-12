from KrakenCancelOrdersForToken import  token, token_pair, buy_price,  get_ticker_data, get_current_price, get_orders, id_matching_order, edit_open_order, cancel_matching_order
from KrakenCancelOrdersForToken import buy_check, buy_place, sell_check, sell_place,  get_order_price
from KrakenCancelOrdersForToken import check_balance, get_existing_balance, get_asset_data
from KrakenCancelOrdersForToken import buy_price, stop_loss_value, take_profit_value, price_round_value
from KrakenOhlcvDataUtilityCSV import get_low_data
from colorama import Fore, Style
from time import sleep
bought_price = None 
# TODO: Need to check SELL-place, sell check logic, check edit order, and price place, edit conditions

def get_status(check_balance, get_current_price, get_existing_balance, token_pair, buy_price, stop_loss, take_profit):
    current_price = get_current_price(token_pair)
    print(Fore.CYAN + f'Current Ticker Price = {current_price}' + Style.RESET_ALL)
    existing_balance =  get_existing_balance(token) # Returns T/F if existing balance exists
    orders = get_orders(token_pair) # Returns all open orders 
    matching_order = id_matching_order(token_pair, orders)
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
    if bought_price:
        buy_price = bought_price    # TODO: When buy order placed, buy_price will use that order_price.                       
        print(f"Buy order was placed, buy_price = {buy_price}, bought_price = {bought_price}")
    # Update Price calculations to use updated 'bought_price'
    stop_loss_delta = (buy_price * stop_loss_value)
    stop_loss = round(buy_price - stop_loss_delta, price_round_value)
    trigger_price = round(stop_loss - (.25 * stop_loss_delta), price_round_value)
    limit_price = round(stop_loss, price_round_value)
    take_profit_delta = (buy_price * take_profit_value)
    take_profit_add = (buy_price + take_profit_delta)
    take_profit = round(take_profit_add, price_round_value)
    
    print(Fore.YELLOW + f'Buy Price = {buy_price}, Take Profit = {take_profit}, Stop Loss = {stop_loss}' + Style.RESET_ALL)   
    status = get_status(check_balance, get_current_price, get_existing_balance, token_pair, buy_price, stop_loss, take_profit)    
    #print(f'Status = {status}')
    # Actions to be performed in response to STATUS check.
    orders = get_orders(token_pair)
    token_balance = check_balance(token)
    if status == 'Sell-Check':
        current_price = get_current_price(token_pair)
        if bought_price:
            buy_price = bought_price    # TODO: When buy order placed, buy_price will use that order_price.                       
            print('Previous buy order placed, buy_price = bought_price.')
        else:
            pass
        sell_check(trigger_price, limit_price, current_price, orders, buy_price, token_balance, stop_loss, stop_loss_delta, take_profit, take_profit_delta)
    elif status == 'Sell-Place':
        if bought_price:
            buy_price = bought_price    # TODO: When buy order placed, buy_price will use that order_price.                       
            print(f'Previous buy order placed, buy_price = {buy_price }, bought_price = {bought_price}.')
        else:
            print('No existing Bought price.')
        sell_place(take_profit, token_pair, token_balance)
    elif status == 'Buy-Check':
        low_10_latest = get_low_data(token_pair)
        # TODO: edit buy order to use low10 data
        bought_price = buy_check(low_10_latest, orders, token_pair)
    elif status == 'Buy-Place':
        low_10_latest = get_low_data(token_pair)
        # TODO: Place buy order using low10 data
        bought_price = buy_place(low_10_latest, token_pair)
    delay_interval = 240
    print(Fore.BLUE + f'------- Sleeping for {delay_interval} seconds before next status update --------' + Style.RESET_ALL)
    sleep(delay_interval) # Sleep delay before Running again.




