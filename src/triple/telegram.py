import logging

from aiogram import Bot, Dispatcher, types


class Telegram:

    def __init__(self, token: str, handler, loop, content_types):
        """  """
        self.log: logging.Logger = logging.getLogger("Telegram")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")

        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher(self.bot, loop)

        self.__debug(f"Bot: {self.bot}")
        self.handler = handler
        self.content_types = content_types

    async def start_handler(self, event: types.Message):
        """  """
        answer, _ = await self.handler('tg_event', event, self)
        if answer:
            await event.answer(
                answer,
                parse_mode=types.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )

    async def run(self):
        """  """
        kwargs = {
            "callback": self.start_handler,
            "content_types": self.content_types
        }
        while True:
            try:
                self.dispatcher.register_message_handler(**kwargs)
                self.dispatcher.register_edited_message_handler(**kwargs)
                print("Telegram bot started!")
                self.__debug("Run")
                await self.dispatcher.start_polling()
            finally:
                await self.bot.close()
