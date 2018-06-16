#!/usr/bin/env python3
from lib.message_queue import MessageQueue

from lib.socket import Socket


mq = MessageQueue()

server='localhost'

print("Connecting to the tyo-mq server: {}".format(server))

# Test Socket
# socket = Socket()
# socket.connect()

# Test Subscriber
subscriber = mq.createSubscriber("TYO Lab Tester")
subscriber.connect(4)

# Test Producer
producer = mq.createPublisher("TYO Lab")
producer.connect(4)
