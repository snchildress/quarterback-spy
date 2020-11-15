# Quarterback Spy

Quarterback Spy is a ticket marketplace polling service to find cheap tickets for sale at a given event

## Supported Features

Quarterback Spy was created to find and alert on an affordable ticket to the New Orleans Saints 2018 NFC Championship game. As such, it polls the supported ticket marketplaces and logs the cheapest price

### Supported Ticket Marketplaces

- SeatGeek

## Getting Started

1. Create and instantiate a virtual environment: `virtualenv venv && source venv/bin/activate`
2. Install all dependencies: `pip install -r requirements.txt`
3. Obtain and set all secrets as environment variables as a `.env` file (see example.env): `source local.env`
4. Execute the handler locally: `python lambda.py`

## Deployments

Quarterback Spy is a serverless application hosted on AWS Lambda using the Serverless Framework for deployment management

### Deployment Set Up

You'll need to have Docker installed on your machine to build prod with the required dependencies

1. Configure your AWS account's `aws_access_key_id` and `aws_secret_access_key` as the `[personal]` profile in `~/.aws/credentials`
2. Set all of your production environment variables in `prod.env.yml`
3. Install the Serverless Framework and Python dependencies plugin: `npm i`

Deploy to your production environment with `serverless deploy`
