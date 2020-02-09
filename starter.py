import config
import util
import requests
import json

username = config.USERNAME
password = config.PASSWORD

client_id, client_token = util.login(username, password)

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'investfly-client-id': client_id,
           'investfly-client-token': client_token,
           'investfly-app-token': config.APP_TOKEN}

# Helpful links:
# https://www.investfly.com/guides/api_documentation
# https://www.investfly.com/guides/api_tuts

# Example: buy TSLA when it's price is down by 5% two days ago, down by less than 2% in the previous day, and up today

# Get prices
response = requests.get(url='https://api.investfly.com/stockmarket/bars?symbol=TSLA&market=US&days=3',
                        headers=headers)
info = json.loads(response.text)
tsla_price_0 = info[0]['lastPrice']     # most recent closing price
tsla_price_1 = info[1]['lastPrice']     # 1-day-ago closing price
tsla_price_2 = info[2]['lastPrice']     # 2-days-ago closing price

response = requests.get(url='https://api.investfly.com/stockmarket/quote?symbol=TSLA&market=US&'
                            'securityType=STOCK&realtime=true',
                        headers=headers)
tsla_price = json.loads(response.text)['lastPrice']     # current price

# Execute trade if prices satisfy criterion
# if (tsla_price_1 - tsla_price_2) / tsla_price_2 <= -0.05 and \
#         0 > (tsla_price_0 - tsla_price_1) / tsla_price_1 >= -0.02 and tsla_price - tsla_price_0 > 0:
if True:    # Remove once bug is fixed
    headers_copy = dict(headers)
    trade_headers = {'tradeType': 'BUY',
                     'orderType': 'MARKET_ORDER',
                     'quantity': '50',
                     'brokerType': 'INVESTFLY',
                     'security': json.dumps({
                         'symbol': 'TSLA',
                         'securityType': 'STOCK',
                         'market': 'US'})
                     }
    trade_headers = {**headers_copy, **trade_headers}
    portfolio_id = '1465449'
    response = requests.post(url='https://api.investfly.com/portfolio/Investfly/' + portfolio_id + '/trade?market=US',
                             headers=trade_headers)
    print(trade_headers)
    print(json.loads(response.text))

util.logout(client_id, client_token)
