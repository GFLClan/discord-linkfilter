from redbot.core import commands
from redbot.core import Config
from redbot.core import utils
import discord

class LinkFilter(commands.Cog):
	def __init__(self):
		self.config = Config.get_conf(self, identifier=280102)
		# Blacklist is shared between guilds
		self.config.register_global(
			blacklist = []
		)
		# The logs channel is defined per guild
		self.config.register_guild(
			logchannel = False
		)
		# Dummy blacklist
		self.blacklist = False

	@commands.Cog.listener()
	async def on_message(self, message):
		# Cache blacklist
		if not self.blacklist:
			self.blacklist = await self.config.blacklist()
		# Stop recursion or private messages stuff
		if message.author.bot or not message.guild:
			return

	@commands.command()
	async def linkfilter(self, ctx, action, *args):
		# Cache blacklist
		if not self.blacklist:
			self.blacklist = await self.config.blacklist()
		# Defines log channel
		if action == "log":
			if len(ctx.message.channel_mentions) > 0:
				channel = ctx.message.channel_mentions[0]
				await self.config.guild(ctx.guild).logchannel.set(channel.id)
				# Respond
				await ctx.send(f"Set linkfilter's log channel to {channel.mention}")
				# Start logging
				time = ctx.message.created_at
				# Log
				await ctx.guild.get_channel(channel.id).send(f"[`{time.hour}:{time.minute}:{time.second}`] :pencil: {str(ctx.author)} (`{ctx.author.id}`) set linkfilter's log channel to {channel.mention}.")
			else:
				await ctx.send("Please specify a channel to log linkfilter.")
		# Adds to blacklist
		elif action == "add":
			logchannel = await self.config.guild(ctx.guild).logchannel()

			for arg in args:
				# Add to config
				async with self.config.blacklist() as blacklist:
					blacklist.append(arg)
				# Add to blacklist cache
				self.blacklist.append(arg)

				# Respond
				await ctx.send(f"Added `{arg}` to the blacklisted domains.")

				# Log
				time = ctx.message.created_at
				await ctx.guild.get_channel(logchannel).send(f"[`{time.hour}:{time.minute}:{time.second}`] :pencil: {str(ctx.author)} (`{ctx.author.id}`) added `{arg}` to the blacklisted domains.")
		# Gets all blacklisted links
		elif action == "list":
			desc = ""

			for i in range(0, len(self.blacklist)):
				desc = desc + f"**{i + 1}:** {self.blacklist[i]}\n"

			embed = discord.Embed(title="Blacklisted domains", description=desc, colour=ctx.author.colour)
			await ctx.send(content=None, embed=embed)
		# Removes from list
		elif action == "remove":
			for arg in args:
				try:
					self.blacklist.remove(arg)
					await self.config.blacklist.set(self.blacklist)
					await ctx.send(f"Removed `{arg}` from the blacklist.")
				except ValueError:
					await ctx.send(f"`{arg}` is not on the blacklist!")

		#await ctx.send(await self.config.guild(ctx.guild).logchannel())