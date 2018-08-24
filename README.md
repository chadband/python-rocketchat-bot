# python-rocketchat-bot
rocket.chat python basic bot using dpp

# Introduction

This is a simple rocket chat interface for python, making use of DPP. It requires the meteor client,
but probably needs to be patched. More information below.

# Dependancies

### Meteor

`pip install python-meteor`


## Getting Rocket.Chat

If you're using Ubuntu or another version of Linux that supports the snap framework, Rocket chat can be installed
as simply as `snap install rocketchat-server`. If you're using another system, information can be found
[here](https://rocket.chat/install)

Rocket chat will generally be running on <http://localhost:3000>.


# Usage

Firstly import the base bot

`from rocketchat import RocketChatBot`

Then we need to create an instance

`rocket = RocketChatBot('admin', 'admin', server='localhost:3000', secure=False, channel_id='GENERAL')`

Then we start the bot with 

`rocket.start()`

Username and Password are required, the other parameters are optional based on your setup. However the
defaults should work as expected with a local server.

Then you're ready to write your bot's logic and apply a callable (function) to the bot with a specified
prefix. A basic example is shown below.

```python
from rocketchat import RocketChatBot
import re

"""
Simple hello method, that will take anything after 'hello' as the users name
and responsd to them with a fiendly message
"""
def hello(bot, fields):
    # The contents of the users message will be in fields['args'][0]['msg']
    message = str (fields['args'][0]['msg'])

    name = ""
    matches = re.match("hello (.*)", message)
    #If we find something after hello, we assume it's the name
    if matches:
        name = matches.group(1);

    # Send a response with the users name
    bot.sendMessage(fields['args'][0]['rid'], "Hello %s, how are you doing today?" % name)


rocket = RocketChatBot('admin', 'admin', server='localhost:3000', secure=False, channel_id='GENERAL')
rocket.addPrefixHandler('hello', hello)
rocket.start()

```

An example bot is included in the file bot.py


# Troubleshooting

## Meteor - Error

It seems that the Rocket Chat API has changed and the default Meteor client won't work as expected, you can tell
that this is the case if you get an error (in the python console) when your bot receives a message. In order
to fix this, you will need to patch the meteor client file `MeteorClient.py`. On Ubuntu this file can be found
`~/.local/lib/python3.6/site-packages/MeteorClient.py`, but a search for the filename should allow you to find it.

To update you will need to update the change_data method. This can be found around line 25. Initially the method
looks like;

```python
    def change_data(self, collection, id, fields, cleared):
        for key, value in fields.items():
            self.data[collection][id][key] = value
    
        for key in cleared:
            del self.data[collection][id][key]
```

It needs to be updated so the we adds a series of checks in. The final method will look like;
```python
    def change_data(self, collection, id, fields, cleared):
        if collection not in self.data:
            self.data[collection] = {}
        if not id in self.data[collection]:
            self.data[collection][id] = {}
        for key, value in fields.items():
            self.data[collection][id][key] = value

        for key in cleared:
            del self.data[collection][id][key]

```

Once that's complete it should all work, hopefully.