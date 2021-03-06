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
    configured game, post them to Slack, and alert
    if the price is below the configured max threshold
    """
    # create an empty dict to store lowest ticket prices and message for Slack
    lowest_prices = {}
    lowest_prices_message = 'Current cheapest 49ers/Saints ticket prices:\n\n'

    # find cheapest SeatGeek ticket
    response = requests.get(
        config.SEATGEEK_ENDPOINT.format(config.SEATGEEK_EVENT_ID))
    if response.ok:
        response_body = response.json()
        lowest_prices['SeatGeek'] = str(response_body['stats']['lowest_price'])

    # iterate through the lowest prices to log and post affordable alert to Slack
    for marketplace, lowest_price in lowest_prices.items():
        lowest_prices_message += marketplace + ': $' + lowest_price + '\n'
        if int(lowest_price) < config.MAX_AFFORDABLE_PRICE:
            message = '<!channel> ' + marketplace + \
                ' has an affordable 49ers/Saints ticket for $' + lowest_price + '!'
            _message_slack(message)

    # if it is currently the job closest to the top of the hour
    current_minute = datetime.now().minute
    if (current_minute < config.POLLING_RATE / 2) \
            or (current_minute > (60 - config.POLLING_RATE / 2)):
        # post all of the lowest prices to Slack
        # remove the trailing new line
        lowest_prices_message = lowest_prices_message[:-1]
        _message_slack(lowest_prices_message)

    # log the lowest prices as a JSON object
    logger.info(json.dumps(lowest_prices))


def _message_slack(message, api_key=config.SLACK_API_KEY,
                   channel_id=config.SLACK_CHANNEL):
    """
    Internal function to post a given message to the
    configured Slack channel
    """
    url = config.SLACK_ENDPOINT
    headers = {'Authorization': 'Bearer ' + api_key}
    body = {
        'channel': channel_id,
        'text': str(message),
    }
    requests.post(url, headers=headers, json=body)


if config.ENV != 'prod' and '__main__' in __name__:
    # run the handler when executing this file in a non-prod env
    handler()
