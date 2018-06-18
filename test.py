#!/usr/bin/env python3
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

from lib.message_queue import MessageQueue
from lib.socket import Socket
from lib.logger import Logger
from lib.constants import Constants

import json

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
subscriber = mq.createSubscriber("TYO Lab Tester")

# Test Producer
producer = mq.createPublisher("TYO Lab")

def on_message_published(*args):
    print ("received message")
    # if (fromWhom is not None):
    #     print("Received message from", json.dumps(fromWhom))

    # test += 1
    # if (data == 'test-a'):
    #     print('test1 succeeded!')
    # else:
    #     print('test1 failed')

    # if (test == 2):
    subscriber.disconnect()

def check ():
    if (ready[0] and ready[1]):
        producer.produce({"message": "Hello World"})

def subscriber_on_connect () :
    Logger.log("Subscriber is connected")
    ready[0] = True
    subscriber.subscribe(producer.name, Constants.EVENT_DEFAULT, on_message_published, False)
    producer.connect(-1)

def on_subscription () :
    print ("received subscription")

def producer_on_connect () : 
    Logger.log("Producer is connected")
    ready[1] = True
    producer.on_subscription_listener = on_subscription
    producer.on_subscriber_lost(on_subscriber_lost)
    producer.produce({"message": "Hello World"})
    producer.on('test', on_message_published)
    producer.socket.emit('test')

def on_subscriber_lost (data):
    # test += 1
    message = json.dumps(data)
    Logger.log('Informed that connection with a subscriber (' + message["consumer"] + ') was lost')
    producer.disconnect()

subscriber.add_on_connect_listener(subscriber_on_connect)
producer.add_on_connect_listener(producer_on_connect)

subscriber.connect(-1)

