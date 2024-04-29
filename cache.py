import constants
from models.market_symbol import market_symbol

class cache:
    market_symbols = {}

    def __init__(self):
        pass

    @staticmethod
    def update_market_symbol(self, symbol, market = None, broker_symbol = None, update = False):
        if symbol in cache.market_symbols:
            if (update is False):
                return
            
            cache.market_symbols[symbol].symbol = symbol
            cache.market_symbols[symbol].market = market
            cache.market_symbols[symbol].broker_symbol = broker_symbol

        else:
            cache.market_symbols[symbol] = market_symbol(symbol, market, broker_symbol)