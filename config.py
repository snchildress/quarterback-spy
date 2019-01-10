import os

# secrets
ENV = os.environ.get('ENV', 'local')
SEATGEEK_API_KEY = os.environ['SEATGEEK_API_KEY']
TICKET_CITY_API_KEY = os.environ['TICKET_CITY_API_KEY']
SLACK_API_KEY = os.environ['SLACK_API_KEY']

# api endpoints
SEATGEEK_ENDPOINT = 'https://api.seatgeek.com/2/events/{}?client_id=' + SEATGEEK_API_KEY
TICKET_CITY_ENDPOINT = 'https://api.ticketcity.com/affiliate/events/{}/tickets'
SLACK_ENDPOINT = 'https://slack.com/api/chat.postMessage'

# event ids for the Saints NFC Championship game
SEATGEEK_EVENT_ID = '4628040'
TICKET_CITY_EVENT_ID = '2911133'

# slack channel id
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', 'GF1BK650A')

# affordable price max threshold
MAX_AFFORDABLE_PRICE = int(os.environ['MAX_AFFORDABLE_PRICE'])

# job schedule frequency in minutes
POLLING_RATE = 10
