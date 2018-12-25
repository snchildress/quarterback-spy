import config

import requests


def handler(event=None, context=None):
  # find cheapest seatgeek ticket
  response = requests.get(config.SEATGEEK_ENDPOINT.format(config.SEATGEEK_EVENT_ID))
  if response.ok:
    response_body = response.json()
    lowest_price = response_body['stats']['lowest_price']
    print('SeatGeek Cheapest Ticket: $' + str(lowest_price))


if config.ENV != 'prod' and '__main__' in __name__:
  # run the handler when executing this file in a non-prod env
  handler()
