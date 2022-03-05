# -*- coding: utf-8 -*-

# Written by: SantaSpeen
# (c) SantaSpeen 2022
import asyncio
import json
import logging
from http import HTTPStatus

import aiogram
from aiogram import Bot, Dispatcher, types, exceptions

log = logging.getLogger(__name__)
raw_handler = lambda *x: None
_tg = None


class Telegram:

    def __init__(self, token: str, handler, _raw_handler, loop, content_types):
        """  """
        self.log: logging.Logger = log
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {token=}, {handler=})")

        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher(self.bot, loop)

        self.__debug(f"Bot: {self.bot}")
        self.handler = handler
        self.content_types = content_types

        global raw_handler, _tg
        raw_handler = _raw_handler
        _tg = None

    async def start_handler(self, event: types.Message):
        """  """
        answer, _ = await self.handler('tg_event', event, self)
        if answer:
            await event.answer(
                answer,
                parse_mode=types.ParseMode.MARKDOWN,
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
                self.dispatcher.register_message_handler(kwargs['callback'])
                print("Telegram bot started!")
                self.__debug("Run")
                await self.dispatcher.start_polling()
            finally:
                await self.bot.close()


def check_result(method_name, content_type, status_code, body):
    log.debug('Response for %s: [%d] "%r"', method_name, status_code, body)

    if content_type != 'application/json':
        raise exceptions.NetworkError(f"Invalid response with content type {content_type}: \"{body}\"")

    try:
        result_json = json.loads(body)
    except ValueError:
        result_json = {}

    description = result_json.get('description') or body
    parameters = types.ResponseParameters(**result_json.get('parameters', {}) or {})

    if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
        result = result_json.get('result')
        if method_name == "getUpdates":
            if len(result) == 1:
                asyncio.create_task(raw_handler("tg_event", result[0], _tg))
        return result
    elif parameters.retry_after:
        raise exceptions.RetryAfter(parameters.retry_after)
    elif parameters.migrate_to_chat_id:
        raise exceptions.MigrateToChat(parameters.migrate_to_chat_id)
    elif status_code == HTTPStatus.BAD_REQUEST:
        exceptions.BadRequest.detect(description)
    elif status_code == HTTPStatus.NOT_FOUND:
        exceptions.NotFound.detect(description)
    elif status_code == HTTPStatus.CONFLICT:
        exceptions.ConflictError.detect(description)
    elif status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
        exceptions.Unauthorized.detect(description)
    elif status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        raise exceptions.NetworkError('File too large for uploading. '
                                      'Check telegram api limits https://core.telegram.org/bots/api#senddocument')
    elif status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        if 'restart' in description:
            raise exceptions.RestartingTelegram()
        raise exceptions.TelegramAPIError(description)
    raise exceptions.TelegramAPIError(f"{description} [{status_code}]")


aiogram.bot.api.check_result = check_result
