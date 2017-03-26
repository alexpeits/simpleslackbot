import re
import time

from decouple import config

from simpleslackbot.bot import BaseSlackBot
from simpleslackbot.utils import filter_channel
from simpleslackbot.exceptions import SlackAppExit


TOKEN = config('USER_TOKEN')
GET_IP_CMD = 'ip'
IP_RE = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
MAX_TIME = 10


def handler_wrapper(channel_name, sc):
    channels_list = sc.api_call('channels.list')['channels']
    channel = filter_channel(channel_name, channels_list)

    def request_ip():
        sc.api_call(
            'chat.postMessage',
            channel=channel['id'],
            text=GET_IP_CMD,
            as_user=True
        )

    request_ip()
    started = time.time()

    def handler(events):
        if time.time() - started > MAX_TIME:
            raise SlackAppExit()
        for event in events:
            if ('channel' not in event or
                    event['channel'] != channel['id'] or
                    event['type'] != 'message'):
                continue
            if 'text' in event and IP_RE.match(event['text']):
                print(event['text'])
                raise SlackAppExit()

    return handler


if __name__ == '__main__':
    sc = BaseSlackBot(TOKEN)
    sc.initialize()
    sc.start(handler_wrapper('services', sc))
