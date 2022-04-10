import discord
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands

TOKEN = open("token.txt", "r").read()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
guild_ids = []


@bot.event
async def on_ready():
    global guild_ids
    print('Logged in as {0.user}'.format(bot))
    guild_ids = [guild.id for guild in bot.guilds]


@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'({channel[:10]}) - {username}: {user_message}')


@slash.slash(name="test", description="this is to test slash commands", guild_ids=guild_ids)  # TODO: GODO FIX!
async def test(ctx: SlashContext):
    print("Received")
    await ctx.send(content="Success!")


bot.run(TOKEN)
