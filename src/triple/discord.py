import logging

import discord


class Discord(discord.Client):

    def __init__(self, token, handler, loop, **options):
        super().__init__(**options)
        self.log: logging.Logger = logging.getLogger("Discord")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")

        self.loop = loop

        self.handler = handler

    async def on_ready(self):
        print(f'Discord bot started! Bot ID: {self.user.id}')

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            return

        answer = await self.handler('ds_event', message, self)
        if answer[0]:
            await message.reply(
                answer[0]
            )

    async def run(self, *args, **kwargs):
        try:
            await self.start(*args, **kwargs)
        finally:
            if not self.is_closed():
                await self.close()
