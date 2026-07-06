"""
tyo_mq_client — Python client for the tyo-mq messaging service.

    from tyo_mq_client import MessageQueue

    mq = MessageQueue(host='localhost')
    producer = mq.createProducer('order-service')
    producer.connect()
    producer.produce({'orderId': 1001}, 'order-placed')

    consumer = mq.createConsumer('email-service')
    consumer.subscribe('order-service', 'order-placed', print)
    consumer.connect()

See https://github.com/tyolab/tyo-mq for the server.
"""

__version__ = "0.3.0"

from .constants import Constants
from .events import Events
from .logger import Logger
from .message_queue import MessageQueue
from .publisher import Publisher
from .subscriber import Subscriber

# Friendly aliases matching the Node.js client
Factory = MessageQueue
Producer = Publisher
Consumer = Subscriber

__all__ = [
    "MessageQueue", "Factory",
    "Publisher", "Producer",
    "Subscriber", "Consumer",
    "Constants", "Events", "Logger",
]
