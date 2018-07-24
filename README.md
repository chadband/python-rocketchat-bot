# python-rocketchat-bot
rocket.chat python basic bot using dpp

# dependancies
`emerge -va python-meteor`
or
`pip install python-meteor`

# usage
```
from deps.rocketchat import *

def hello(bot, fields):
    bot.sendMessage(fields['args'][0]['rid'], "React from hello command")

rocket = RocketChatBot('username', 'password')
rocket.addPrefixHandler('hello', hello)
rocket.start()
```
