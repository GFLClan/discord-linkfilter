from .linkfilter import LinkFilter

async def setup(bot):
	cog = LinkFilter()
	await cog.initialize()
	bot.add_cog(cog)