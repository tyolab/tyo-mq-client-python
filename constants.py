from models.market_symbol import market_symbol

class constants:
    common_symbols = {}

    # Crypto
    common_symbols['BTCUSD'] = market_symbol('BTCUSD', 'crypto')  # Bitcoin to USD
    common_symbols['ETHUSD'] = market_symbol('ETHUSD', 'crypto')
    common_symbols['XRPUSD'] = market_symbol('XRPUSD', 'crypto')
    common_symbols['LTCUSD'] = market_symbol('LTCUSD', 'crypto')
    common_symbols['BCHUSD'] = market_symbol('BCHUSD', 'crypto')
    common_symbols['EOSUSD'] = market_symbol('EOSUSD', 'crypto')
    common_symbols['XLMUSD'] = market_symbol('XLMUSD', 'crypto') 
    common_symbols['ADAUSD'] = market_symbol('ADAUSD', 'crypto')  # Cardano to USD
    common_symbols['TRXUSD'] = market_symbol('TRXUSD', 'crypto')  # Tron to USD
    common_symbols['NEOUSD'] = market_symbol('NEOUSD', 'crypto')  # Neo to USD
    common_symbols['DASHUSD'] = market_symbol('DASHUSD', 'crypto')  # Dash to USD

    # Forex
    common_symbols['EURUSD'] = market_symbol('EURUSD', 'forex')  # Euro to USD
    common_symbols['GBPUSD'] = market_symbol('GBPUSD', 'forex')  # British Pound to USD
    common_symbols['AUDUSD'] = market_symbol('AUDUSD', 'forex')  # Australian Dollar to USD
    common_symbols['AUDEUR'] = market_symbol('AUDEUR', 'forex')  # Australian Dollar to Euro
    common_symbols['AUDGBP'] = market_symbol('AUDGBP', 'forex')  # Australian Dollar to British Pound
    common_symbols['AUDNZD'] = market_symbol('AUDNZD', 'forex')  # Australian Dollar to New Zealand Dollar
    common_symbols['AUDCAD'] = market_symbol('AUDCAD', 'forex')  # Australian Dollar to Canadian Dollar
    common_symbols['AUDCHF'] = market_symbol('AUDCHF', 'forex')  # Australian Dollar to Swiss Franc
    common_symbols['AUDJPY'] = market_symbol('AUDJPY', 'forex')  # Australian Dollar to Japanese Yen
    common_symbols['AUDZAR'] = market_symbol('AUDZAR', 'forex')  # Australian Dollar to South African Rand
    common_symbols['NZDUSD'	] = market_symbol('NZDUSD', 'forex')  # New Zealand Dollar to USD
    common_symbols['CADUSD'] = market_symbol('CADUSD', 'forex')  # Canadian Dollar to USD
    common_symbols['CHFUSD'] = market_symbol('CHFUSD', 'forex')  # Swiss Franc to USD
    common_symbols['JPYUSD'] = market_symbol('JPYUSD', 'forex')  # Japanese Yen to USD
    common_symbols['ZARUSD'] = market_symbol('ZARUSD', 'forex')  # South African Rand to USD
    common_symbols['HKDUSD'] = market_symbol('HKDUSD', 'forex')  # Hong Kong Dollar to USD
    common_symbols['SGDUSD'] = market_symbol('SGDUSD', 'forex')  # Singapore Dollar to USD
    common_symbols['SEKUSD'] = market_symbol('SEKUSD', 'forex')  # Swedish Krona to USD
    common_symbols['NOKUSD'] = market_symbol('NOKUSD', 'forex')  # Norwegian Krone to USD
    common_symbols['TRYUSD'] = market_symbol('TRYUSD', 'forex')  # Turkish Lira to USD
    common_symbols['MXNUSD'] = market_symbol('MXNUSD', 'forex')  # Mexican Peso to USD
    common_symbols['PLNUSD'] = market_symbol('PLNUSD', 'forex')  # Polish Zloty to USD
    common_symbols['RUBUSD'] = market_symbol('RUBUSD', 'forex')  # Russian Ruble to USD
    common_symbols['INRUSD'] = market_symbol('INRUSD', 'forex')  # Indian Rupee to USD
    common_symbols['BRLUSD'] = market_symbol('BRLUSD', 'forex')  # Brazilian Real to USD
    common_symbols['CNYUSD'] = market_symbol('CNYUSD', 'forex')  # Chinese Yuan to USD
    common_symbols['CNHUSD'] = market_symbol('CNHUSD', 'forex')  # Chinese Yuan Offshore to USD
    common_symbols['KRWUSD'] = market_symbol('KRWUSD', 'forex')  # South Korean Won to USD
    common_symbols['TWDUSD'] = market_symbol('TWDUSD', 'forex')  # New Taiwan Dollar to USD
    common_symbols['THBUSD'] = market_symbol('THBUSD', 'forex')  # Thai Baht to USD
    common_symbols['PHPUSD'] = market_symbol('PHPUSD', 'forex')  # Philippine Peso to USD
    common_symbols['IDRUSD'] = market_symbol('IDRUSD', 'forex')  # Indonesian Rupiah to USD
    common_symbols['VNDUSD'] = market_symbol('VNDUSD', 'forex')  # Vietnamese Dong to USD
    common_symbols['MYRUSD'] = market_symbol('MYRUSD', 'forex')  # Malaysian Ringgit to USD
    common_symbols['PKRUSD'] = market_symbol('PKRUSD', 'forex')  # Pakistani Rupee to USD
    common_symbols['KWDUSD'] = market_symbol('KWDUSD', 'forex')  # Kuwaiti Dinar to USD
    common_symbols['SARUSD'] = market_symbol('SARUSD', 'forex')  # Saudi Riyal to USD
    common_symbols['QARUSD'] = market_symbol('QARUSD', 'forex')  # Qatari Riyal to USD
    common_symbols['AEDUSD'] = market_symbol('AEDUSD', 'forex')  # UAE Dirham to USD
    common_symbols['NZDUSD'] = market_symbol('NZDUSD', 'forex')  # New Zealand Dollar to USD
    common_symbols['USDCAD'] = market_symbol('USDCAD', 'forex')  # USD to Canadian Dollar
    common_symbols['USDCHF'] = market_symbol('USDCHF', 'forex')  # USD to Swiss Franc
    common_symbols['USDJPY'] = market_symbol('USDJPY', 'forex')  # USD to Japanese Yen
    common_symbols['USDZAR'] = market_symbol('USDZAR', 'forex')  # USD to South African Rand
    common_symbols['USDHKD'] = market_symbol('USDHKD', 'forex')  # USD to Hong Kong Dollar
    common_symbols['USDSGD'] = market_symbol('USDSGD', 'forex')  # USD to Singapore Dollar
    common_symbols['USDSEK'] = market_symbol('USDSEK', 'forex')  # USD to Swedish Krona
    common_symbols['USDNOK'] = market_symbol('USDNOK', 'forex')  # USD to Norwegian Krone
    common_symbols['USDTRY'] = market_symbol('USDTRY', 'forex')  # USD to Turkish Lira
    common_symbols['USDMXN'] = market_symbol('USDMXN', 'forex')  # USD to Mexican Peso
    common_symbols['USDPLN'] = market_symbol('USDPLN', 'forex')  # USD to Polish Zloty
    common_symbols['USDRUB'] = market_symbol('USDRUB', 'forex')  # USD to Russian Ruble
    common_symbols['USDINR'] = market_symbol('USDINR', 'forex')  # USD to Indian Rupee
    common_symbols['USDBRL'] = market_symbol('USDBRL', 'forex')  # USD to Brazilian Real
    common_symbols['USDCNY'] = market_symbol('USDCNY', 'forex')  # USD to Chinese Yuan
    common_symbols['USDCNH'] = market_symbol('USDCNH', 'forex')  # USD to Chinese Yuan Offshore
    common_symbols['USDKRW'] = market_symbol('USDKRW', 'forex')  # USD to South Korean Won
    common_symbols['USDTWD'] = market_symbol('USDTWD', 'forex')  # USD to New Taiwan Dollar
    common_symbols['USDTHB'] = market_symbol('USDTHB', 'forex')  # USD to Thai Baht
    common_symbols['USDPHP'] = market_symbol('USDPHP', 'forex')  # USD to Philippine Peso
    common_symbols['USDIDR'] = market_symbol('USDIDR', 'forex')  # USD to Indonesian Rupiah
    common_symbols['USDVND'] = market_symbol('USDVND', 'forex')  # USD to Vietnamese Dong
    common_symbols['USDMYR'] = market_symbol('USDMYR', 'forex')  # USD to Malaysian Ringgit
    common_symbols['USDPKR'] = market_symbol('USDPKR', 'forex')  # USD to Pakistani Rupee
    common_symbols['USDKWD'] = market_symbol('USDKWD', 'forex')  # USD to Kuwaiti Dinar
    common_symbols['USDSAR'] = market_symbol('USDSAR', 'forex')  # USD to Saudi Riyal
    common_symbols['USDQAR'] = market_symbol('USDQAR', 'forex')  # USD to Qatari Riyal
    common_symbols['USDAED'] = market_symbol('USDAED', 'forex')  # USD to UAE Dirham

    # Commodities
    common_symbols['XTIUSD'] = market_symbol('USDOIL', 'forex')  # Crude Oil to USD
    common_symbols['XNGUSD'] = market_symbol('USNATGAS', 'forex')  # Natural Gas to USD
    common_symbols['XBRUSD'] = market_symbol('XAUUSD', 'forex')  # Brent to USD

    # Metals
    common_symbols['XAUUSD'] = market_symbol('XAUUSD', 'forex')  # Gold to USD
    common_symbols['XAGUSD'] = market_symbol('XAGUSD', 'forex')  # Silver to USD

    # Indices
    common_symbols['SPX500'] = market_symbol('SPX500', 'forex')  # S&P 500
    common_symbols['US500'] = market_symbol('US500', 'forex')  # S&P 500
    common_symbols['US30'] = market_symbol('US30', 'forex')  # Dow Jones 30
    common_symbols['NAS100'] = market_symbol('NAS100', 'forex')  # Nasdaq 100
    common_symbols['US100'] = market_symbol('US100', 'forex')  # Nasdaq 100
    common_symbols['US2000'] = market_symbol('US2000', 'forex')  # Russell 2000
    common_symbols['UK100'] = market_symbol('UK100', 'forex')  # FTSE 100
    common_symbols['DE30'] = market_symbol('DE30', 'forex')  # DAX 30
    common_symbols['JP225'] = market_symbol('JP225', 'forex')  # Nikkei 225
    common_symbols['HK50'] = market_symbol('HK50', 'forex')  # Hang Seng 50
    common_symbols['AUS200'] = market_symbol('AUS200', 'forex')  # Australia 200
    common_symbols['ES35'] = market_symbol('ES35', 'forex')  # Spain 35
    common_symbols['FR40'] = market_symbol('FR40', 'forex')  # France 40
    common_symbols['IT40'] = market_symbol('IT40', 'forex')  # Italy 40
    common_symbols['NL25'] = market_symbol('NL25', 'forex')  # Netherlands 25
    common_symbols['SG30'] = market_symbol('SG30', 'forex')  # Singapore 30
    common_symbols['CN50'] = market_symbol('CN50', 'forex')  # China A50
    common_symbols['IN50'] = market_symbol('IN50', 'forex')  # India 50
    common_symbols['USDX'] = market_symbol('USDX', 'forex')  # US Dollar Index
    common_symbols['VIX'] = market_symbol('VIX', 'forex')  # CBOE Volatility Index
    common_symbols['DXY'] = market_symbol('DXY', 'forex')  # US Dollar Index

    converted_symbols = {}
    # converted_symbols.Add("BITCOIN", "BTCUSD");
    # converted_symbols.Add("ETHEREUM", "ETHUSD");
    # converted_symbols.Add("BNB", "BNBUSD");
    # converted_symbols.Add("XRP", "XRPUSD");
    # converted_symbols.Add("OIL", "XTIUSD");
    # converted_symbols.Add("OILUK", "XBRUSD");
    # converted_symbols.Add("OILUS", "XTIUSD");
    # converted_symbols.Add("GOLD", "XAUUSD");
    # converted_symbols.Add("SILVER", "XAGUSD");
    # converted_symbols.Add("PLATINUM", "XPTUSD");
    # converted_symbols.Add("PALLADIUM", "XPDUSD");
    # // converted_symbols.Add("CORN", "CORNUSD");
    # // converted_symbols.Add("SOYBEAN", "SOYBNUSD");
    # // converted_symbols.Add("WHEAT", "WHEATUSD");
    # // converted_symbols.Add("COTTON", "COTTONUSD");
    # // converted_symbols.Add("SUGAR", "SUGARUSD");
    # // converted_symbols.Add("COFFEE", "COFFEEUSD");
    # // converted_symbols.Add("COCOA", "COCOAUSD");
    # converted_symbols.Add("DOW", "US30");
    # converted_symbols.Add("NASDAQ", "US100");
    # converted_symbols.Add("SP500", "SPX500");
    # converted_symbols.Add("NIKKEI", "JP225");
    # converted_symbols.Add("HANGSENG", "HK50");
    # converted_symbols.Add("DAX", "DE30");
    # converted_symbols.Add("FTSE", "UK100");
    # converted_symbols.Add("CAC", "FR40");
    # converted_symbols.Add("IBEX", "ES35");
    # converted_symbols.Add("EUROSTOXX", "EU50");
    # // converted_symbols.Add("VIX", "VIXX");
    # converted_symbols.Add("USDINDEX", "DXY");
    # converted_symbols.Add("ASX200", "AUS200");
    # converted_symbols.Add("UKOUSD", "XBRUSD");
    # converted_symbols.Add("USOUSD", "XTIUSD");
    # converted_symbols.Add("USOIL", "XTIUSD");
    # converted_symbols.Add("UKOIL", "XBRUSD");
    # converted_symbols.Add("NDX100", "US100");
    # converted_symbols.Add("SPX500", "US500");      
    # convert the above commented out code to python
    converted_symbols['BITCOIN'] = 'BTCUSD'
    converted_symbols['ETHEREUM'] = 'ETHUSD'
    converted_symbols['BNB'] = 'BNBUSD'
    converted_symbols['XRP'] = 'XRPUSD'
    converted_symbols['OIL'] = 'XTIUSD'
    converted_symbols['OILUK'] = 'XBRUSD'
    converted_symbols['OILUS'] = 'XTIUSD'
    converted_symbols['GOLD'] = 'XAUUSD'
    converted_symbols['SILVER'] = 'XAGUSD'
    converted_symbols['PLATINUM'] = 'XPTUSD'
    converted_symbols['PALLADIUM'] = 'XPDUSD'
    converted_symbols['DOW'] = 'US30'
    converted_symbols['NASDAQ'] = 'US100'
    converted_symbols['SP500'] = 'US500'
    converted_symbols['NIKKEI'] = 'JP225'
    converted_symbols['HANGSENG'] = 'HK50'
    converted_symbols['DAX'] = 'DE30'
    converted_symbols['FTSE'] = 'UK100'
    converted_symbols['CAC'] = 'FR40'
    converted_symbols['IBEX'] = 'ES35'
    converted_symbols['EUROSTOXX'] = 'EU50'
    converted_symbols['USDINDEX'] = 'DXY'
    converted_symbols['ASX200'] = 'AUS200'
    converted_symbols['UKOUSD'] = 'XBRUSD'
    converted_symbols['USOUSD'] = 'XTIUSD'
    converted_symbols['USOIL'] = 'XTIUSD'
    converted_symbols['UKOIL'] = 'XBRUSD'
    converted_symbols['NDX100'] = 'US100'
    converted_symbols['SPX500'] = 'US500'
    

