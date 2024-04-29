#!/usr/bin/env python3

import sys
import os
import logging
logging.getLogger('tyosis-data').setLevel(logging.DEBUG)
logging.basicConfig()

import threading
# Now start the terminal
import MetaTrader5 as mt5
import pytz

import json

import threading
from datetime import timedelta, datetime

from tyo_mq_client.message_queue import MessageQueue

import constants
from cache import cache
from models import market_symbol

publisher = None
subscriber = None

account = None
password = None
server = None

broker = None

# checking the parameters
mq = None
mq_host = 'localhost'
mq_port = 17352
mq_protocol = 'websocket'

id = None

app_name = None
app_id = None

account_type = 1

server_count = 10

if len(sys.argv) > 1:
    # looping through the arguments
    for i in range(1, len(sys.argv)):
        first_char = sys.argv[i][0]
        if first_char == '-':
            cmd = sys.argv[i][1]
            if cmd == 'h':
                server = sys.argv[i + 1]
            elif cmd == 'p':
                port = int(sys.argv[i + 1])
            elif cmd == 't':
                protocol = sys.argv[i + 1]
            elif cmd == '-':
                # long command, substring the first 2 characters
                cmd = sys.argv[i][2:]
                if cmd == 'mq-server':
                    mq_host = sys.argv[i + 1]
                elif cmd == 'mq-port':
                    mq_port = int(sys.argv[i + 1])
                elif cmd == 'mq-protocol':
                    mq_protocol = sys.argv[i + 1]
                elif cmd == 'login':
                    account = int(sys.argv[i + 1])
                elif cmd == 'password':
                    password = sys.argv[i + 1]
                elif cmd == 'server':
                    server = sys.argv[i + 1]
                elif cmd == 'id':
                    id = sys.argv[i + 1]
                elif cmd == 'server-count':
                    server_count = int(sys.argv[i + 1])
                elif cmd == 'broker':
                    broker = sys.argv[i + 1]
                elif cmd == 'account_type':
                    account_type = int(sys.argv[i + 1])
                
                elif cmd == 'help':
                    print('Usage: tyosis-gateway.py [options]')
                    print('Options:')
                    print('  -h <host>         Message Queue Host')
                    print('  -p <port>         Message Queue Port')
                    print('  -t <protocol>     Message Queue Protocol')
                    print('  --mq-server <host>  Message Queue Host')
                    print('  --mq-port <port>  Message Queue Port')
                    print('  --mq-protocol <protocol>  Message Queue Protocol')
                    print('  --help            Display this help message')
                    sys.exit()
                
if account is None:
    sys.exit('Login is required')

if password is None:
    sys.exit('Password is required')

if server is None:
    sys.exit('Host is required')

if id is None:
    sys.exit('ID is required')

if broker is None:
    sys.exit('Broker is required')

###################### MAIN ######################
# tyosis_server = None
server_id = "tyostocks-server-producer"

app_name = "tyosis-data"
app_id = app_name + id

broker_info_dict = {}
broker_info_dict["broker"] = broker
broker_info_dict["account"] = account
broker_info_dict["account_type"] = account_type     #/**   * 0 - raw  * 1 - standard  */
broker_info_dict["app_id"] = app_id

symbols = None
# Set Type
symbols_subscribed = set()
symbols_last_update_dict = {}

# mt5 = None
timezone = pytz.timezone("Etc/UTC")

def on_command (message):
    print ("received command: " + message)
    cmd = json.loads(message)
    to_broker = cmd['To']
    to_broker_id = None
    if 'ToId' in cmd:
        cmd['ToId']

    if to_broker is not None and to_broker != broker:
        print ("Broker does not match, not for this broker: " + broker)
        return
    
    if to_broker_id is None or to_broker_id == -1:
        pass
    else:
        if to_broker_id != id:
            print ("Broker ID does not match, not for this broker: " + broker + " ID: " + to_broker_id)

    handle_command(cmd['Message'])

