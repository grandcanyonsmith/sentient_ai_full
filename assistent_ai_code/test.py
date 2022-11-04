Recommendation ID: 4f19722309958afdea40f869f2fabf01f137b725f1b6ae7ced449eb
Category: PythonBestPractices
Recommendation: To create a `list`, try to use `list` comprehension instead of a loop. List comprehension is the preferred way to make a list using Python, and it's simpler and easier to understand than using a loop.

[Learn more](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
Start line: 101
End line: 101
File path: StockInformation/old_support_extract.py
Severity: Low



Enter the path to the file you want to search: 
/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/hello_world.py
Total number of functions extracted: 8
/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//StockInformation/old_support_extract.py:get_stock_resistance_for_any_interval  score=0.885
def get_stock_resistance_for_any_interval(ticker,current_price,previous_close):
    resistance_levels = ['15','30','60','D','W','M']

    resistance_level_bank = [
        check_if_resistance_broken(
            ticker, level, current_price, previous_close
        )
        for level in resistance_levels
    ]

    return next(
        (
            resistance_level
            for resistance_level in resistance_level_bank
            if resistance_level['break_through'] == 'True'
        ),
        None,
    )

----------------------------------------------------------------------
aasdfa



recommendation To create a `list`, try to use `list` comprehension instead of a loop. List comprehension is the preferred way to make a list using Python, and it's simpler and easier to understand than using a loop.

[Learn more](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)



def get_stock_resistance_for_any_interval(ticker,current_price,previous_close):
    resistance_level_bank = [
        check_if_resistance_broken(
            ticker, level, current_price, previous_close
        )
        for level in ['15','30','60','D','W','M']
    ]

    return next(
        (
            resistance_level
            for resistance_level in resistance_level_bank
            if resistance_level['break_through'] == 'True'
        ),
        None,
    )

def get_stock_resistance_for_any_interval(ticker,current_price,previous_close):
    resistance_level_bank = [
        check_if_resistance_broken(
            ticker, level, current_price, previous_close
        )
        for level in ['15','30','60','D','W','M']
    ]

    return next(
        (
            resistance_level
            for resistance_level in resistance_level_bank
            if resistance_level['break_through'] == 'True'
        ),
        None,
    )










Recommendation ID: 6a3d2d8d66f7633c930517227c0b043e2ad5d75db0af0f27ae3ce22
Category: PythonBestPractices
Recommendation: To check if a container or sequence (string, list, tuple) is empty, use `if not val`. Do not compare its length using `if len(val) == 0` or `if len(val) > 0`

 [Learn more](https://www.python.org/dev/peps/pep-0008/#programming-recommendations#:~:text=if%20not%20seq)
Start line: 32
End line: 32
File path: StockInformation/old_support_extract.py
Severity: Low



/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//StockInformation/old_support_extract.py:get_resistance_levels  score=0.821
def get_resistance_levels(ticker, interval):
    url = f'https://finnhub.io/api/v1/scan/support-resistance?symbol={str(ticker)}&resolution={str(interval)}&token={finnhub_api_key_2}'

    r = requests.get(url)
    resistance_levels = r.json()
    resistance_levels = resistance_levels['levels']

    if len(resistance_levels) != 0:
        for x in resistance_levels:
            json = {"interval": interval,"resistance":x}
            all_resistances.append(json)
    return resistance_levels
----------------------------------------------------------------------
aasdfa



recommendation To check if a container or sequence (string, list, tuple) is empty, use `if not val`. Do not compare its length using `if len(val) == 0` or `if len(val) > 0`

 [Learn more](https://www.python.org/dev/peps/pep-0008/#programming-recommendations#:~:text=if%20not%20seq)



def get_resistance_levels(ticker, interval):
    url = f'https://finnhub.io/api/v1/scan/support-resistance?symbol={str(ticker)}&resolution={str(interval)}&token={finnhub_api_key_2}'

    r = requests.get(url)
    resistance_levels = r.json()
    resistance_levels = resistance_levels['levels']

    if resistance_levels:
        for x in resistance_levels:
            json = {"interval": interval,"resistance":x}
            all_resistances.append(json)
    return resistance_levels
def get_resistance_levels(ticker, interval):
    url = f'https://finnhub.io/api/v1/scan/support-resistance?symbol={str(ticker)}&resolution={str(interval)}&token={finnhub_api_key_2}'

    r = requests.get(url)
    resistance_levels = r.json()
    resistance_levels = resistance_levels['levels']

    if resistance_levels:
        for x in resistance_levels:
            json = {"interval": interval,"resistance":x}
            all_resistances.append(json)
    return resistance_levels










Recommendation ID: bad800c8c05bb01e30be7bb4183dcc00b120fdaed71a62fec632657
Category: PythonBestPractices
Recommendation: It appears you are unpacking more than three variables while using a function that returns more than one variable. Using a large number of return values is prone to errors. We recommend that you return a small class or `namedtuple` instance instead.

[Learn more](https://docs.python.org/3/library/typing.html#typing.NamedTuple)

Similar issue at line number 146.
Start line: 135
End line: 135
File path: StockInformation/old_support_extract.py
Severity: Medium



/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//StockInformation/old_support_extract.py:create_resistance_report  score=0.929
def create_resistance_report(ticker,current_price,previous_close):
    get_resistance = get_stock_resistance_for_any_interval(ticker,current_price,previous_close)

    if get_resistance is not None:
        next_highest_resistance, interval = get_next_high_for_any_interval(current_price)
        resistance = float(get_resistance['Resistance']).__round__(2)
        break_through = get_resistance['break_through']
        past_time_interval = get_resistance['time_interval']
        next_time_interval = interval
        price = get_resistance['price']
        next_resistance = float(next_highest_resistance).__round__(2)
        words = f" crossed resistance today at {str(resistance)} for {past_time_interval} time interval. Price is {str(price)}."

    else:
        break_through = " "
        words = "No resistance broken"
        past_time_interval = " "
        next_time_interval = " "
        resistance = " "
        next_resistance = " "
        price = " "

    all_resistances.clear()
    return words, break_through, past_time_interval, next_time_interval, resistance, next_resistance

----------------------------------------------------------------------
aasdfa



recommendation It appears you are unpacking more than three variables while using a function that returns more than one variable. Using a large number of return values is prone to errors. We recommend that you return a small class or `namedtuple` instance instead.

[Learn more](https://docs.python.org/3/library/typing.html#typing.NamedTuple)

Similar issue at line number 146.



def create_resistance_report(ticker,current_price,previous_close):
    get_resistance = get_stock_resistance_for_any_interval(ticker,current_price,previous_close)

    if get_resistance is not None:
        next_highest_resistance, interval = get_next_high_for_any_interval(current_price)
        resistance = float(get_resistance['Resistance']).__round__(2)
        break_through = get_resistance['break_through']
        past_time_interval = get_resistance['time_interval']
        next_time_interval = interval
        price = get_resistance['price']
        next_resistance = float(next_highest_resistance).__round__(2)
        words = f" crossed resistance today at {str(resistance)} for {past_time_interval} time interval. Price is {str(price)}."

    else:
        break_through = " "
        words = "No resistance broken"
        past_time_interval = " "
        next_time_interval = " "
        resistance = " "
        next_resistance = " "
        price = " "

    all_resistances.clear()
    return words, break_through, past_time_interval, next_time_interval, resistance, next_resistance, price

def create_resistance_report(ticker,current_price,previous_close):
    get_resistance = get_stock_resistance_for_any_interval(ticker,current_price,previous_close)

    if get_resistance is not None:
        next_highest_resistance, interval = get_next_high_for_any_interval(current_price)
        resistance = float(get_resistance['Resistance']).__round__(2)
        break_through = get_resistance['break_through']
        past_time_interval = get_resistance['time_interval']
        next_time_interval = interval
        price = get_resistance['price']
        next_resistance = float(next_highest_resistance).__round__(2)
        words = f" crossed resistance today at {str(resistance)} for {past_time_interval} time interval. Price is {str(price)}."

    else:
        break_through = " "
        words = "No resistance broken"
        past_time_interval = " "
        next_time_interval = " "
        resistance = " "
        next_resistance = " "
        price = " "

    all_resistances.clear()
    return words, break_through, past_time_interval, next_time_interval, resistance, next_resistance, price










Recommendation ID: e811d7962e33afcc4e1202db93793fde9f0c02cbb92affda170915d
Category: PythonBestPractices
Recommendation: It appears that you are generically passing an `Exception` object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the [logging.exception()](https://docs.python.org/3/library/logging.html#logging.exception) API. For example,

```
try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

```
Start line: 44
End line: 44
File path: StockInformation/stock_indicators_analysis.py
Severity: High



/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//StockInformation/stock_indicators_analysis.py:nyse  score=0.743
def nyse(stock, time_interval):
    try:
        stock_exchange = 'NYSE'
        handler = TA_Handler(
            symbol= stock,
            exchange=stock_exchange,
            screener="america",
            interval=time_interval,
            timeout=None
        )

        # analysis = 
        summary = handler.get_analysis().summary
        overall_recommendation = summary['RECOMMENDATION']
        print(time_interval,"=",overall_recommendation)
        return overall_recommendation
    except:
        Exception
    


----------------------------------------------------------------------
aasdfa



recommendation It appears that you are generically passing an `Exception` object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the [logging.exception()](https://docs.python.org/3/library/logging.html#logging.exception) API. For example,

```
try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

```



def nyse(stock, time_interval):
    try:
        stock_exchange = 'NYSE'
        handler = TA_Handler(
            symbol= stock,
            exchange=stock_exchange,
            screener="america",
            interval=time_interval,
            timeout=None
        )

        # analysis = 
        summary = handler.get_analysis().summary
        overall_recommendation = summary['RECOMMENDATION']
        print(time_interval,"=",overall_recommendation)
        return overall_recommendation
    except:
        logging.exception('ZeroDivisionError: %s', e)
    


def nyse(stock, time_interval):
    try:
        stock_exchange = 'NYSE'
        handler = TA_Handler(
            symbol= stock,
            exchange=stock_exchange,
            screener="america",
            interval=time_interval,
            timeout=None
        )

        # analysis = 
        summary = handler.get_analysis().summary
        overall_recommendation = summary['RECOMMENDATION']
        print(time_interval,"=",overall_recommendation)
        return overall_recommendation
    except:
        logging.exception('ZeroDivisionError: %s', e)
    










Recommendation ID: security-3e11bef7a44b5116ed8622e671b23581c7f17c138cac33d97038ffb
Category: SecurityIssues
Recommendation: It appears your code contains a hardcoded API Gateway API Key. Hardcoded secrets or credentials can allow attackers to bypass authentication methods and perform malicious actions. We recommend revoking access to resources using this credential and storing future credentials in a management service such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).

[Learn more about the use of hardcoded credentials](https://cwe.mitre.org/data/definitions/798.html)
Start line: 4
End line: 4
File path: StockInformation/exchange_lookup.py
Severity: Critical



/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//StockInformation/exchange_lookup.py:look_up_exchange  score=0.949
def look_up_exchange(tick):
    url = f'https://financialmodelingprep.com/api/v3/search?query={tick}&limit=10&apikey=e49e22b0865cfeea71aa0771ddf965a1'

    r = requests.get(url)
    return r.json()[0].get('exchangeShortName')

----------------------------------------------------------------------
aasdfa



recommendation It appears your code contains a hardcoded API Gateway API Key. Hardcoded secrets or credentials can allow attackers to bypass authentication methods and perform malicious actions. We recommend revoking access to resources using this credential and storing future credentials in a management service such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).

[Learn more about the use of hardcoded credentials](https://cwe.mitre.org/data/definitions/798.html)



Old code:  def look_up_exchange(tick):
    url = f'https://financialmodelingprep.com/api/v3/search?query={tick}&limit=10&apikey=e49e22b0865cfeea71aa0771ddf965a1'

    r = requests.get(url)
    return r.json()[0].get('exchangeShortName')

def look_up_exchange(tick):
    url = f'https://financialmodelingprep.com/api/v3/search?query={tick}&limit=10&apikey=e49e22b0865cfeea71aa0771ddf965a1' # noqa: E501

    r = requests.get(url)
    return r.json()[0].get('exchangeShortName')










Recommendation ID: security-6244f7070e5e3433abe5c6a3951da44136715f4c00e3aab850d83f9
Category: ResourceLeaks
Recommendation: **Problem**
This line of code might contain a resource leak. Resource leaks can cause your system to slow down or crash.

**Fix**
Consider closing the following resource: *session*. The resource is allocated by call *sessions.Session*. Currently, there are execution paths that do not contain closure statements, for example, when *Session.get()* throws an exception. To prevent this resource leak, close *session* in a try-finally block or declare it using a `with` statement.

**More info**
[View details about the `with` statement in the Python developer's guide](https://www.python.org/dev/peps/pep-0343/) (external link).
Start line: 13
End line: 13
File path: ScrapedStocks/scrape_iv_stocks.py
Severity: Medium



/Users/canyonsmith/Documents/GitHub/stock-options-analyzer//ScrapedStocks/scrape_iv_stocks.py:scrape_highest_iv_stocks  score=0.887
def scrape_highest_iv_stocks():
    session = requests.Session()
    main_page_url = 'https://www.barchart.com/options/highest-implied-volatility/highest?sector=stock'
    url = f"https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol,baseSymbol,baseLastPrice,baseSymbolType,symbolType,strikePrice,expirationDate,daysToExpiration,bidPrice,midpoint,askPrice,lastPrice,volume,openInterest,volumeOpenInterestRatio,volatility,tradeTime,symbolCode,hasOptions&orderBy=volatility&baseSymbolTypes=stock&between(lastPrice,.10,)=&between(daysToExpiration,15,)=&between(tradeTime,{week_ago_date},{today_date})=&orderDir=desc&between(volatility,60,)=&limit=200&between(volume,500,)=&between(openInterest,100,)=&in(exchange,(AMEX,NASDAQ,NYSE))=&meta=field.shortName,field.type,field.description&hasOptions=true&raw=1"

    payload={}
    headers = {
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'Accept': 'application/json',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }

    r = session.get(main_page_url,headers=headers)
    headers['X-XSRF-TOKEN'] = unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
    response = session.request("GET", url, headers=headers, data=payload)
    return [stock_ticker['baseSymbol'] for stock_ticker in response.json()['data'] if stock_ticker not in highest_iv_stocks]





----------------------------------------------------------------------
aasdfa



recommendation **Problem**
This line of code might contain a resource leak. Resource leaks can cause your system to slow down or crash.

**Fix**
Consider closing the following resource: *session*. The resource is allocated by call *sessions.Session*. Currently, there are execution paths that do not contain closure statements, for example, when *Session.get()* throws an exception. To prevent this resource leak, close *session* in a try-finally block or declare it using a `with` statement.

**More info**
[View details about the `with` statement in the Python developer's guide](https://www.python.org/dev/peps/pep-0343/) (external link).



def scrape_highest_iv_stocks():
    session = requests.Session()
    main_page_url = 'https://www.barchart.com/options/highest-implied-volatility/highest?sector=stock'
    url = f"https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol,baseSymbol,baseLastPrice,baseSymbolType,symbolType,strikePrice,expirationDate,daysToExpiration,bidPrice,midpoint,askPrice,lastPrice,volume,openInterest,volumeOpenInterestRatio,volatility,tradeTime,symbolCode,hasOptions&orderBy=volatility&baseSymbolTypes=stock&between(lastPrice,.10,)=&between(daysToExpiration,15,)=&between(tradeTime,{week_ago_date},{today_date})=&orderDir=desc&between(volatility,60,)=&limit=200&between(volume,500,)=&between(openInterest,100,)=&in(exchange,(AMEX,NASDAQ,NYSE))=&meta=field.shortName,field.type,field.description&hasOptions=true&raw=1"

    payload={}
    headers = {
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'Accept': 'application/json',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }

    r = session.get(main_page_url,headers=headers)
    headers['X-XSRF-TOKEN'] = unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
    response = session.request("GET", url, headers=headers, data=payload)
    return [stock_ticker['baseSymbol'] for stock_ticker in response.json()['data'] if stock_ticker not in highest_iv_stocks]





def scrape_highest_iv_stocks():
    with requests.Session() as session:
        main_page_url = 'https://www.barchart.com/options/highest-implied-volatility/highest?sector=stock'
        url = f"https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol,baseSymbol,baseLastPrice,baseSymbolType,symbolType,strikePrice,expirationDate,daysToExpiration,bidPrice,midpoint,askPrice,lastPrice,volume,openInterest,volumeOpenInterestRatio,volatility,tradeTime,symbolCode,hasOptions&orderBy=volatility&baseSymbolTypes=stock&between(lastPrice,.10,)=&between(daysToExpiration,15,)=&between(tradeTime,{week_ago_date},{today_date})=&orderDir=desc&between(volatility,60,)=&limit=200&between(volume,500,)=&between(openInterest,100,)=&in(exchange,(AMEX,NASDAQ,NYSE))=&meta=field.shortName,field.type,field.description&hasOptions=true&raw=1"

        payload={}
        headers = {
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'Accept': 'application/json',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
        }

        r = session.get(main_page_url,headers=headers)
        headers['X-XSRF-TOKEN'] = unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
        response = session.request("GET", url, headers=headers, data=payload)
        return [stock_ticker['baseSymbol'] for stock_ticker in response.json()['data'] if stock_ticker not in highest_iv_stocks]













Recommendation ID: security-ecbae05c13eb1520f52c65831b2eb31093b06c66cb01e5f0057f2b0
Category: PythonBestPractices
Recommendation: The naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. The recommended way to create an aware datetime object representing a specific timestamp in UTC is by passing `tzinfo` as an argument to the method.

[Learn more](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)
Start line: 5
End line: 5
File path: ScrapedStocks/scrape_iv_stocks.py
Severity: Medium


def scrape_highest_iv_stocks():
    session = requests.Session()
    main_page_url = 'https://www.barchart.com/options/highest-implied-volatility/highest?sector=stock'
    url = f"https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol,baseSymbol,baseLastPrice,baseSymbolType,symbolType,strikePrice,expirationDate,daysToExpiration,bidPrice,midpoint,askPrice,lastPrice,volume,openInterest,volumeOpenInterestRatio,volatility,tradeTime,symbolCode,hasOptions&orderBy=volatility&baseSymbolTypes=stock&between(lastPrice,.10,)=&between(daysToExpiration,15,)=&between(tradeTime,{week_ago_date},{today_date})=&orderDir=desc&between(volatility,60,)=&limit=200&between(volume,500,)=&between(openInterest,100,)=&in(exchange,(AMEX,NASDAQ,NYSE))=&meta=field.shortName,field.type,field.description&hasOptions=true&raw=1"

    payload={}
    headers = {
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'Accept': 'application/json',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }

    r = session.get(main_page_url,headers=headers)
    headers['X-XSRF-TOKEN'] = unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
    response = session.request("GET", url, headers=headers, data=payload)
    return [stock_ticker['baseSymbol'] for stock_ticker in response.json()['data'] if stock_ticker not in highest_iv_stocks]



