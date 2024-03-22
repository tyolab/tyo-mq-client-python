#!/usr/bin/env python3
import sys
import logging
logging.getLogger('tyosis-data').setLevel(logging.DEBUG)
logging.basicConfig()

from tyo_mq_client.message_queue import MessageQueue

publisher = None
subscriber = None

# checking the parameters
mq_host = 'localhost'
mq_port = 17352
mq_protocol = 'websocket'

if len(sys.argv) > 1:
    # looping through the arguments
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-h':
            mq_host = sys.argv[i + 1]
        elif sys.argv[i] == '-p':
            mq_port = int(sys.argv[i + 1])
        elif sys.argv[i] == '-t':
            mq_protocol = sys.argv[i + 1]
    mq_host = sys.argv[1]


mq = MessageQueue()