def handle_command (message):
    # split the message by space
    parts = message.split(' ')
    cmd = parts[0]
    if (cmd == 'subscribe'):
        print ("subscribing ", parts[1])
        subscribe_to_symbols = parts[1].split(',')
        for symbol in subscribe_to_symbols:
            tokens = symbol.split(':')
            broker_symbol = None
            market = None
            a_symbol= None
            if len(tokens) > 2:
                broker_symbol = tokens[2]
                market = tokens[1]
            elif len(tokens) > 1:
                market = tokens[1]
            a_symbol = tokens[0]

            if len(tokens) > 1:
                cache.update_market_symbol(a_symbol, market, broker_symbol)

            subscribe_quote(a_symbol)

    elif (cmd == 'unsubscribe'):
        print ("unsubscribing to the quote" + parts[1])
    elif (cmd == 'order'):
        print ("sending order: " + parts[1])
        # if (parts.Length < 4) {
        #         Console.WriteLine("Invalid order command, need at least 5 parameters including command, symbol,order type and volume, optional price (if not market buy/sell), stop loss, take profit and comment");
        #         return -1;
        #     }

        #     var type = Int32.Parse(parts[2]);
        #     var volume = Double.Parse(parts[3]);
            
        #     var price = 0.0;
        #     if (parts.Length > 4) {
        #         price = Double.Parse(parts[4]);
        #     }

        #     double stop_loss = 0.0;
        #     double take_profit = 0.0;
        #     if (parts.Length > 5) {
        #         stop_loss = Double.Parse(parts[5]);
        #     }
        #     if (parts.Length > 6) {
        #         take_profit = Double.Parse(parts[6]);
        #     }
        #     string comment = "";
        #     if (parts.Length > 7) {
        #         comment = parts[7];
        #     }

        #     var order = place_order(
        #         parts[1], // symbol
        #         type, // tyosis order type
        #         price, // price
        #         volume, // volume / lots
        #         stop_loss, // stop loss
        #         take_profit, // take profit
        #         comment // comment
        #     );
    elif (cmd == 'close'):
        print ("closing order: " + parts[1])
    elif (cmd == 'closeall'):
        print ("closing all orders")
    elif (cmd == 'load'):
        print ("loading historical data")
        #         // load data
        # // we will have a full month worth of data (1 minute interval)
        # //
        # var symbol = parts[1];
        # var market = parts[2];
        # var prefix = parts.Length > 3 ? parts[3] : "";
        # var suffix = parts.Length > 4 ? parts[4] : "";
        # var period = parts.Length > 5 ? Int32.Parse(parts[5]) : 7;
        # var delay = parts.Length > 6 ? Int32.Parse(parts[6]) : 20;

        # if (prefix == ".")
        #     prefix = "";

        # if (suffix == ".")
        #     suffix = "";

        # Thread t = new Thread(() => {
        #     load_data(symbol, market, prefix, suffix, period, delay);
        # });
    elif (cmd == 'opened'):
        print ("getting opened orders")
        #         var orders = mt5.get_opened_orders();
        # if (null != orders) {
        #     foreach (var order in orders) {
        #         Console.WriteLine("Opened Order, ticket: " + order.Ticket + ", symbol: " + order.Symbol + ", volume: " + order.Lots + ", price: " + order.OpenPrice + ", type: " + order.OrderType + ", profit: " + order.Profit + ", profit rate: " + order.ProfitRate + ", open time: " + order.OpenTime);

        #         Thread t = new Thread(() => {
        #             string msg = $"{{\"ticket\": {order.Ticket}, \"symbol\": \"{order.Symbol}\", \"volume\": {order.Lots}, \"price\": {order.OpenPrice}, \"type\": {mt5.to_type(order.OrderType)}, \"stop_loss\": {order.StopLoss}, \"take_profit\": {order.TakeProfit}, \"comment\": \"{order.Comment}\", \"profit\": {order.Profit}, \"profit_rate\": {order.ProfitRate}, \"open_time\": \"{order.OpenTime}\"}}";
        #             #if DEBUG
        #             Console.WriteLine("Sending existing order message: " + msg);
        #             #endif
        #             publisher.produce(JsonEncodedText.Encode(msg).ToString(), "new_order");
        #         });
        #         t.Start();
        #         Thread.Sleep(1000);
        #     }
        # }
    elif (cmd == 'symbols'):
        print ("getting symbols")

    
        # subscribe("TYO")

