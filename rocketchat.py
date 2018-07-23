from MeteorClient import MeteorClient
import time

class RocketChatBot():
    def __init__(self, user, password, server='utilities.spencer.org.uk'):
        self.username = user
        self.password = password
        self.server = server
        self.debug = True

        self._prefixs = []

        self.client = client = MeteorClient('wss://utilities.spencer.org.uk/websocket')

        # registering internal handlers
        self.client.on('connected', self._connected)
        self.client.on('closed', self._closed)
        self.client.on('logging_in', self._logging_in)
        self.client.on('failed', self._failed)
        self.client.on('added', self._added)
        self.client.on('changed', self._changed)
        self.client.on('unsubscribed', self._unsubscribed)
        self.client.on('subscribed', self._subscribed)

    """
    Internal events handlers
    """
    def _connected(self):
        print("[+] rocketchat: connected")
        self.client.subscribe('stream-room-messages', ['test-channel', False], self.cb1)
        print("[?] test")
        all_rooms = self.client.find('rooms/get')

    def _closed(self, code, reason):
        print('[-] rocketchat: connection closed: %s (%d)' % (reason, code))

    def _logging_in(self):
        print('[+] rocketchat: logging in')

    def _failed(self, collection, data):
        print('[-] %s' % str(data))

    def _added(self, collection, id, fields):
        print('[+] %s: %s' % (collection, id))
        print('[+] %s: %s' % (collection, fields))

        if not fields.get('args'):
            return

        args = fields['args']

        if args[0] == "GENERAL":
            print("[+] message: general, skipping")
            return

        if args[1].get('msg'):
            return self._incoming(args[1])

        if args[1].get('attachments'):
            return self._downloading(args[1])

        print(args)
        print(args[0])
        print(args[1])


        # for key, value in fields.items():
        #    print('[+]  %s: %s' % (key, value))

    def _changed(self, collection, id, fields, cleared):
        print('[+] changed: %s %s' % (collection, id))

        for key, value in fields.items():
            print('[+]  field %s: %s' % (key, value))

        for key, value in cleared.items():
            print('[+]  cleared %s: %s' % (key, value))

    def _subscribed(self, subscription):
        print('[+] subscribed: %s' % subscription)

    def _unsubscribed(self, subscription):
        print('[+] unsubscribed: %s' % subscription)

    """
    Internal callback handlers
    """
    def cb(self, error, data):
        if not error:
            if self.debug:
                print(data)

            return

        print('[-] callback error:')
        print(error)

    def cb1(self, data):
        if not self.debug:
            return

        if(data):
            print(data)

        else:
            print("[+] callback success")


    """
    Internal dispatcher
    """
    def _incoming(self, data):
        print("[+] Message from %s: %s" % (data['u']['username'], data['msg']))

        for prefix in self._prefixs:
            if data['msg'].startswith(prefix['prefix']):
                prefix['handler'](self, data)

    def _downloading(self, data):
        print("[+] attachement from %s: %d files" % (data['u']['username'], len(data['attachments'])))

    """
    Public initializers
    """
    def start(self):
        self.client.connect()
        self.client.login(self.username, self.password.encode('utf-8'), callback=self.cb)

        # let's yeld to background task
        while True:
            time.sleep(3600)

    def addPrefixHandler(self, prefix, handler):
        self._prefixs.append({'prefix': prefix, 'handler': handler})

    def sendMessage(self, id, message):
        self.client.call('sendMessage', [{'msg': message, 'rid': id}], self.cb)


