import asyncio
import signal
import traceback
import logging

from nextcord.client import _cleanup_loop

from src.bot import Bot
from src.constants import EnvVars, Config
from src.logger import _log

_log = logging.getLogger(__name__)

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

async def run_bot(bot: Bot):
    try:
        await bot.before_start(_loop)
        await bot.login(EnvVars.BOT_TOKEN)
        _log.info("connecting to websocket")
        await bot.connect(reconnect=Config.RECONNECT)
    except KeyboardInterrupt:
        _log.info("Bot interrupted")
    except Exception as e:
        _log.error(f"An error occurred: {e}\n{traceback.format_exc(traceback)}")
    finally:
        if not bot.is_closed():
            await bot.close()

async def close_bot(bot: Bot) -> None:
    _log.info("Closing the Bot")
    await bot.close()
    _log.info("Bot successfully closed")

def stop_loop(*args, **kwargs):
    _loop.stop()

if __name__ == "__main__":
    bot = Bot()

    try:
        _loop.add_signal_handler(signal.SIGINT, stop_loop)
        _loop.add_signal_handler(signal.SIGTERM, stop_loop)
    except NotImplementedError:
        pass

    future = asyncio.ensure_future(run_bot(bot), loop=_loop)
    future.add_done_callback(stop_loop)
    try:
        _loop.run_forever()
    except KeyboardInterrupt:
        _log.info("Received signal to terminate bot and event loop.")
    finally:
        future.remove_done_callback(stop_loop)
        _loop.run_until_complete(close_bot(bot))
        _log.info("Cleaning up tasks and closing the bot.")
        _cleanup_loop(_loop)
        _loop.close()
