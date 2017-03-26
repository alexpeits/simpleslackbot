# simpleslackbot

Simple wrapper for Slack's RTM API for quick bot implementations

## Installation

```
$ git clone https://github.com/alexpeits/simpleslackbot.git
$ cd simpleslackbot
$ mkvirtualenv slackbot
$ pip install .
```

## Usage

```python
from simpleslackbot.bot import BaseSlackBot

TOKEN = 'your-slack-token'

def handler(events):
    for event in events:
        print(event)

if __name__ == '__main__':
    sc = BaseSlackBot(TOKEN)
    sc.initialize()
    sc.start(handler)
```
