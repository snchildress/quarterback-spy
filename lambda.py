import config

import requests


def handler(event=None, context=None):
  # create an empty dict to store lowest ticket prices
  lowest_prices = {}

  # find cheapest seatgeek ticket
  response = requests.get(config.SEATGEEK_ENDPOINT.format(config.SEATGEEK_EVENT_ID))
  if response.ok:
    response_body = response.json()
    lowest_prices['SeatGeek'] = str(response_body['stats']['lowest_price'])

  # iterate through the lowest prices to log and post affordable alert to Slack
  for marketplace, lowest_price in lowest_prices.items():
    # log each price in Slack
    print(marketplace + ' Cheapest Ticket: $' + lowest_price)
    if int(lowest_price) < config.MAX_AFFORDABLE_PRICE:
      message = '<!channel> ' + marketplace + ' has an affordable ticket for $' + lowest_price + '!'
      _message_slack(message)

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
