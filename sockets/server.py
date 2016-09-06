import asyncio_redis
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


message = {
    'google': '',
    'yandex': '',
    'instagram': ''
}
now_client = ''


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connection: {0}".format(request.peer))
        self.factory.clients[request.peer] = self
        global now_client
        now_client = request.peer
        print(self.factory.clients)

    def onOpen(self):
        print("WebSocket connection open.")
        global now_client
        self.sendMessage(now_client.encode('utf8'))

    def onMessage(self, payload, isBinary):
        global now_client
        now_client = payload.decode('utf8')
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        self.factory.clients.pop(self.peer)
        print("WebSocket connection closed: {0}".format(reason))


class MyFactory(WebSocketServerFactory):
    clients = {}


if __name__ == "__main__":
    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    factory = MyFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    @asyncio.coroutine
    def my_function():
        # Create connection
        print("MY FUNCTION")
        connection = yield from asyncio_redis.Connection.create(
            host='localhost',
            port=6379
        )

        # Create subscriber
        subscriber = yield from connection.start_subscribe()

        # Subscribe to channel.
        yield from subscriber.subscribe([
            'google-channel',
            'yandex-channel',
            'instagram-channel'
        ])

        # Inside a while loop, wait for incoming events.
        while True:
            reply = yield from subscriber.next_published()
            global message
            if reply.channel == 'google-channel':
                message['google'] = reply.value
            if reply.channel == 'yandex-channel':
                message['yandex'] = reply.value
            if reply.channel == 'instagram-channel':
                message['instagram'] = reply.value
            if message['google'] and message['yandex'] and message['instagram']:
                global now_client
                # self.sendMessage(message['google'].encode('utf8'))
                factory.clients[now_client].sendMessage(
                    message['google'].encode('utf8')
                )
                message = {
                    'google': '',
                    'yandex': '',
                    'instagram': ''
                }
                now_client = ''
            print('Received: ', repr(reply.value), 'on channel',
                  reply.channel)

        # When finished, close the connection.
        connection.close()

    corot = loop.run_until_complete(my_function())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
