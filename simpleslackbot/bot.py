import time
import sys

from slackclient import SlackClient
from websocket._exceptions import WebSocketConnectionClosedException

from .exceptions import SlackAppError, SlackAppExit

TIME_WAIT = 1  # seconds


class BaseSlackBot(object):
    def __init__(self, token):
        self._token = token
        self._client = None

    def initialize(self):
        if self._client is not None:
            raise SlackAppError('Cannot initialize twice')
        self._client = SlackClient(self._token)

    def api_call(self, *args, **kwargs):
        return self._client.api_call(*args, **kwargs)

    def start(self, handler):
        if not self._client.rtm_connect():
            raise SlackAppError('RTM connection failed')
        while True:
            try:
                event = self._client.rtm_read()
                try:
                    handler(event)
                except SlackAppExit:
                    break
            except WebSocketConnectionClosedException:
                if not self._client.rtm_connect():
                    raise SlackAppError('RTM connection failed')
        print('Exiting...', file=sys.stderr)
