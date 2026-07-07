# tyo-mq-client-python

A Python client for **[tyo-mq](https://github.com/tyolab/tyo-mq)** — the
distributed pub/sub messaging service with durable delivery (ACK / retry /
dead-letter queue), MQTT-style topic wildcards, consumer groups, and
multi-tenant auth realms.

Built on `python-socketio` (Socket.IO v4). Python 3.8+.

## Install

```bash
pip install tyo-mq-client
```

You'll need a running tyo-mq server:
`npm install tyo-mq && node -e "new (require('tyo-mq').Server)().start()"`,
or Docker — see the [server repo](https://github.com/tyolab/tyo-mq).

## Quick start

```python
from tyo_mq_client import MessageQueue

mq = MessageQueue(host='localhost', port=17352)
# with auth enabled on the server:
# mq = MessageQueue(auth={'token': 'my-token'})

# consume
consumer = mq.createConsumer('email-service')
consumer.subscribe('order-service', 'order-placed',
                   lambda order: print('sending confirmation for', order))
consumer.connect()

# produce
producer = mq.createProducer('order-service')
producer.connect()
producer.produce({'orderId': 1001}, 'order-placed')
```

Connections run on a background thread; call `consumer.wait()` to block a
worker process on the connection, and `disconnect()` to stop.

## Durable delivery, ACK, and retry

```python
def handle(message, from_whom, ack, raw):
    do_work(message)          # raising skips the auto-ACK → server retries

consumer.subscribe('order-service', 'payment', handle, options={
    'durable': True,          # queue while this consumer is offline
    'ack': True,              # auto-ACK after the handler returns
    'retry': {'max_attempts': 3, 'delay': '5s', 'backoff': 'exponential'},
})
```

With `'manual_ack': True` (plus e.g. `'ack_timeout': '30s'`) the handler
receives an `ack` callable and acknowledges only when the work truly
succeeded; unacknowledged deliveries are retried on the schedule and
dead-lettered when attempts run out. Handlers may accept 1–4 arguments:
`(message)`, `(message, from)`, `(message, from, ack)`, or
`(message, from, ack, raw)`.

## Topics, groups, broadcast

```python
# MQTT-style wildcards: + is one level, # is the rest
consumer.subscribe_topic('orders/+/status', handler)
consumer.subscribe_topic('factory/#', handler, {'durable': True, 'ack': True})

# consumer groups load-balance across workers
consumer.subscribe('dispatcher', 'jobs', handler, options={'group': 'workers'})

# broadcast one copy to every realm member, or every group member
producer.broadcast({'notice': 'maintenance at 22:00'}, 'announcement')
producer.broadcast({'cmd': 'reload'}, 'control', group='workers')
```

Large messages are chunked automatically in both directions (256 KB frames),
matching the Node.js client.

## Note on the produce signature

`produce(data, event)` — data first, then the event name — kept for
compatibility with existing users of this client. (The Node.js client is
`produce(event, data)`.)

## Other clients

Node.js (and browsers) ships with the [server package](https://github.com/tyolab/tyo-mq);
see also [Go](https://github.com/tyolab/tyo-mq-client-go),
[Rust](https://github.com/tyolab/tyo-mq-client-rust),
[C/C++](https://github.com/tyolab/tyo-mq-client-cpp),
[Ruby](https://github.com/tyolab/tyo-mq-client-ruby),
[Java](https://github.com/tyolab/tyo-mq-client-java), and
[C#](https://github.com/tyolab/tyo-mq-client-csharp).

All clients are exercised together by the cross-language
[conformance suite](https://github.com/tyolab/tyo-mq-conformance), which runs
the same pub/sub, durable-delivery, topic, group, and auth scenarios against
every client (and every producer/consumer language pair) and publishes the
resulting matrix.

## License

Apache-2.0. Built by [TYO Lab](https://tyo.com.au).
