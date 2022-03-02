import asyncio
import json
import os
import re
import logging
from enum import Enum
from typing import List

import aiogram

from .exceptions import NoEnoughTokens
from .telegram import Telegram

asyncio_loop = asyncio.get_event_loop()


class OnlyFrom(Enum):
    vk = 0
    telegram = 1
    discord = 2
    all = 3


class Triple:

    def __init__(self,
                 vk_token=None,
                 tg_token=None,
                 ds_token=None,
                 prefix=".",
                 config_path="./config/polling.json"):
        self.log: logging.Logger = logging.getLogger("triple")
        self.__debug: logging.Logger.debug = self.log.debug

        self.__debug(f"__init__(self, {vk_token=}, {tg_token=}, {ds_token=}, {config_path=})")

        self.tokens: dict = {
            "vk": vk_token,
            "tg": tg_token,
            "ds": ds_token
        }

        self.prefix = prefix
        self._config_path: str = config_path

        self.__queries = {
            "vk_query": [],
            "tg_query": [],
            "ds_query": []
        }

        self.__read_config()
        self.__debug(f"{self.tokens=}")

        if not any(self.tokens.values()):
            error_string = f"You have not entered any tokens or they have not been detected at \"{self._config_path}\""
            self.__debug(error_string)
            raise NoEnoughTokens(error_string)

    def __str__(self) -> str:
        return f"Triple(vk_token={self.tokens['vk'][0:5]}, tg_token={self.tokens['tg'][0:5]}, ds_token={self.tokens['ds'][0:5]}, config_path={self._config_path})"

    def __repr__(self) -> str:
        return f"Triple(vk_token={self.tokens['vk'][0:5]}, tg_token={self.tokens['tg'][0:5]}, ds_token={self.tokens['ds'][0:5]}, config_path={self._config_path})"

    def __read_config(self):
        self.__debug("__read_config(self)")
        if os.path.isfile(self._config_path):
            self.__debug(f"Config file: %s - found" % self._config_path)
            with open(self._config_path, 'r') as f:
                config = json.load(f)
        else:
            self.__debug(f"Cannot found config file at %s. Use default." % self._config_path)
            config = dict()

        self.tokens.update({
            "vk": config.get("vk_token") or self.tokens['vk'],
            "tg": config.get("tg_token") or self.tokens['tg'],
            "ds": config.get("ds_token") or self.tokens['ds']
        })

    def __found_in_query(self, query, text):
        for v in self.__queries[query]:
            cmd: str or re = v['command']
            regex = v['regex']
            if regex:
                if regex.match():
                    return v
            else:
                if v['is_startswith']:
                    if text.startswith(cmd):
                        return v
                if cmd == text:
                    return v

    async def __message_handler(self, event):
        func = None
        if event.get("tg_event"):
            event: aiogram.types.Message = event['tg_event']
            text = event.text
            func = self.__found_in_query("tg_query", text)

        if func:
            return func['function'](event)

    def on_message(self,
                   commands: list or str,
                   only_from: OnlyFrom or List[OnlyFrom] = OnlyFrom.all,
                   startswith: bool = True,
                   regex: bool = False):
        """
        Add command / commands to query
            Usage:
                pass
            :param commands: >
            :param only_from: >
            :param startswith: >
            :param regex: >
        """

        if isinstance(only_from, list):
            only_from = []
            for of in [only_from]:
                only_from.append(of.value)

        if isinstance(only_from, OnlyFrom):
            only_from = only_from.value

        add_to_list = []

        for of in [only_from]:
            if of == 0:
                add_to_list.append("vk_query")
            elif of == 1:
                add_to_list.append("tg_query")
            elif of == 2:
                add_to_list.append("ds_query")
            else:
                add_to_list.append("vk_query")
                add_to_list.append("tg_query")
                add_to_list.append("ds_query")

        def wrapper(f):

            for cmd in [commands]:
                if regex:
                    regex_compiled = re.compile(cmd)
                else:
                    regex_compiled = None
                    cmd = self.prefix + cmd

                for add_to in add_to_list:
                    self.__debug(f'{add_to=}, {f=}, {cmd=}, {startswith=}, {regex_compiled=}')
                    self.__queries[add_to].append({
                        "function": f,
                        "command": cmd,
                        "is_startswith": startswith,
                        "regex": regex_compiled
                    })

            return f

        return wrapper

    async def async_loop(self):
        tg = Telegram(self.tokens['tg'], self.__message_handler)

        tasks = [
            tg.run()
        ]
        for task in tasks:
            await asyncio.create_task(task)

    def run(self, loop: asyncio.get_event_loop = asyncio_loop) -> None:
        """
        Запуск программы:
            bot.run(asyncio.get_event_loop())

            :param loop: > self asyncio.get_event_loop() or u may input yours
        """

        try:
            loop.run_until_complete(self.async_loop())  # Запуск
        except KeyboardInterrupt:
            self.__debug('Exit')
            loop.stop()
