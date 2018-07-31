from rocketchat import *
import re

"""
Simple hello method, that will take anything after 'hello' as the users name
and responsd to them with a fiendly message
"""
def hello(bot, fields):
    # The contents of the users message will be in fields['args'][0]['msg']
    message = str (fields['args'][0]['msg'])

    # To get the name we can use a Regular Expression
    # https://docs.python.org/3/library/re.html#match-objects
    # These are quite complex, but the developers can explain them to you.
    name = ""
    matches = re.match("hello (.*)", message)
    #If we find something after hello, we assume it's the name
    if matches:
        name = matches.group(1);

    # Send a response with the users name
    bot.sendMessage(fields['args'][0]['rid'], "Hello %s, how are you doing today?" % name)


"""
Simple string calculator method
This takes the string, splits the string using spaces
Each part of the string will then attempt to convert to numbers
Total is returned to the user
"""
def sumup(bot, fields):
    # define a total value
    total = 0.00
    message = str(fields['args'][0]['msg'])

    #split the string into bits, this creates a list of all of the numbers
    stringBits = message.split(' ')

    #iterate over the bits os string
    for bit in stringBits:

        # Use a Try/Except as we will attempt to convert strings into numbers, which will throw an error
        try:
            # convert the string to a float and add to the total
            total += float(bit)

        except ValueError as valueError:
            # If we get an error, just ignore it...
            pass

    # Send the response to the channel.
    bot.sendMessage(fields['args'][0]['rid'], "Thank you for using the Adder. The result is %f" % total)



rocket = RocketChatBot('admin', 'admin')
rocket.addPrefixHandler('hello', hello)
rocket.addPrefixHandler('sum', sumup)
rocket.start()
