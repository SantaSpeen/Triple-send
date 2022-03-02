import json
import os
import sys
import logging
from .exceptions import NoEnoughTokens


class Triple:

    def __init__(self,
                 vk_token=None,
                 tg_token=None,
                 ds_token=None,
                 config_path="./config/polling.json"):
        self.log: logging.Logger = logging.getLogger("triple")
        self.debug: logging.Logger.debug = self.log.debug

        self.debug(f"__init__(self, {vk_token=}, {tg_token=}, {ds_token=}, {config_path=})")

        self._fast_print = sys.stdout.write
        self._config_path: str = config_path

        self.tokens: dict = {
            "vk": vk_token,
            "tg": tg_token,
            "ds": ds_token
        }

        self.__read_config()
        self.debug(f"{self.tokens=}")

        if not any(self.tokens.values()):
            error_string = f"You have not entered any tokens or they have not been detected at \"{self._config_path}\""
            self.debug(error_string)
            raise NoEnoughTokens(error_string)

    def __read_config(self):
        self.debug("__read_config(self)")
        if os.path.isfile(self._config_path):
            self.debug(f"Config file: %s - found" % self._config_path)
            with open(self._config_path, 'r') as f:
                config = json.load(f)
        else:
            self.debug(f"Cannot found config file at %s. Use default." % self._config_path)
            config = dict()

        self.tokens.update({
            "vk": config.get("vk_token") or self.tokens['vk'],
            "tg": config.get("tg_token") or self.tokens['tg'],
            "ds": config.get("ds_token") or self.tokens['ds']
        })

    def run(self):
        pass