def on_quote_update(quote):
    print ("received quote: " + quote)      

###################### END #######################
    
def subscriber_on_connect () :
    # Logger.log("Subscriber is connected")
    print ("Subscriber is connected")

    # after we connnect, we subscribe to the producer
    # loop server count
    for i in range(server_count):
        if (i == 0):
            tyosis_server = server_id
        else:
            tyosis_server = server_id + str(i)
        subscriber.subscribe(tyosis_server, "data-command", on_command)

def producer_on_connect () :
    # Logger.log("Producer is connected")
    print ("Producer is connected")

def connect_to_mq():
    print ("Connecting to the message queue host " + mq_host + " on port " + str(mq_port) + " using protocol " + mq_protocol)

    publisher.add_on_connect_listener(producer_on_connect)
    subscriber.add_on_connect_listener(subscriber_on_connect)

    publisher.connect(-1)
    subscriber.connect(-1)

def get_data_file (date, symbol, market, timeframe, create_dir = False):
    # (DateTime date, string symbol, string market, int timeframe, bool create_dir = false) 
    # {
    #     var minutes_dir = (timeframe > 1 ? timeframe.ToString() : "") + "minutes";
    #     var dir = "data" + Path.DirectorySeparatorChar.ToString() + 
    #                 minutes_dir + Path.DirectorySeparatorChar.ToString() +
    #                 market + Path.DirectorySeparatorChar.ToString() +
    #                 symbol + Path.DirectorySeparatorChar.ToString() +
    #                 date.Year + Path.DirectorySeparatorChar.ToString();
    #     if (!File.Exists(dir) && create_dir) {
    #         try {
    #             Directory.CreateDirectory(dir);
    #         }
    #         catch (Exception e) {
    #             Logger.error("Error creating directory: " + dir + ", error: " + e.Message);
    #             Logger.error(e);
    #         }
    #     }
    #     return (dir +
    #                 date.ToString("yyyyMMdd") + ".txt");
    # }
    minutes_dir = str(timeframe) if timeframe > 1 else ""
    dir = "data" + os.path.sep + minutes_dir + os.path.sep + market + os.path.sep + symbol + os.path.sep + str(date.year) + os.path.sep
    if not os.path.exists(dir) and create_dir:
        try:
            os.makedirs(dir)
        except Exception as e:
            print("Error creating directory: " + dir + ", error: " + e)
            print(e)
    return dir + date.strftime("%Y%m%d") + ".txt"

def load_data(symbol, market, prefix, suffix, period, delay):
    print ("loading data for " + symbol)

def subscribe_quote (symbol):
    print ("subscribing to the quote: " + symbol)
    symbols_subscribed.add(symbol)

def get_tick_update(symbol):
    print ("getting tick update for symbol: " + symbol)
    # Most servers set the time to UTC+3
    server_now = datetime.now(timezone) + timedelta(hours=3) # UTC+3;
    utc_from = None
    # check if exists in symbols_last_update_dict
    if symbol in symbols_last_update_dict:
        utc_from = symbols_last_update_dict[symbol]
    else:
        utc_from = server_now - timedelta(minutes=2)
        symbols_last_update_dict[symbol] = utc_from

    # print the time (utc_from)
    print("UTC Time:", server_now)
    print("From UTC Time:", utc_from)
    # var symbol = "BTCUSD";
    ticks = mt5.copy_ticks_from(symbol, utc_from, 100, mt5.COPY_TICKS_ALL)
    if ticks is None or len(ticks) == 0:
        print("No ticks received from ", utc_from, "for ", symbol)
        return
    
    print("Ticks received:", len(ticks))
    # print("Displaying the last 10 ticks:")
    count = 0
    # for tick in ticks[:10]:
    # loop ticks from top to bottom
    for tick in reversed(ticks):
        # print the time of the tick
        # named time, bid, ask, last and flags 
        # convert ecpoch to datetime
        time = datetime.fromtimestamp(tick[0])
        # conver time to native with timezone
        time = time.astimezone(timezone)

        if count == 0:
            symbols_last_update_dict[symbol] = time

        # print(time, tick[1], tick[2], tick[3], tick[4])
        # format print
        print("#", count, "Time: ", time, "Bid: ", tick[1], "Ask: ", tick[2], "Last: ", tick[3], "Flags: ", tick[4])

        # break when time is older than utc_from
        if time < utc_from:
            # print("Breaking the loop")
            break
        count += 1

