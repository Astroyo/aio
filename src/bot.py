import asyncio
import logging

import nextcord
from nextcord.ext import commands

from src.logger import setup_logging

_log = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=nextcord.Intents.all()
        )
        setup_logging()
    
    async def on_ready(self):
        _log.info(f'{self.user} is online')

    async def before_start(self, loop: asyncio.AbstractEventLoop):
        self.load_extension('src.events')