from models.symbol_bar import symbol_bar
from models.symbol_quote import symbol_quote

from utils import utils

import json

# fix this error: TypeError: module() takes at most 2 arguments (3 given)  for inherit the symbol_bar class
class ohlc(symbol_bar):
    def __init__(self, open, high, low, close):
        symbol_bar.__init__(self, open, high, low, close)
        self.span = None
        self.broker = None
        self.market = None

    @classmethod
    def from_quote(cls, quote, broker = None, market = None):
        bar = None
        if quote.last > 0:
            bar = cls(quote.last, quote.last, quote.last, quote.last)
        elif quote.ask > 0 and quote.bid > 0:
            bar = cls(quote.bid, quote.ask, quote.bid, quote.bid)
        elif quote.bid > 0:
            bar = cls(quote.bid, quote.bid, quote.bid, quote.bid)
        elif quote.ask > 0:
            bar = cls(quote.ask, quote.ask, quote.ask, quote.ask)
        bar.broker = broker
        bar.market = market
        bar.time = quote.time
        bar.volume = quote.volume
        bar.symbol = quote.symbol
        return bar

    # the quote is symbol_quote type
    def update(self, quote: symbol_quote):
        if (quote.last > 0):
            self.close = quote.last
            if (self.high < quote.last):
                self.high = quote.last
            if (self.low > quote.last):
                self.low = quote.last
        else:
            if (quote.ask > 0 and quote.bid > 0):
                if (self.high < quote.ask):
                    self.high = quote.ask
                if (self.low > quote.bid):
                    self.low = quote.bid
                self.close = quote.bid
                self.span = quote.ask - quote.bid
            elif (quote.bid > 0):
                self.close = quote.bid
                if (self.high < quote.bid):
                    self.high = quote.bid
                if (self.low > quote.bid):
                    self.low = quote.bid
            elif (quote.ask > 0):
                self.close = quote.ask
                if (self.high < quote.ask):
                    self.high = quote.ask
                if (self.low > quote.ask):
                    self.low = quote.ask
        self.volume += quote.volume
        self.time = quote.time   

    def to_json(self):
        # return json.dumps(self, default=utils.json_default, sort_keys=False, indent=4)
        # handcrafed json without white space
        return """{\"symbol\": \"{}\", \"time\": \"{}\", \"open\": {}, \"high\": {}, \"low\": {}, \"close\": {}, \"volume\": {}, \"market\": \"{}\", \"broker\": \"{}\"}""".format(
            self.symbol, 
            self.time.isoformat(), 
            self.open, 
            self.high, 
            self.low, 
            self.close, 
            self.volume,
            self.market,
            self.broker
            )
    
    def to_line(self):
        return "{}, {}, {}, {}, {}, {}".format(self.time, self.open, self.high, self.low, self.close, self.volume)

