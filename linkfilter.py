from redbot.core import commands
import logging

log = logging.getLogger("red.linkfilter.linkfilter")
class LinkFilter(commands.Cog):

	@commands.Cog.listener()
	async def on_message(self, message):
		# Stop recursion or private messages stuff
		if message.author.bot or not message.guild:
			return

		