from redbot.core import commands
from redbot.core import Config
import discord
import re

class LinkFilter(commands.Cog):
	def __init__(self):
		# Regular expression
		self.Re = r"\b([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b"
		# Config init
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
		self.blacklist = []

	# Load blacklist
	async def initialize(self):
		self.blacklist = await self.config.blacklist()


	@commands.Cog.listener()
	async def on_message(self, message):
		# Stop recursion, private message checking and people with perms
		if message.author.bot or not message.guild:
			return
		# Try to match a blacklisted domain
		result = re.search(self.Re, message.content.lower(), re.MULTILINE | re.VERBOSE)
		# Now try to find a blacklisted domain
		if result:
			for domain in self.blacklist:
				if domain in result.group(0):
					# Remove the message
					try:
						await message.delete()
					except discord.Forbidden:
						pass
					except discord.NotFound:
						pass

					# Respond
					await message.channel.send(f"{message.author.mention}! You sent a blacklisted link and your message has been removed.")
					#Log
					logchannel = await self.config.guild(message.guild).logchannel()
					channel = message.guild.get_channel(logchannel)
					if channel:
						await channel.send(f"[`{message.created_at.strftime('%H:%M:%S')}`] :wastebasket: {str(message.author)} (`{message.author.id}`) posted a blacklisted domain!\n**Match**: `{result.group(0)}`\n**Message**: {message.content}")
					# Stop looking for domains
					break
		
	@commands.command()
	#@commands.has_guild_permissions(manage_messages=True)
	@commands.guild_only()
	async def linkfilter(self, ctx, action, *args):
		# Defines log channel
		if action == "log":
			if len(ctx.message.channel_mentions) > 0:
				channel = ctx.message.channel_mentions[0]
				await self.config.guild(ctx.guild).logchannel.set(channel.id)
				# Respond
				await ctx.send(f"Set linkfilter's log channel to {channel.mention}")
				# Log
				await ctx.guild.get_channel(channel.id).send(f"[`{ctx.message.created_at.strftime('%H:%M:%S')}`] :pencil: {str(ctx.author)} (`{ctx.author.id}`) set linkfilter's log channel to {channel.mention}.")
			else:
				await ctx.send("Please specify a channel to log linkfilter.")
		# Adds to blacklist
		elif action == "add":
			# Cache logs channel
			logchannel = await self.config.guild(ctx.guild).logchannel()
			channel = ctx.guild.get_channel(logchannel)
			# For each domain given
			for arg in args:
				# Check if it's duplicated
				if arg in self.blacklist:
					await ctx.send(f"`{arg}` is already on the blacklist!")
				# Validate
				elif re.match(self.Re, arg):
					# Add to config
					async with self.config.blacklist() as blacklist:
						blacklist.append(arg)
					# Add to blacklist cache
					self.blacklist.append(arg)

					# Respond
					await ctx.send(f"Added `{arg}` to the blacklisted domains.")

					# Log
					if channel:
						await channel.send(f"[`{ctx.message.created_at.strftime('%H:%M:%S')}`] :pencil: {str(ctx.author)} (`{ctx.author.id}`) added `{arg}` to the blacklisted domains.")
				else:
					await ctx.send(f"I couldn't validate that domain. My regex is set to `{self.Re}`")
		# Gets all blacklisted links
		elif action == "list":
			# Respond
			await ctx.send(f"{ctx.author.mention} I will send you the blacklisted domains in private.")
			# Create embed
			desc = ""

			for i in range(0, len(self.blacklist)):
				desc = desc + f"**{i + 1}:** {self.blacklist[i]}\n"
			# Send domains
			embed = discord.Embed(title="Blacklisted domains", description=desc, colour=ctx.author.colour)
			await ctx.author.send(content=None, embed=embed)
		# Removes from list
		elif action == "remove":
			# Cache logs channel
			logchannel = await self.config.guild(ctx.guild).logchannel()
			channel = ctx.guild.get_channel(logchannel)
			# For each domain given
			for arg in args:
				try:
					self.blacklist.remove(arg)
					await self.config.blacklist.set(self.blacklist)
					await ctx.send(f"Removed `{arg}` from the blacklist.")
					# Log
					if channel:
						await channel.send(f"[`{ctx.message.created_at.strftime('%H:%M:%S')}`] :pencil: {str(ctx.author)} (`{ctx.author.id}`) removed `{arg}` from the blacklisted domains.")
				except ValueError:
					await ctx.send(f"`{arg}` is not on the blacklist!")