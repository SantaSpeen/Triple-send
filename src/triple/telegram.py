from aiogram import Bot, Dispatcher, types


class Telegram:

    def __init__(self, token: str, handler):
        self.bot = Bot(token=token)
        self.handler = handler

    async def start_handler(self, event: types.Message):
        answer = await self.handler({'tg_event': event})
        if answer:
            await event.answer(
                answer,
                parse_mode=types.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )

    async def run(self):
        while True:
            try:
                disp = Dispatcher(bot=self.bot)
                disp.register_message_handler(self.start_handler)
                await disp.start_polling()
            finally:
                await self.bot.close()
