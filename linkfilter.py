from redbot.core import commands
from redbot.core import Config
import logging

log = logging.getLogger("red.linkfilter.linkfilter")
class LinkFilter(commands.Cog):
	def __init__(self):
		self.config = Config.get_conf(self, identifier=280102)
		# Blacklist is shared between guilds
		default_global = {
			"blacklist": []
		}
		# The logs channel is defined per guild
		default_guild = {
			"logchannel": False
		}
		# Register default values
		self.config.register_global(**default_global)
		self.config.register_guild(**default_guild)

	@commands.Cog.listener()
	async def on_message(self, message):
		# Stop recursion or private messages stuff
		if message.author.bot or not message.guild:
			return

	@commands.command()
	async def test(self, ctx):
		await ctx.send(await self.config.foo())