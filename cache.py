from datetime import timedelta, datetime

import constants
from models.market_symbol import market_symbol
from models.ohlc import ohlc

class cache:
    market_symbols = {}
    cache_map = dict()
    cache_map_m15 = dict()
    cache_map_day = dict()

    def __init__(self):
        pass

    @staticmethod
    def update_market_symbol(broker_symbol, market = None, symbol = None, update = False):
        if broker_symbol in cache.market_symbols:
            if (update is False):
                return
            
            cache.market_symbols[broker_symbol].symbol = broker_symbol
            cache.market_symbols[broker_symbol].market = market
            cache.market_symbols[broker_symbol].symbol = symbol

        else:
            cache.market_symbols[broker_symbol] = market_symbol(broker_symbol, market, broker_symbol)

    @staticmethod
    def update(quote, broker = None, market = None, gmt_offset = 0):

        bars = None
        bar = None
        key = quote.symbol
        old_bar = cache.cache_map.get(key)
        old_bar_m15 = cache.cache_map_m15.get(key)
        old_bar_day = cache.cache_map_day.get(key)

        if old_bar is not None:
            bar_time = old_bar.time
            quote_time = quote.time

            if bar_time > quote_time:
                return None

            if bar_time.minute != quote_time.minute:
                # new minute bar
                bars = [old_bar]
                cache.cache_map[key] = ohlc.from_quote(quote, broker, market)

                old_mod = int(bar_time.minute / 15) % 4
                new_mod = int(quote_time.minute / 15) % 4

                if old_mod != new_mod:
                    # new 15 minute bar
                    bars.append(old_bar_m15)
                    cache.cache_map_m15[key] = ohlc.from_quote(quote, broker, market)
                else:
                    old_bar_m15.update(quote)

                server_time = quote_time + timedelta(hours = gmt_offset)
                time = bar_time + timedelta(hours = gmt_offset)
                if time.day != server_time.day:
                    # new day bar
                    cache.cache_map_day[key] = ohlc.from_quote(quote, broker, market)
                else:
                    old_bar_day.update(quote)

            else:
                old_bar.update(quote)
                old_bar_m15.update(quote)
                old_bar_day.update(quote)
            
        else:
            cache.cache_map[key] = ohlc.from_quote(quote, broker, market)
            cache.cache_map_m15[key] = ohlc.from_quote(quote, broker, market)
            cache.cache_map_day[key] = ohlc.from_quote(quote, broker, market)
        return bars

