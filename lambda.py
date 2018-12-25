import config


def handler(event=None, context=None):
  pass


if config.ENV != 'prod' and '__main__' in __name__:
  # run the handler when executing this file in a non-prod env
  handler()
