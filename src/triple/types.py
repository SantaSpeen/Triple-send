import time
from typing import Union

import aiogram
import aiovk
import discord


class MessageObject:
    client: Union[aiovk.TokenSession, aiogram.Bot, discord.Client]
    api: Union[aiovk.API, aiogram.Dispatcher, None]

    date: int
    user_id: int
    chat_id: int
    message_id: Union[list, None]
    attachments: list
    text: str

    raw: dict or discord.Message


class Vkontakte(MessageObject):

    def __init__(self, client, api, raw: dict):
        self.client: aiovk.TokenSession = client
        self.api: aiovk.API = api

        self.date: int = raw.get("date")
        self.user_id: int = raw.get("from_id")
        self.chat_id: int = raw.get("peer_id")
        self.message_id: int or None = raw.get("id")
        self.attachments: list = raw.get("attachments")
        self.text: str = raw.get("text")

        self.raw: dict = raw

    def __repr__(self):
        return f"<Vkontakte date={self.date} user_id={self.user_id} chat_id={self.chat_id} message_id={self.message_id} attachments={self.attachments} text={self.text}>"


class Telegram(MessageObject):

    def __init__(self, client, api, raw: dict):
        raw = dict(raw)
        self.client: aiogram.Bot = client
        self.api: aiogram.Dispatcher = api

        self.date: int = raw.get("date")
        self.user_id: int = raw['from'].get('id')
        self.chat_id: int = raw.get("date")
        self.message_id: int = raw.get("message_id")
        self.attachments: Union[list, None] = None
        self.text: str = raw.get("text")

        self.raw: dict = raw

    def __repr__(self):
        return f"<Telegram date={self.date} user_id={self.user_id} chat_id={self.chat_id} message_id={self.message_id} attachments={self.attachments} text={self.text}>"


class Discord(MessageObject):

    def __init__(self, client, api, raw: discord.Message):
        self.client: discord.Client = client
        self.api = api

        self.date: int = int(time.time())
        self.user_id: int = raw.author.id
        self.chat_id: int = raw.channel.id
        self.message_id: int = raw.id
        self.attachments: list = raw.attachments
        self.text: str = raw.content

        self.raw: discord.Message = raw

    def __repr__(self):
        return f"<Discord date={self.date} user_id={self.user_id} chat_id={self.chat_id} message_id={self.message_id} attachments={self.attachments} text={self.text}>"
