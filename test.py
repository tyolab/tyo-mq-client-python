#!/usr/bin/env python3
from lib.message_queue import MessageQueue

mq = MessageQueue()

server='localhost'

print("Connecting to the tyo-mq server: {}".format(server))