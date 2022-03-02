import aiovk


class Vk:

    def __init__(self, token):
        self.group_id = None
        vk_session = aiovk.TokenSession(access_token=token)
        vk_session.API_VERSION = "5.131"
        self.api = aiovk.API(vk_session)
        
    async def find_self_id(self):
        print(await self.api.groups.getById())
        self.group_id = 1

    async def longpoll(self):
        pass
        # longpoll = aiovk.longpoll.BotsLongPoll(self.api, group_id=self.group_id, wait=5)

    async def run(self):
        await self.find_self_id()
        await self.longpoll()
