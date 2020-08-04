from redbot.core import commands
import logging

log = logging.getLogger("red.linkfilter.linkfilter")
class LinkFilter(commands.Cog):
	"""
		Prevents malicious links from being posted
		This works in a blacklist fashion, where you prohibit domains
	"""

	@commands.Cog.listener()
	async def on_message(self, message):
		# Stop recursion or private messages stuff
		if message.author.bot or not message.guild:
			return

		