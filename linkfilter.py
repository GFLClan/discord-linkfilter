from redbot.core import commands

class LinkFilter(commands.Cog):
	"""
		Prevents malitious links from being posted
		This works in a blacklist fashion, where you prohibit domains
	"""

	@commands.command()
	async def placeholder(self, ctx):
		await ctx.send("HELL")