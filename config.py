import os


# secrets
ENV = os.environ.get('ENV', 'local')
SEATGEEK_API_KEY = os.environ['SEATGEEK_API_KEY']

# api endpoints
SEATGEEK_ENDPOINT = 'https://api.seatgeek.com/2/events/{}?client_id=' + SEATGEEK_API_KEY

# event ids for the NFC Championship game
SEATGEEK_EVENT_ID = '4628040'
