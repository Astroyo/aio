import aiohttp

from nextcord import Embed, Webhook, Guild
from nextcord.ext import commands
from nextcord.utils import MISSING

from src.constants import Webhooks

class event_listeners(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    async def sendUpdate(self, *args, **kwargs):
        if not Webhook.GUILD:
            return
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(Webhooks.Guild, session=session)
            await webhook.send(username=f'Updates: ({self.bot.user})', *args, **kwargs)

    def guildEventEmbed(self, guild, status, color):
        return Embed(
            title = f"Guild {status}",
            color = color,
            description = '\n'.join([
                f'> Name: {guild.name}  ||{guild.id}||',
                f'> Owner: {guild.owner.mention} {guild.owner} ||{guild.owner_id}||',
                f'> Total Members: {len(guild.humans)} humans + {len(guild.bots)} bots = {guild.member_count}',
            ])
        ).set_footer(
            text = f"Guild Count: {len(self.bot.guilds)}"
        ).set_thumbnail(
            url = guild.icon
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.sendUpdate(embed = self.guildEventEmbed(guild, 'Joined', 0x5865F2))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.sendUpdate(embed = self.guildEventEmbed(guild, 'Left', 0xF13F43))

    # TODO : setup the error handlers
    # nextcord.on_error(event, *args, **kwargs)
    # nextcord.ext.application_checks.on_application_command_error(interaction, error)
    # nextcord.ext.commands.on_command_error(ctx, error)

def setup(bot):
    bot.add_cog(event_listeners(bot))