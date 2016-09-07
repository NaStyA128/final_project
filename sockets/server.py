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
    """Interface for stream protocol.

    The user should implement this interface.

    When the user wants to requests a transport, they pass a protocol
    factory to a utility function (e.g., EventLoop.create_connection()).
    """

    def onConnect(self, request):
        """Callback fired during WebSocket opening handshake when new WebSocket client
        connection is about to be established.

        When you want to accept the connection, return the accepted protocol
        from list of WebSocket (sub)protocols provided by client or `None` to
        speak no specific one or when the client protocol list was empty.

        You may also return a pair of `(protocol, headers)` to send additional
        HTTP headers, with `headers` being a dictionary of key-values.

        Args:
            request: WebSocket connection request information.
        """
        # print("Client connection: {0}".format(request.peer))
        self.factory.clients[request.peer] = self
        global now_client
        now_client = request.peer

    def onOpen(self):
        """WebSocket connection open.

        WebSocket connection established. Now let the user WAMP
        session factory create a new WAMP session and fire off
        session open callback.
        """
        # print("WebSocket connection open.")
        global now_client
        self.sendMessage(now_client.encode('utf8'))

    def onMessage(self, payload, isBinary):
        """Callback fired when receiving of a new WebSocket message.

        Args:
            payload: a message.
            isBinary: True if payload is binary, else the payload is UTF-8 encoded text.
        """
        global now_client
        now_client = payload.decode('utf8')

    def onClose(self, wasClean, code, reason):
        """WebSocket connection closed.

        Callback fired when the WebSocket connection has been
        closed (WebSocket closing handshake has been finished
        or the connection was closed uncleanly).

        Args:
            wasClean: True if the WebSocket connection was closed cleanly.
            code: Close status code as sent by the WebSocket peer.
            reason: Close reason as sent by the WebSocket peer.
        """
        self.factory.clients.pop(self.peer)
        # print("WebSocket connection closed: {0}".format(reason))


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
                factory.clients[now_client].sendMessage(
                    message['google'].encode('utf8')
                )
                message = {
                    'google': '',
                    'yandex': '',
                    'instagram': ''
                }
                now_client = ''
            # print('Received: ', repr(reply.value), 'on channel',
            #       reply.channel)

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
