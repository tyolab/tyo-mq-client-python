#!/usr/bin/env python3
import sys
import logging
logging.getLogger('tyosis-data').setLevel(logging.DEBUG)
logging.basicConfig()

from tyo_mq_client.message_queue import MessageQueue

publisher = None
subscriber = None

user = None
password = None
host = None

broker = None

# checking the parameters
mq_host = 'localhost'
mq_port = 17352
mq_protocol = 'websocket'

id = None

app_name = None
app_id = None

server_count = 10

if len(sys.argv) > 1:
    # looping through the arguments
    for i in range(1, len(sys.argv)):
        first_char = sys.argv[i][0]
        if first_char == '-':
            cmd = sys.argv[i][1]
            if cmd == 'h':
                host = sys.argv[i + 1]
            elif cmd == 'p':
                port = int(sys.argv[i + 1])
            elif cmd == 't':
                protocol = sys.argv[i + 1]
            elif cmd == '-':
                # long command, substring the first 2 characters
                cmd = sys.argv[i][2:]
                if cmd == 'mq-host':
                    mq_host = sys.argv[i + 1]
                elif cmd == 'mq-port':
                    mq_port = int(sys.argv[i + 1])
                elif cmd == 'mq-protocol':
                    mq_protocol = sys.argv[i + 1]
                elif cmd == 'user':
                    user = sys.argv[i + 1]
                elif cmd == 'password':
                    password = sys.argv[i + 1]
                elif cmd == 'host':
                    host = sys.argv[i + 1]
                elif cmd == 'id':
                    id = sys.argv[i + 1]
                elif cmd == 'server-count':
                    server_count = int(sys.argv[i + 1])
                elif cmd == 'broker':
                    broker = sys.argv[i + 1]
                
                elif cmd == 'help':
                    print('Usage: tyosis-gateway.py [options]')
                    print('Options:')
                    print('  -h <host>         Message Queue Host')
                    print('  -p <port>         Message Queue Port')
                    print('  -t <protocol>     Message Queue Protocol')
                    print('  --mq-host <host>  Message Queue Host')
                    print('  --mq-port <port>  Message Queue Port')
                    print('  --mq-protocol <protocol>  Message Queue Protocol')
                    print('  --help            Display this help message')
                    sys.exit()
                
if user is None:
    sys.exit('User is required')

if password is None:
    sys.exit('Password is required')

if host is None:
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

def on_command (message):
    print ("received command: " + message)
    cmd = json.loads(message)
    handle_command(cmd.Message)

def handle_command (message):
    # split the message by space
    parts = message.split(' ')
    cmd = parts[0]
    if (cmd == 'subscribe'):
        print ("subscribing to the quote" + parts[1])
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
    
        # subscribe("TYO")

def on_quote_update(quote):
    print ("received quote: " + quote)
           
def subscribe(symbol):
    print ("subscribing to the quote")
    

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

mq = MessageQueue()
publisher = mq.createPublisher(app_name, "quote", mq_host, mq_port, mq_protocol)
subscriber = mq.createConsumer(app_id, mq_host, mq_port, mq_protocol)

publisher.add_on_connect_listener(producer_on_connect)
subscriber.add_on_connect_listener(subscriber_on_connect)

publisher.connect(-1, transports=['websocket'])
subscriber.connect(-1)

publisher.socket.wait()
