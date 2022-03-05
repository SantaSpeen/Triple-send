# -*- coding: utf-8 -*-

# Written by: SantaSpeen
# (c) SantaSpeen 2022
import asyncio
import logging

import aiovk


class Vk:

    def __init__(self, token, handler, raw_handler,):
        self.group_id = None

        self.log: logging.Logger = logging.getLogger("vkontakte")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")

        self.vk_session = aiovk.TokenSession(access_token=token)
        self.vk_session.API_VERSION = "5.131"
        self.api = aiovk.API(self.vk_session)

        self.__debug(f"{self.vk_session=}, {self.api=}")

        self.handler = handler
        self.raw_handler = raw_handler

    async def find_self_id(self):
        response = await self.api.groups.getById()
        self.group_id = response[0]['id']

    async def longpoll(self):
        longpoll = aiovk.longpoll.BotsLongPoll(
            self.api,
            group_id=self.group_id
        )

        allowed_events = ['message_new']

        while True:
            try:
                longpoll_object = await longpoll.wait()
                if longpoll_object.get('updates'):
                    event_type: str = longpoll_object['updates'][0]['type']
                    self.__debug(f"Event: %s" % longpoll_object)
                    asyncio.create_task(self.raw_handler("vk_event", longpoll_object['updates'][0], self))
                    if event_type in allowed_events:
                        event_object = longpoll_object['updates'][0]['object']
                        event = event_object
                        if event_type.startswith('message'):
                            event = event_object['message']
                        answer, peer_id = await self.handler("vk_event", event, self)
                        if answer:
                            await self.api.messages.send(message=answer, peer_id=peer_id, random_id=0)

            except Exception as e:
                print(e)

    async def run(self):
        self.__debug("Run")
        await self.find_self_id()
        print(f"Vk bot started! Bot ID: {self.group_id}")
        await self.longpoll()
