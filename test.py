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

server='localhost'

print("Connecting to the tyo-mq server: {}".format(server))

# Test Socket
# socket = Socket()
# socket.connect()

# Test Subscriber
# subscriber = mq.createSubscriber("TYO Lab Tester")

# Test Producer
producer = mq.createPublisher("TYO Lab")
subscriber = producer

def on_message_published(message):
    print ("received message" + json.dumps(message))
    # sys.exit()
    os._exit(1)

def check ():
    if (ready[0] and ready[1]):
        producer.produce({"message": "Hello World"})

def subscriber_on_connect () :
    Logger.log("Subscriber is connected")
    ready[0] = True
    subscriber.subscribe(producer.name, Constants.EVENT_DEFAULT, on_message_published, False)
    
def on_subscription (data) :
    print ("received subscription")
    producer.produce({"message1": "Hello World"})
    producer.on('test', on_message_published)
    producer.socket.emit('test')
    producer.produce({"message2": "Hello World"}, producer.eventDefault, Constants.METHOD_BROADCAST)

def producer_on_connect () :
    subscriber_on_connect() 

    Logger.log("Producer is connected")
    ready[1] = True
    producer.on_subscription_listener = on_subscription
    producer.on_subscriber_lost(on_subscriber_lost)

def on_subscriber_lost (data):
    message = json.dumps(data)
    Logger.log('Informed that connection with a subscriber (' + message["consumer"] + ') was lost')

#subscriber.add_on_connect_listener(subscriber_on_connect)
producer.add_on_connect_listener(producer_on_connect)

# subscriber.connect(-1)
producer.connect(-1)

