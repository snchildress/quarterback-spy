import config

from datetime import datetime
import json
import requests
import logging

# configure the logger to log anything at or above the DEBUG level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event=None, context=None):
  """
  AWS Lambda handler to get the lowest prices for the
  NFC Championship game, post them to Slack, and alert
  if the price is below the configured max threshold
  """
  # create an empty dict to store lowest ticket prices and message for Slack
  lowest_prices = {}
  lowest_prices_message = 'Current cheapest Saints NFC Championship ticket prices:\n\n'

  # find cheapest SeatGeek ticket
  response = requests.get(config.SEATGEEK_ENDPOINT.format(config.SEATGEEK_EVENT_ID))
  if response.ok:
    response_body = response.json()
    lowest_prices['SeatGeek'] = str(response_body['stats']['lowest_price'])

  # find cheapest Ticket City ticket
  url = config.TICKET_CITY_ENDPOINT.format(config.TICKET_CITY_EVENT_ID)
  headers = {'X-TcAffKey': config.TICKET_CITY_API_KEY}
  response = requests.get(url, headers=headers)
  if response.ok:
    response_body = response.json()
    prices = [ticket['ListPrice'] for ticket in response_body]
    lowest_price = round(min(prices)) + config.TICKET_CITY_ESTIMATED_FEES
    lowest_prices['Ticket City'] = str(lowest_price)

  # iterate through the lowest prices to log and post affordable alert to Slack
  for marketplace, lowest_price in lowest_prices.items():
    lowest_prices_message += marketplace + ': $' + lowest_price + '\n'
    if int(lowest_price) < config.MAX_AFFORDABLE_PRICE:
      message = '<!channel> ' + marketplace + ' has an affordable NFC Championship ticket for $' + lowest_price + '!'
      _message_slack(message)

  # if it is currently the job closest to the top of the hour
  current_minute = datetime.now().minute
  if (current_minute < config.POLLING_RATE / 2) \
      or (current_minute > (60 - config.POLLING_RATE / 2)):
    # post all of the lowest prices to Slack
    lowest_prices_message = lowest_prices_message[:-1] # remove the trailing new line
    _message_slack(lowest_prices_message)

  # log the lowest prices as a JSON object
  logger.info(json.dumps(lowest_prices))

def _message_slack(message):
  """
  Internal function to post a given message to the
  configured Slack channel
  """
  url = config.SLACK_ENDPOINT
  headers = {'Authorization': 'Bearer ' + config.SLACK_API_KEY}
  body = {
    'channel': config.SLACK_CHANNEL,
    'text': str(message),
  }
  requests.post(url, headers=headers, json=body)


if config.ENV != 'prod' and '__main__' in __name__:
  # run the handler when executing this file in a non-prod env
  handler()
