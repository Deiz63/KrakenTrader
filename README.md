# KrakenTrader 
Python based utility to automate placing orders for trading tokens using Kraken Exchange API. 

WORK IN PROGRESS. 

INTRODUCTION
Project created to automate trading strategies for blockchain tokens using Kraken exchange.
Various API calls are used in a "status update loop". 

USAGE & FUNCTIONALITY
Choose a token or (Asset Pair) via Kraken exchange (i.e. SOLUSD), 
The program will initialy check OHLCV data to find the 10 period low for the LOW candle value.
It will also poll the API for the correct decimals to use in the 'price', and 'volume' fields, among other api calls. 
Assuming no orders exist, and we have no balance for this token, a BUY order will be placed for this 10 period low value. 
(All this can be altered to specific strategy)

The program will now delay and then continue to 'check status', and respond accordingly every few minutes. 
Check status = check balance and for any open orders matching the asset pair.
There are (4) possible conditions that will determine the next actions for each cycle. 
[Token Balance exists - T/F & An order for token exists - T/F] = Buy-Place FF, Buy-Check FT, Sell-Place TF, Sell-Check TT
The combination of these values will become the trigger to drive the next action.  

STRATEGY / OBSERVATIONS
The logic attempts to delay after order placement to allow some time for orders to place, and for the natural market movement.  
it also attempts to place 'limit' orders ASAP using predetermined price points. This gives a better chance for success of the limit orders being placed.

Currently the logic is cancelling and recreating orders quite often, 
which is in hopes of keeping the trading alive, and not getting "stuck" for too long if a particular price has is already far from the order price. 

Part of the process is also the fact that many of these placed orders will be unsuccessful, due to price being within the spread, etc.
When placing an order fails, it will typically recover and attempt the action again after next status update.
The check & re-check logic seems to do well accounting for all situations without many errors, but it all needs to be scrutinized further to develop profitable gains. 
 