# Check updates for all subscribed symbols
def check_updates():
    # print ("checking for updates") 
    for symbol in symbols_subscribed:
        # get_tick_update(symbol)
        threading.Thread(target=get_tick_update, args=(symbol,)).start()
    set_timer()

def set_timer():
    threading.Timer(5.0, check_updates).start()     

####################################################################

def main():
    # display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # C:\Program Files\MetaTrader 5
    path = "C:\\Program Files\\EightCap MetaTrader 5\\terminal64.exe"	# path to MetaTrader 5 terminal
    # path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    timeout = 1000000
    portable = False
    # establish connection to the MetaTrader 5 terminal
    # login=login, password=password, portable=portable, timeout=timeout, 
    if not mt5.initialize(path=path, portable=portable, timeout=timeout):
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # display data on the MetaTrader 5 package
    terminal_info = mt5.terminal_info()
    print("MetaTrader 5 package:",terminal_info)
    # TerminalInfo(community_account=True,
    #              community_connection=False, connected=True,
    #              dlls_allowed=False, trade_allowed=False,
    #              tradeapi_disabled=False,email_enabled=False, 
    #              ftp_enabled=False, notifications_enabled=False, 
    #              mqid=True, build=3391,
    #              maxbars=100000, codepage=0, ping_last=258801,
    #              community_balance=0.0, retransmission=0.0, 
    #              company='FXOpen Investments Inc.', name='MetaTrader 5 - FXOpen',
    #              language='English', path='your path', data_path='your data path', 
    #              commondata_path='your common data path')

    
    # connect to the trade account specifying a password and a server
    print("Login to the trade account with login={}, password={}, server={}".format(account, password, server))
    authorized=mt5.login(account, password=password, server=server, timeout=timeout)
    if authorized:
        print("Login successful")
        # get account information
        # display trading account data in the form of a dictionary
        account_info = mt5.account_info()._asdict()
        for prop in account_info:
            print("  {}={}".format(prop, account_info[prop]))
        print()
        # Example output:
        # login=25115284
        # trade_mode=0
        # leverage=100
        # limit_orders=200
        # margin_so_mode=0
        # trade_allowed=True
        # trade_expert=True
        # margin_mode=2
        # currency_digits=2
        # fifo_close=False
        # balance=99511.4
        # credit=0.0
        # profit=41.82
        # equity=99553.22
        # margin=98.18
        # margin_free=99455.04
        # margin_level=101398.67590140559
        # margin_so_call=50.0
        # margin_so_so=30.0
        # margin_initial=0.0
        # margin_maintenance=0.0
        # assets=0.0
        # liabilities=0.0
        # commission_blocked=0.0
        # server=MetaQuotes-Demo
        # currency=USD
        # company=MetaQuotes Software Corp.

        # get all symbols information
        # get all symbols
        symbols=mt5.symbols_get()
        print('Symbols: ', len(symbols))
        count=0
        # # display the first five ones
        for s in symbols:
            count+=1
            print("{}. {}".format(count,s.name))
            if count==5: 
                print(s)
                break
        print()

        # threading.Thread(target=get_tick_update, args=("BTCUSD",)).start()
        # symbols_subscribed.add("BTCUSD")
        # symbols_subscribed.add("FMG")
        # symbols_subscribed.add("ASX200")
        # symbols_subscribed.add("AUDUSD")
        # symbols_subscribed.add("NDX100")
        # symbols_subscribed.add("XAUUSD")
        # symbols_subscribed.add("EURUSD")

        set_timer()

        print("Waiting for updates")
    else: 
        print("Failed to connect to the trade account with error code =", mt5.last_error())
        # mt5.shutdown()
        # sys.exit(1)

mq = MessageQueue()
publisher = mq.createPublisher(app_name, "quote", mq_host, mq_port, mq_protocol)
subscriber = mq.createConsumer(app_id, mq_host, mq_port, mq_protocol)        

connect_to_mq()

main()

publisher.socket.wait()
subscriber.socket.wait()    