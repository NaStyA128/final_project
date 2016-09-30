import asyncio_redis
from ast import literal_eval
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):
    """Interface for stream protocol.

    The user should implement this interface.

    When the user wants to requests a transport, they pass a protocol
    factory to a utility function (e.g., EventLoop.create_connection()).
    """

    _sites = ['google', 'yandex', 'instagram']

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
        pass

    def onOpen(self):
        """WebSocket connection open.

        WebSocket connection established. Now let the user WAMP
        session factory create a new WAMP session and fire off
        session open callback.
        """
        pass

    def onMessage(self, payload, isBinary):
        """Callback fired when receiving of a new WebSocket message.

        Args:
            payload: a message.
            isBinary: True if payload is binary, else the payload is UTF-8 encoded text.
        """
        payload = literal_eval(payload.decode('utf-8'))

        for site in self._sites:
            self.factory.search_engines[site].setdefault(payload['keyword'], {
                'address': {self.peer: self}, 'counter': False})
            self.factory.search_engines[site][payload['keyword']][
                'address'].setdefault(self.peer, self)

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
        for tags in self.factory.search_engines.values():
            for clients in tags.values():
                if self.peer in clients['address']:
                    del(clients['address'][self.peer])
                    clients['counter'] = False

        for site in self._sites:
            self.factory.search_engines[site] = {k: v for k, v in
                                                 self.factory.search_engines[
                                                     site].items() if
                                                 v['counter']}
        # print("WebSocket connection closed: {0}".format(reason))


class MyFactory(WebSocketServerFactory):
    search_engines = {
        'google': {},
        'yandex': {},
        'instagram': {}
    }


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
        connection = yield from asyncio_redis.Connection.create(
            host='localhost',
            port=6379
        )

        # Create subscriber
        subscriber = yield from connection.start_subscribe()

        # Subscribe to channel.
        yield from subscriber.subscribe([
            'google',
            'yandex',
            'instagram'
        ])

        # Inside a while loop, wait for incoming events.
        while True:
            reply = yield from subscriber.next_published()

            key_dict = factory.search_engines[reply.channel][reply.value]
            key_dict['counter'] = True

            if factory.search_engines['google'][reply.value]['counter'] \
                and factory.search_engines['yandex'][reply.value]['counter'] \
                    and factory.search_engines['instagram'][reply.value]['counter']:
                for client in key_dict['address'].values():
                    client.sendMessage(reply.value.encode('utf8'))

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

