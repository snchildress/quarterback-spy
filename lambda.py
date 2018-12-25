import config

import requests


def handler(event=None, context=None):
  # create an empty dict to store lowest ticket prices
  lowest_prices = {}

  # find cheapest seatgeek ticket
  response = requests.get(config.SEATGEEK_ENDPOINT.format(config.SEATGEEK_EVENT_ID))
  if response.ok:
    response_body = response.json()
    lowest_prices['SeatGeek'] = response_body['stats']['lowest_price']

  for marketplace, lowest_price in lowest_prices.items():
    print(marketplace + ' Cheapest Ticket: $' + str(lowest_price))

  # post affordable ticket alert to Slack
  request_url = config.SLACK_ENDPOINT
  request_headers = {'Authorization': 'Bearer ' + config.SLACK_API_KEY}
  request_body = {
    'channel': config.SLACK_CHANNEL,
    'text': 'SeatGeek Cheapest Ticket: $' + str(lowest_price)
  }
  response = requests.post(request_url, headers=request_headers, json=request_body)


if config.ENV != 'prod' and '__main__' in __name__:
  # run the handler when executing this file in a non-prod env
  handler()
