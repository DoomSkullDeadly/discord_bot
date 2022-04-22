import discord
import json
from discord.ext import commands

with open("token.txt", "r") as f:
    TOKEN = f.read()
bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())
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


@bot.command(name='say')
async def bot_list(ctx, *args):
    await ctx.send("{}".format(" ".join(args)))


@bot.command(name='fusion')
async def fusion(ctx):
    await ctx.send("Fusion Bot!")


@bot.command(name='commands')  # TODO add all commands for help
async def helpme(ctx):
    await ctx.send("Command(s) - Usage(s):")


@bot.command(name='warn')  # TODO warns sender of message replied to, or the @name
async def warn(ctx, name):
    await ctx.send(f"Warning! {name}")


@bot.command(name='list')  # TODO return requested list with optional arguments i.e. list logs @name
async def bot_list(ctx, *args):
    await ctx.send("listed {}".format(" ".join(args)))


@bot.command(name='log')  # TODO logs @name with reason and who logged
async def mod_log(ctx, name, *args):
    await ctx.send("Logged {} for {}".format(name, " ".join(args)))


if __name__ == '__main__':
    bot.run(TOKEN)
