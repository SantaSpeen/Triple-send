import logging

import aiovk


class Vk:

    def __init__(self, token, handler):
        self.group_id = None

        self.log: logging.Logger = logging.getLogger("vkontakte")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")

        vk_session = aiovk.TokenSession(access_token=token)
        vk_session.API_VERSION = "5.131"
        self.api = aiovk.API(vk_session)

        self.__debug(f"{vk_session=}, {self.api=}")

        self.handler = handler
        
    async def find_self_id(self):
        response = await self.api.groups.getById()
        self.group_id = response[0]['id']

    async def longpoll(self):
        longpoll = aiovk.longpoll.BotsLongPoll(self.api,
                                               group_id=self.group_id)
        while True:
            try:
                r = await longpoll.wait()
                if r.get('updates'):
                    if r['updates'][0]['type'] == 'message_new':
                        answer = await self.handler({"vk_event": r['updates'][0]['object'].get('message')})
                        if answer[0]:
                            await self.api.messages.send(message=answer[0], peer_id=answer[1][0], random_id=0)
            except Exception as e:
                print(e)

    async def run(self):
        self.__debug("Run")
        await self.find_self_id()
        print(f"Vk bot started! Bot ID: {self.group_id}")
        await self.longpoll()
