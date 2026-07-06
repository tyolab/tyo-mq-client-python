"""A minimal tyo-mq round trip: produce on one connection, consume (durable,
auto-ACK) on another.

Start a server first (see https://github.com/tyolab/tyo-mq), then:

    python examples/pubsub.py [server-host] [port]
"""

import sys
import time

sys.path.insert(0, '.')  # run from the repo root without installing
from tyo_mq_client import MessageQueue

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = int(sys.argv[2]) if len(sys.argv) > 2 else 17352

mq = MessageQueue(host=host, port=port)
# With auth enabled on the server:
# mq = MessageQueue(host=host, port=port, auth={'token': 'my-token'})

received = []


def on_order(message, from_whom, ack, raw):
    print(f"received from {from_whom}: {message} (msgId: {raw.get('msgId')})")
    received.append(message)
    # ack() is called automatically after this handler returns, because the
    # subscription below sets ack=True without manual_ack.


consumer = mq.createConsumer('py-listener')
consumer.subscribe('py-example', 'order-placed', on_order,
                   options={'durable': True, 'ack': True})
consumer.connect()

producer = mq.createProducer('py-example')
producer.connect()

time.sleep(0.5)  # let both connections register
producer.produce({'orderId': 1001, 'total': 129.0}, 'order-placed')

deadline = time.time() + 10
while not received and time.time() < deadline:
    time.sleep(0.1)

producer.disconnect()
consumer.disconnect()

if received:
    print("round trip OK")
else:
    print("no message received before timeout", file=sys.stderr)
    sys.exit(1)
