import requests
from decouple import config

from ipbot.bot import BaseSlackBot
from ipbot.utils import filter_channel

TOKEN = config('BOT_TOKEN')
GET_IP_CMD = ['home_ip', 'ip', '~home_ip', '~ip']
GET_IP_URL = 'http://ipv4.icanhazip.com/'


def get_ip():
    try:
        resp = requests.get(GET_IP_URL)
        if resp.status_code != 200:
            raise requests.RequestException
        return resp.text.strip()
    except requests.RequestException:
        return 'Error trying to fetch IP'


def handler_wrapper(channel_name, sc):
    channels_list = sc.api_call('channels.list')['channels']
    channel = filter_channel(channel_name, channels_list)
    print('Found channel {}'.format(channel))

    def handler(events):
        for event in events:
            if ('channel' not in event or
                    event['channel'] != channel['id'] or
                    event['type'] != 'message'):
                continue
            if 'text' in event and event['text'] in GET_IP_CMD:
                print('Received command')
                ip = get_ip()
                print('IP is {}'.format(ip))
                sc.api_call(
                    'chat.postMessage',
                    channel=channel['id'],
                    text=ip,
                    as_user=True
                )
                break

    return handler


if __name__ == '__main__':
    sc = BaseSlackBot(TOKEN)
    sc.initialize()
    print('Initialized')
    sc.start(handler_wrapper('services', sc))
