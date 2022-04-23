import discord
import json
from datetime import datetime as dt
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


@bot.command(name='name')
async def name(ctx):
    await ctx.send(f"your name is {ctx.author}")


@bot.command(name='say')
async def bot_list(ctx, *args):
    if not args:
        await ctx.send("You have to tell me what to say!")
        return
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
async def mod_log(ctx, uid: str, *args):
    if not uid or '<@' not in uid:
        await ctx.send("Must provide name, @user")
        return

    if not args:
        await ctx.send("Must provide a reason!")
        return

    with open("mod_logs.json", "r") as f:
        logs = json.loads(f.read())

    for i in ('<', '>', '@'):
        uid = uid.replace(i, '')
    if uid not in logs:
        logs[uid] = {}

    user_name = await bot.fetch_user(uid)
    times_logged = len(logs[uid])
    logs[uid][times_logged + 1] = {"timestamp": dt.timestamp(dt.now()),
                                   "reason": " ".join(args),
                                   "user_name_at_time": user_name.name,
                                   "mod_id": ctx.author.id,
                                   "mod_name": ctx.author.name}

    with open("mod_logs.json", "w") as f:
        f.write(json.dumps(logs, indent=4))

    await ctx.send("Logged {} for {}".format(await bot.fetch_user(uid), " ".join(args)))


if __name__ == '__main__':
    bot.run(TOKEN)
