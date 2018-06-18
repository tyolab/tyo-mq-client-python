#!/usr/bin/env python3
from lib.message_queue import MessageQueue
from lib.socket import Socket
from lib.logger import Logger

import json

test = 0
subscriber = None
producer = None
ready = (False, False)

def on_message_published(data, fromWhom):
    if (fromWhom is not None):
        print("Received message from", fromWhom)

    test += 1
    if (data == 'test-a'):
        print('test1 succeeded!')
    else:
        print('test1 failed')

    if (test == 2):
        subscriber.disconnect()

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

def subscriber_on_connect () :
    ready[0] = True
    subscriber.subscribe(producer.name, 'tyo-mq-mt-default', on_message_published, False)

def producer_on_connect () : 
    ready[1] = True

def on_subscriber_lost (data):
    test += 1
    message = json.dumps(data)
    Logger.log('Informed that connection with a subscriber (' + message["consumer"] + ') was lost')


def test():


subscriber.add_on_connect_listener(subscriber_on_connect)
producer.on_subscriber_lost(on_subscriber_lost)

subscriber.connect(-1)
producer.connect(-1)
