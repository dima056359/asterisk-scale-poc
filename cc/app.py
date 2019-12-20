import aiohttp
from aiohttp import web
import asyncio
import asynqp
import logging
import json
import yaml

RECONNECT_RATE = 1

logger = logging.getLogger(__name__)


class Context:

    def __init__(self):

        self.api_endpoint = "http://localhost:8888"
        self.api_username = "wazo"
        self.api_password = "wazo"
        self.amqp_host = "127.0.0.1"
        self.amqp_port = 5672
        self.amqp_username = "guest"
        self.amqp_password = "guest"
        self.amqp_exchange = "wazo"

    def from_conf(self, conf="app.yml"):
        doc = yaml.load(conf)

        self.api_endpoint = doc.api.api_endpoint
        self.api_username = doc.api.username
        self.api_password = doc.api.password

        self.amqp_host = doc.amqp.host
        self.amqp_port = doc.amqp.port
        self.amqp_username = doc.amqp.username
        self.amqp_password = doc.amqp.password
        self.amqp_exchange = doc.amqp.exchange


class Channel:

    def __init__(self, obj):
        self.obj = obj

    @property
    def dialplan(self):
        return self.obj.get('dialplan', {})

    @property
    def app_name(self):
        dialplan = self.dialplan
        return dialplan.get('app_data')

    @property
    def id(self):
        return self.obj.get('id')

    @property
    def state(self):
        return self.obj.get('state')


class Consumer:

    def __init__(self, queue):
        self.queue = queue

    def __call__(self, msg):
        self.queue.put_nowait(msg)

    def on_error(self, exc):
        logging.error("Connection lost while consuming queue : %s" % exc)


class Application:

    def __init__(self, context, name):
        self.context = context
        self.name = name

    def launch(self):
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()

        reconnect_task = loop.create_task(self.reconnector(queue))
        process_msgs_task = loop.create_task(
            self.process_msgs(queue))

        app_task = loop.create_task(self.run())

        try:
            loop.run_until_complete(app_task)
        finally:
            reconnect_task.cancel()
            process_msgs_task.cancel()

            loop.run_until_complete(reconnect_task)
            loop.run_until_complete(process_msgs_task)

            loop.close()

    async def connect_and_consume(self, queue):
        connection = await asynqp.connect(
            self.context.amqp_host, self.context.amqp_port,
            username=self.context.amqp_username,
            password=self.context.amqp_password)
        try:
            channel = await connection.open_channel()
            exchange = await channel.declare_exchange(
                self.context.amqp_exchange, 'topic')

            amqp_queue = await channel.declare_queue()
            await amqp_queue.bind(exchange, '#')

            consumer = Consumer(queue)
            await amqp_queue.consume(consumer)

        except asynqp.AMQPError as err:
            logging.error("Could not consume on queue %s" % err)
            await connection.close()
            return None
        return connection

    async def reconnector(self, queue):
        try:
            connection = None
            while True:
                if connection is None or connection.is_closed():
                    logging.info("Connecting to rabbitmq...")
                    try:
                        connection = await self.connect_and_consume(queue)
                    except (ConnectionError, OSError):
                        logging.error("Failed to connect to rabbitmq server. "
                                      "Will retry in {} seconds".format(RECONNECT_RATE))
                        connection = None
                    if connection is None:
                        await asyncio.sleep(RECONNECT_RATE)
                    else:
                        logging.info("Successfully connected and consuming")
                        await self.register()

                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            if connection is not None:
                await connection.close()

    async def process_msgs(self, queue):

        type_state_cb = {
            'StasisStart/Ring': self.onStart,
            'ChannelStateChange/Up': self.onUp,
            'StasisEnd/Up': self.onEnd
        }

        try:
            while True:
                msg = await queue.get()

                obj = json.loads(msg.body)

                asterisk_id = obj.get('asterisk_id', '')

                typ = obj.get('type', '')
                channel = Channel(obj.get('channel', {}))

                key = "%s/%s" % (typ, channel.state)

                callback = type_state_cb.get(key)
                if callback:
                    # NOTE will be handled by a higher level component
                    if channel.app_name == self.name:
                        await callback(asterisk_id, channel)

                msg.ack()
        except asyncio.CancelledError:
            pass

    async def request(self, asterisk_id, path):
        headers = {'X-Asterisk-ID': asterisk_id}
        url = "%s%s" % (self.context.api_endpoint, path)

        logging.debug("Sending request to %s : %s" % (asterisk_id, url))

        return await self.post(url, headers=headers)

    async def post(self, url, headers={}):
        auth = aiohttp.BasicAuth(
            login=self.context.api_username,
            password=self.context.api_password)
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post(url) as response:
                return response

    async def register(self):
        logging.info("Registering application %s" % self.name)

        # NOTE this will change in order to make a call toward consul
        response = await self.post(
            "%s/ari/amqp/%s" % (self.context.api_endpoint, self.name))
        if response.status <= 299:
            logging.info("Application %s registered" % self.name)
        else:
            logging.error("Error while registering application %s : %s" % (
                self.name, response.reason))

    async def answer(self, asterisk_id, channel):
        logging.info("Answering call on channel : %s" % channel.id)
        response = await self.request(asterisk_id, "/ari/channels/%s/answer" % channel.id)
        if response.status <= 299:
            logging.info("Answered channel %s successful" % channel.id)
        else:
            logging.error("Error while answering channel %s : %s" % (
                channel.id, response.reason))

    def run(self):
        pass

    async def onStart(self, asterisk_id, channel):
        pass

    async def onEnd(self, asterisk_id, channel):
        pass

    async def onUp(self, asterisk_id, channel):
        pass
