from KrakenAPI import api_key, secret_key # Import your API keys
from kraken.spot import User, Trade, Market
from colorama import Fore, Style
from time import sleep
# TODO: check rounding & (decimals) for all lines, verify correct
# TODO: Need to get correct Buy vs Low_10 vs purchased, 
# set edit thresholds - create variables?
# Fix edit order for Stop-limit, do I need to cancel & create new?
bought_price = None 

token = 'CQT'               # TODO: 
buy_price = .0045              # TODO: Enter Desired Buy Price
# Above is the initial desired buy price.
# Once an order is placed, the actual order price will be used. 
# TODO: CHECK IF THE FOLLOWING LINE IS WORKING, edit & change location if not successful. 
if bought_price:
    buy_price = bought_price    # TODO: When buy order placed, buy_price will use that order_price.                       
    print(f"Buy order was placed, buy_price = {bought_price}")
        
stop_loss_value = .10         # TODO: slv * 100 = Sl percent
take_profit_value = .015       # TODO: tpv * 100 = TP percent

# Gather token data
token_pair = f'{token}USD'

def get_asset_data(token_pair):
    print('Get Asset Pair details, decimals, min order, etc.')
    data = Market().get_asset_pairs(pair=token_pair)
    # Check decimals pair vs. cost ???
    pair_decimals = data[token_pair]['pair_decimals']   # 0 - for prices in this pair
    cost_decimals = data[token_pair]['cost_decimals']   # 1 - cost of trades in pair (quote asset terms)
    lot_decimals = data[token_pair]['lot_decimals']     # 2 - volume (base asset terms)
    ordermin = data[token_pair]['ordermin']             # 3 - Min order size
    return pair_decimals, cost_decimals, lot_decimals, ordermin

asset_data = get_asset_data(token_pair)
# Calculations - Price / Volume
order_min = float(asset_data[3])                # Decimals for Order Min
order_calc = 3 * order_min
order_volume = order_min + order_calc       # NOTE: Order Vol = Min + 25%

price_round_value = asset_data[0]           # Decimals for Buy Price
volume_round_value = asset_data[2]          # Decimals for Volume

stop_loss_delta = (buy_price * stop_loss_value)
stop_loss = round(buy_price - stop_loss_delta, price_round_value)
take_profit_delta = (buy_price * take_profit_value)
take_profit_add = (buy_price + take_profit_delta)
take_profit = round(take_profit_add, price_round_value)
volume_calc = 10 / buy_price
volume_to_order = round((volume_calc), volume_round_value)

trigger_price = round(stop_loss - (.25 * stop_loss_delta), price_round_value)
limit_price = round(stop_loss, price_round_value)


def check_balance(token):     # check_balance
    user = User(key=api_key, secret=secret_key)
    balance = user.get_balance(currency=token)    
    #print(balance)
    token_balance = (balance['balance'])
    return token_balance # Function returns isolated token value

def get_existing_balance(token):
    token_balance = check_balance(token)
    if token_balance > 0.01:
        existing_balance = True
    else:
        existing_balance = False
    print(Fore.GREEN + f'Current Token Balance = {token_balance}, Existing Balance = {existing_balance}' + Style.RESET_ALL)
    return existing_balance


def get_ticker_data(token_pair):
    ticker_data = Market().get_ticker(pair=token_pair)
    print(ticker_data)
    current_price = float(ticker_data[token_pair]['c'][0])
    highest_price = float(ticker_data[token_pair]['h'][0])
    lowest_price = float(ticker_data[token_pair]['l'][0])
    print(current_price)
   
def get_current_price(token_pair): 
    ticker_data = Market().get_ticker(pair=token_pair)
    current_price = float(ticker_data[token_pair]['c'][0])
    return current_price

def get_orders(token_pair):
    # Initialize Kraken Order API
    user = User(key=api_key, secret=secret_key)
    orders = user.get_open_orders()     # Get open orders
    return orders # Return All Order listings

