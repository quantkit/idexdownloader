from datetime import datetime, timezone
import numpy as np
import pandas as pd
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time

def get_user_addresses():
  user_input = input('Copy and paste your IDEX ethereum address(es), using commas to separate multiple addresses, and press enter: ')

  addresses = []
  
  for address in user_input.split(','):
    address = address.lower().strip()
    if len(address) != 42 or address[:2] != '0x':
      print_error_message_and_exit('\n' + 'The program encountered an error while trying to read your Ethereum address(es).  Each address must be 42 characters long and begin with 0x.  If you are entering multiple addresses, use commas to separate them.  Please run the program again and reenter your address(es).')

    addresses.append(address)

  return addresses

def retry_session(url, error_codes):
  session = requests.Session()
  retry = Retry(
      total=12,
      backoff_factor=0.1,
      method_whitelist=('GET', 'POST'),
      status_forcelist=error_codes
  )
  adapter = HTTPAdapter(max_retries=retry)
  session.mount(url, adapter)
  return session

def get_idex_trade_history(idex_session, market=None, address=None, start=None, end=None):
  json = {}
  if market:
    json['market'] = market
  if address:
    json['address'] = address
  if start is not None:
    json['start'] = start
  if end:
    json['end'] = end

  try:
    response = post_request(idex_session, idex_api_base_url + 'returnTradeHistory', json=json)
  except Exception as e:
    print_error_message_and_exit('\n' + 'The IDEX API is not responding right now.  Please try running the program again later.')
  return response.json()

def post_request(session, url, auth=None, json=None):
  return session.post(url, auth=auth, json=json, timeout=5)

def print_error_message_and_exit(message):
  print(message)
  raise SystemExit    

def add_record_to_df(df, type, left_amount, left_currency, right_amount, right_currency, fee_amount, timestamp):
  if type == 'buy':
    buy_amount = right_amount
    buy_currency = right_currency
    sell_amount = left_amount
    sell_currency = left_currency
  elif type == 'sell':
    buy_amount = left_amount 
    buy_currency = left_currency
    sell_amount = right_amount
    sell_currency = right_currency
  
  buy_amount = buy_amount - fee_amount
  date = str(datetime.fromtimestamp(timestamp, timezone.utc))

  df.loc[len(df.index)] = ['Trade', buy_amount, buy_currency, sell_amount, sell_currency, fee_amount, buy_currency, 'IDEX', np.NaN, np.NaN, date]

  return df

def write_output_file(df, output_filename):
  if len(df.index) > 0:
    try:
      df.to_csv(output_filename, index=False)
    except:
      print_error_message_and_exit('\n' + 'The program encountered an error while trying to write the output file named "' + output_filename + '".  Please ensure this file is closed and try running the program again.')
    print('\n' + 'Successfully generated ' + output_filename)
  else:
    print_error_message_and_exit('\n' + 'IDEX has no trade history for the entered address(es).  Please run the program again with different address(es).')
  
def main():
  idex_session = retry_session(idex_api_base_url, error_codes)
  
  df = pd.DataFrame(columns=['Type (Trade, IN or OUT)', 'Buy Amount', 'Buy Cur.', 'Sell Amount', 'Sell Cur.', 'Fee Amount (optional)', 'Fee Cur. (optional)', 'Exchange (optional)', 'Trade Group (optional)', 'Comment (optional)', 'Date'])

  addresses = get_user_addresses()
  
  for address in addresses:
    response = get_idex_trade_history(idex_session, address=address, start=0, end=int(time.time()))

    for pair in response:
      currencies = pair.split('_')
      left_currency = currencies[0]
      right_currency = currencies[1]
      for trade in response[pair]:      
        left_amount = float(trade['total'])
        right_amount = float(trade['amount'])
        timestamp = int(trade['timestamp'])
        type = trade['type'].lower().strip()
        
        if type == 'buy':
          fee_amount = float(trade['buyerFee'])
        elif type == 'sell':
          fee_amount = float(trade['sellerFee'])
        
        if trade['taker'].lower().strip() == address:
          fee_amount = fee_amount + float(trade['gasFee'])
        
        add_record_to_df(df, type, left_amount, left_currency, right_amount, right_currency, fee_amount, timestamp)
  
  df.sort_values(by=['Date'], ascending=False, inplace=True)
  write_output_file(df, output_filename)

error_codes = set([400, 401, 403, 404, 429, 500, 502, 503, 504])
idex_api_base_url = 'https://api-regional.idex.market/'
output_filename = 'idex_trade_history.csv'

if __name__ == '__main__':
  main()
