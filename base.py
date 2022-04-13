import discord
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands

TOKEN = open("token.txt", "r").read()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot)
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
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command(name='test')
async def test(ctx, arg=''):
    print("Received test command")
    await ctx.send(f"test: {arg}")


@bot.command(name='name')
async def name(ctx):
    await ctx.send(f"your name is {ctx.author}")


@slash.slash(name="test2", description="this is to test slash commands", guild_ids=guild_ids)  # TODO: GODO FIX!
async def test2(ctx: SlashContext):
    print("Received slash command")
    await ctx.send(content="Success!")


@slash.slash(name="newtest", description="this is to test slash commands, again", guild_ids=guild_ids)
async def newtest(ctx: SlashContext):
    print("Received slash command")
    await ctx.send(content="Success in new!")


bot.run(TOKEN)