def id_matching_order(token_pair, orders):
    matching_order = False
    for order_id, order_details in orders['open'].items(): 
        # Set variables from order data
        asset_pair = order_details['descr']['pair']
        order_action = order_details['descr']['type']
        order_price = order_details['descr']['price']
        # Check if any orders match token pair.
        if asset_pair == token_pair:
            print(f"ID matching order token pair = asset pair : {token_pair} = {asset_pair}")
            matched_order = order_id
            matching_order = True
            #print(f'asset_pair = {asset_pair} token_pair = {token_pair}.')
            print(f'Open order for {token_pair} found : Order Action = {order_action}, Order Price = {order_price}')
            print(Fore.YELLOW + f'order ID = {order_id}.' + Style.RESET_ALL) 
        else:
            pass
    return matching_order

def get_order_price(token_pair, orders):
    for order_id, order_details in orders['open'].items():
        order_price = order_details['descr']['price']
        #print(f'Existing order price = {order_price}')
        return order_price
            
def create_buy_order(low_10_latest, token_pair, order_volume):
    buy_price = low_10_latest
    bought_price = buy_price
    trade = Trade(key=api_key, secret=secret_key)
    trade.create_order(
        ordertype="limit",
        side="buy",
        pair=token_pair,
        volume=order_volume,
        price=buy_price,
        oflags=["post", "fciq"]
    )
    return bought_price

def create_take_profit_order(take_profit, token_pair, token_balance):
    trade = Trade(key=api_key, secret=secret_key)
    trade.create_order(
        ordertype="limit",
        side="sell",
        pair=token_pair,
        volume=token_balance,
        price=take_profit,
        oflags=["post", "fcib"]
    )
    print(f'Take Profit Order created, Take Profit = {take_profit}, Volume = Token Balance @ {token_balance}')
   
def create_stop_loss_order(trigger_price, limit_price, stop_loss, token_pair, token_balance, stop_loss_delta):
    # Stop Loss SELL Order - Create a "stop-loss-limit" order requiring trigger price and limit price. 
    order_type_choice = "stop-loss-limit"
    # price = Trigger Price
    # price2 = Limit Price
    trade = Trade(key=api_key, secret=secret_key)
    trade.create_order(
        ordertype=order_type_choice,
        side="sell",
        pair=token_pair,
        volume=token_balance,
        price=trigger_price,  
        price2=limit_price, 
        oflags=["fciq"]
    )
    print(Fore.RED + f'STOP LOSS ORDER CREATED - trigger price = {trigger_price}, limit price = {limit_price}, price round value = {price_round_value}' + Style.RESET_ALL)

   
     
# Currently set to edit for take Profit only - Adjust this Later        
def edit_open_order(token_pair, orders, edit_price):
    for order_id, order_details in orders['open'].items():
        asset_pair = order_details['descr']['pair']
        if asset_pair == token_pair:
            print(Fore.RED + f'Revising Open order ID = {order_id}, Token {token_pair}.' + Style.RESET_ALL)
            print('Need to fix this process, check prices vs order to avoid constant failed edit attempts')
            # Initialize the Trade client with your API key and secret
            trade = Trade(key=api_key, secret=secret_key)
            # Edit an existing order
            trade.edit_order(
            txid=order_id,                   
            price=edit_price,
            pair=token_pair)
            print(Fore.RED + f'Edit Request sent, New Price = {edit_price}' + Style.RESET_ALL)
    
    
def cancel_matching_order(token_pair, orders):
    for order_id, order_details in orders['open'].items(): 
        #print(Fore.GREEN + f"Order ID: {order_id}" + Style.RESET_ALL)
        asset_pair = order_details['descr']['pair']
        if asset_pair == token_pair:
            #print(f'Asset Pair = {asset_pair} token_pair = {token_pair}.')
            print(f'Open order for {token_pair} found.')
            print(f"Type: {order_details['descr']['type']}, Order Type: {order_details['descr']['ordertype']}, Status: {order_details['status']}")
            print(f"Price: {order_details['descr']['price']}, Volume: {order_details['vol']}")
            # Cancel Order with Order ID matching asset_pair
            trade = Trade(key=api_key, secret=secret_key)
            trade.cancel_order(txid=order_id)
            print(Fore.RED + f'CANCELLED order ID {order_id}.' + Style.RESET_ALL)

