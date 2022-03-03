from typing import Optional

import aiogram
import aiovk
import discord


class Vkontakte:

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


class Telegram:

    def __init__(self, client, api, raw: dict):
        self.client: aiogram.Bot = client
        self.api: aiogram.Dispatcher = api

        self.date: int = raw.get("date")
        self.user_id: int = raw['from'].get('id')
        self.chat_id: int = raw.get("date")
        self.message_id: int or None = raw.get("message_id")
        self.attachments: list = raw.get("date")
        self.text: str = raw.get("text")

        self.raw: dict = raw


class Discord:

    def __init__(self, client, api, raw: dict):
        self.client: discord.Client = client
        self.api = api

        self.date: int = raw.get("date")
        self.from_id: int = raw.get("date")
        self.chat_id: int = raw.get("date")
        self.message_id: int or None = raw.get("date")
        self.attachments: list = raw.get("date")
        self.text: str = raw.get("date")

        self.raw: dict = raw
