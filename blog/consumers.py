"""
module docstring
"""

import asyncio
import json

# binance websocket
from binance.client import Client
from binance.websockets import BinanceSocketManager
from channels.consumer import AsyncConsumer
from decouple import config
from django.core.cache import caches


PUBLIC = config('PUBLIC_WEBSOCKET')
SECRET = config('SECRET_WEBSOCKET')

global PRICES
PRICES = {}


def trade_prices(msg):
    """
    define how to process incoming WebSocket messages
    """
    if msg['s'] == 'BTCUSDT':
        PRICES['BTCUSDT'] = [msg['c'], msg['P']]
    elif msg['s'] == 'ETHUSDT':
        PRICES['ETHUSDT'] = [msg['c'], msg['P']]
    elif msg['s'] == 'LTCUSDT':
        PRICES['LTCUSDT'] = [msg['c'], msg['P']]
    elif msg['s'] == 'XRPUSDT':
        PRICES['XRPUSDT'] = [msg['c'], msg['P']]
    elif msg['s'] == 'BCHUSDT':
        PRICES['BCHUSDT'] = [msg['c'], msg['P']]
    elif msg['s'] == 'EOSUSDT':
        PRICES['EOSUSDT'] = [msg['c'], msg['P']]
    caches['other'].set('prices', PRICES)


async def binace_price():
    cache_obj = caches['other'].get('price_exists')
    if cache_obj is not None:
        pass
    else:
        client = Client(api_key=PUBLIC, api_secret=SECRET)
        bsm = BinanceSocketManager(client)
        # Start trade socket with 'BTCUSDT' and use handle_message to.. handle the message.
        conn_key1 = bsm.start_symbol_ticker_socket('BTCUSDT', trade_prices)
        conn_key2 = bsm.start_symbol_ticker_socket('ETHUSDT', trade_prices)
        conn_key3 = bsm.start_symbol_ticker_socket('LTCUSDT', trade_prices)
        conn_key4 = bsm.start_symbol_ticker_socket('XRPUSDT', trade_prices)
        conn_key5 = bsm.start_symbol_ticker_socket('BCHUSDT', trade_prices)
        conn_key6 = bsm.start_symbol_ticker_socket('EOSUSDT', trade_prices)
        bsm.start()
        caches['other'].set('price_exists', 1)


# Consumers are to channels much like views to django
# So we need to specify routing for it
class ChatConsumer(AsyncConsumer):
    """
    class docstring
    """

    async def websocket_connect(self, event):
        print('websocket_connect : ', event)
        await self.send({
            "type": "websocket.accept",
        })

        await binace_price()

        # Show prices continuously
        while True:
            # Cache the prices
            prices = caches['other'].get('prices')

            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(prices),
            })

            # Sleep for 5 seconds
            await asyncio.sleep(5)

    async def websocket_receive(self, event):
        # When the socket receives message
        print('websocket_receive : ', event)

    async def websocket_disconnect(self, event):
        # When the socket disconnect
        print('websocket_disconnect : ', event)
