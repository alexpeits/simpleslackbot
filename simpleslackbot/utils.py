from .exceptions import SlackAppError

def filter_channel(channel_name, channels_list):
    flt = (ch for ch in channels_list if ch['name'] == channel_name)
    try:
        return next(flt)
    except StopIteration:
        raise SlackAppError(
            'No "{}" channel found in channels list'.format(channel_name)
        )