def buy_check(low_10_latest, orders, token_pair):
    edit_price = low_10_latest 
    bought_price = edit_price
    print(Fore.CYAN + 'Run Buy-Check Function : Check Order Price vs Current.' + Style.RESET_ALL)
    edit_open_order(token_pair, orders, edit_price)
    check_delay = 120
    print(f'Delaying {check_delay} additional seconds, due to active buy order in place.')
    sleep(check_delay)
    # NOTE: print('Required for this function = order_action, Low_10, current_price, token, ??')
    #print(Fore.YELLOW + 'No BUY-CHECK action at this time - NOTE: MAY want to edit LATER' + Style.RESET_ALL)
    return bought_price

def buy_place(low_10_latest, token_pair):
    print(Fore.GREEN + f'Running Buy-Place Function : Place BUY Order. 10 Period Lowest Price = {low_10_latest}' + Style.RESET_ALL)
    bought_price = create_buy_order(low_10_latest, token_pair, order_volume)
    print(Fore.GREEN + f'Buy order created @ {low_10_latest}, bought_price = {bought_price}' + Style.RESET_ALL)
    print('Delaying 60 additional seconds, due to Placing buy order.')
    sleep(60)
    return bought_price
    
def sell_check(current_price, orders, buy_price, take_profit_delta, token_balance):
    # Edit this to use the Actual buy price 
    # buy_price is hardcoded, low_10 will change. How to confirm price?
    # Edit thresholds will trigger edits at 75% of SL or TP goals. 
    order_price = get_order_price(token_pair, orders)
    tp_edit_delta = 0.75 * take_profit_delta
    tp_threshold = buy_price + tp_edit_delta
    sl_edit_delta = 0.75 * stop_loss_delta
    sl_threshold = buy_price - sl_edit_delta
    print(Fore.YELLOW + 'Run Sell-Check Function : Check Sell Price, type = Sell' + Style.RESET_ALL)
    print(f'Check order price vs Current. Edit if current < 75%-SL @ {sl_threshold} OR  > 75%-TP @ {tp_threshold}') 
    if current_price > tp_threshold:
        print('Assure that TAKE PROFIT price is on ORDER')
        edit_price = take_profit
        if order_price == take_profit:
            print('Take Profit price already on order - No Change.')
        else:
            cancel_matching_order(token_pair, orders)
            create_take_profit_order(take_profit, token_pair, token_balance)
            print(Fore.GREEN + f'New TAKE PROFIT ORDER Created - Take Profit @ {take_profit}' + Style.RESET_ALL)   
    if current_price < sl_threshold:
        print(Fore.CYAN + f'SL Threshold Reached @ {sl_threshold} Current = {current_price}.Assure that STOP LOSS price is on ORDER' + Style.RESET_ALL)
        edit_price = stop_loss
        print(f'order_price = {order_price}, stop_loss = {stop_loss}, trigger_price = {trigger_price}')
        if order_price == stop_loss or order_price == trigger_price:
            print('Stop Loss price already on order - No Change.')
        else:
            cancel_matching_order(token_pair, orders)
            create_stop_loss_order(trigger_price, limit_price, stop_loss, token_pair, token_balance, stop_loss_delta)
            print(Fore.RED + f'CANCEL order and create Stop Loss Order - stop loss = {stop_loss}' + Style.RESET_ALL)                                                         
    else:
        print('Within SELL orders thresholds, no change. ')    
    return bought_price
    
def sell_place(take_profit, token_pair, token_balance):
    # order_volume = token_balance 
    print('Run Sell-Place Function')
    print(Fore.RED + 'Place SELL order.' + Style.RESET_ALL)
    create_take_profit_order(take_profit, token_pair, token_balance)
    
    
    
