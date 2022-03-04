# -*- coding: utf-8 -*-

# Written by: SantaSpeen
# (c) SantaSpeen 2022
import logging

import discord


class Discord(discord.Client):

    def __init__(self, token, handler, loop, **options):
        super().__init__(**options)
        self.log: logging.Logger = logging.getLogger("Discord")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")
        self.loop = loop
        self.token = token
        self.handler = handler

    async def on_ready(self):
        print(f'Discord bot started! Bot ID: {self.user.id}')

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            return

        answer, _ = await self.handler('ds_event', message, self)
        if answer:
            await message.reply(
                answer
            )

    async def run(self, *args, **kwargs):
        args = list(args)
        args.append(self.token)

        try:
            await self.start(*args, **kwargs)
        finally:
            if not self.is_closed():
                await self.close()
