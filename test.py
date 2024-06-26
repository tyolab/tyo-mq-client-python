#!/usr/bin/env python3
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

from tyo_mq_client.message_queue import MessageQueue
from tyo_mq_client.socket import Socket
from tyo_mq_client.logger import Logger
from tyo_mq_client.constants import Constants

import json
import sys
import os

test = 0
subscriber = None
producer = None
ready = [False, False]

mq = MessageQueue()

server='mqserver'

print("Connecting to the tyo-mq server: {}".format(server))

# Test Socket
# socket = Socket()
# socket.connect()

# Test Subscriber
# subscriber = mq.createSubscriber("TYO Lab Tester")

event = "tyo-lab-event-test"

# Test Producer
producer = mq.createPublisher("TYO Lab", event, server, 17352, "websocket")
# producer.host = "https://c-its-emulator.herokuapp.com:443"
# producer.port = None
subscriber = mq.createConsumer("TYO Lab Tester", server, 17352, "websocket")

def on_message_published(message):
    print ("received message" + json.dumps(message))
    # sys.exit()
    os._exit(1)

def check ():
    if (ready[0] and ready[1]):
        producer.produce({"message": "Hello World"}, event)

def subscriber_on_connect () :
    Logger.log("Subscriber is connected")

    # after we connnect, we subscribe to the producer
    subscriber.subscribe(producer.name, event, on_message_published, False)

    ready[0] = True
    check()
    
def on_subscription (data) :
    print ("received subscription")
    # producer.produce({"message1": "Hello World"})
    # producer.on('test', on_message_published)
    # producer.socket.emit('test')
    # producer.produce({"message2": "Hello World"}, event, Constants.METHOD_BROADCAST)

def producer_on_connect () :
    Logger.log("Producer is connected")
    ready[1] = True
    producer.on_subscription_listener = on_subscription
    producer.on_subscriber_lost(on_subscriber_lost)
    check()
    # subscriber_on_connect() 

def on_subscriber_lost (data):
    message = json.dumps(data)
    message = json.loads(message)
    Logger.log('Informed that connection with a subscriber (' + message["consumer"] + ') was lost')    

#subscriber.add_on_connect_listener(subscriber_on_connect)
producer.add_on_connect_listener(producer_on_connect)

# subscriber.connect(-1)
producer.connect(-1, transports=['websocket'])

subscriber.add_on_connect_listener(subscriber_on_connect)

subscriber.connect(-1, transports=['websocket'])

Logger.log("Waiting for connection to be established")
producer.socket.wait()

# while ready[0] == False or ready[1] == False:
#     pass