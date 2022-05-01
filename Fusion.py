import discord
import json
from datetime import datetime as dt
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role, has_any_role

with open("token.txt", "r") as f:
    TOKEN = f.read()
bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())
guild_ids = []
servers = {"916372812460068915":
               {"welcome_channel": 916372812460068918}  # set to False if no channel
           }


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


@bot.event
async def on_member_join(member):
    welcome_channel = await bot.fetch_channel(servers[str(member.guild.id)]["welcome_channel"])
    if welcome_channel:
        await welcome_channel.send(f'Welcome in <@{member.id}>, \n'
                                   'https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@bot.command(name='name')
async def name(ctx):
    await ctx.send(f"your name is {ctx.author}")


@bot.command(name='bp')
async def bp(ctx):
    await ctx.send("Someone may not want to share their blueprint because once it gets out, other people may start"
                   " taking credit for the hard work that was put into making it, which is pretty sucky.")


@bot.command(name='say')
@has_any_role("Fusion Space Member")
async def bot_list(ctx, *args):
    if not args:
        await ctx.send("You have to tell me what to say!")
        return

    args = "{}".format(" ".join(args))

    if '<@' in args:
        args = args.split(' ')
        for arg in args:
            if arg[:2] == '<@' and arg[-1:] == '>':
                idx = args.index(arg)
                arg = arg.replace('<@', '')
                arg = arg.replace('>', '')
                if arg.isdigit():
                    user = bot.get_user(int(arg))
                    args[idx] = f'{user.name}#{user.discriminator}'
        args = "{}".format(" ".join(args))

    if args[-2:] == '/s':
        args = list(args)
        lu = -1
        for idx in range(len(args[:-2])):
            if args[idx] == ' ':
                continue
            if lu == -1:
                args[idx] = args[idx].lower()
            if lu == 1:
                args[idx] = args[idx].upper()
            lu *= -1
        args = ''.join(args[:-2])

    await ctx.send(args)


@bot.command(name='fusion')
async def fusion(ctx):
    await ctx.send("Fusion Bot!")


@bot.command(name='warn')  # TODO warns sender of message replied to, or the @name
@has_any_role("Fusion Space Member", "Moderation")
async def warn(ctx, name, *args):
    await ctx.send(f"Warning! {name} "+"{}".format(" ".join(args)))


@bot.command(name='logs')
@has_any_role("Fusion Space Member", "Moderation")
async def mod_logs(ctx, uid, *args):
    if (not uid or '<@' not in uid) and ('#' not in uid) and not uid.isdigit():
        await ctx.send("Must provide valid name!")
        return

    with open("mod_logs.json", "r") as f:
        all_logs = json.loads(f.read())

    if '#' in uid:
        guild = bot.get_guild(ctx.guild.id)
        user = discord.utils.get(guild.members, name=uid.split('#')[0], discriminator=uid.split('#')[1])
        if user is None:
            await ctx.send("User not found")
            return
        uid = user.id

    elif uid.isdigit():
        if not await bot.fetch_user(int(uid)):
            await ctx.send("User not found")
            return

    else:
        for i in ('<', '>', '@'):
            uid = uid.replace(i, '')

    if str(ctx.guild.id) not in all_logs:
        await ctx.send("No logs found for this server")
        return
    else:
        logs = all_logs[str(ctx.guild.id)]

    if str(uid) not in logs:
        await ctx.send(f"No logs found for {bot.get_user(uid)}")
        return

    message = ''
    for log in logs[str(uid)]:
        message += f'{int(log)} - {dt.fromtimestamp(logs[str(uid)][log]["timestamp"]).strftime("%Y/%m/%d at %H:%M:%S")} UTC\n'  # log number and time
        message += f'Username at time: {logs[str(uid)][log]["user_name_at_time"]}\n'  # name of user logged
        if bot.get_user(logs[str(uid)][log]["mod_id"]).name == logs[str(uid)][log]["mod_name"]:
            message += f'Logged by {bot.get_user(logs[str(uid)][log]["mod_id"])}\n'  # name of person that logged
        else:
            message += f'Logged by {bot.get_user(logs[str(uid)][log]["mod_id"])} ({logs[str(uid)][log]["mod_name"]})\n'  # name of person that logged + name at time
        message += f'Reason: {logs[str(uid)][log]["reason"]}\n'  # reason for log
        message += '\n'

    await ctx.send(message)
    return


@bot.command(name='log')
@has_any_role("Fusion Space Member", "Moderation")
async def mod_log(ctx, uid, *args):
    if (not uid or '<@' not in uid) and ('#' not in uid) and not uid.isdigit():
        await ctx.send("Must provide valid name")
        return

    if not args:
        await ctx.send("Must provide a reason!")
        return

    if '#' in uid:
        guild = bot.get_guild(ctx.guild.id)
        user = discord.utils.get(guild.members, name=uid.split('#')[0], discriminator=uid.split('#')[1])
        if user is None:
            await ctx.send("User not found")
            return
        uid = user.id

    elif uid.isdigit():
        if not await bot.fetch_user(int(uid)):
            await ctx.send("User not found")
            return

    else:
        for i in ('<', '>', '@'):
            uid = uid.replace(i, '')

    with open("mod_logs.json", "r") as f:
        logs = json.loads(f.read())

    if str(ctx.guild.id) not in logs:
        logs[str(ctx.guild.id)] = {}

    if str(uid) not in logs[str(ctx.guild.id)]:
        logs[str(ctx.guild.id)][str(uid)] = {}

    user_name = await bot.fetch_user(uid)
    times_logged = len(logs[str(ctx.guild.id)][str(uid)])
    logs[str(ctx.guild.id)][str(uid)][times_logged + 1] = {"timestamp": dt.timestamp(dt.now()),
                                                           "reason": " ".join(args),
                                                           "user_name_at_time": user_name.name,
                                                           "mod_id": ctx.author.id,
                                                           "mod_name": ctx.author.name}

    with open("mod_logs.json", "w") as f:
        f.write(json.dumps(logs, indent=4))

    await ctx.send("Logged {} for {}".format(await bot.fetch_user(uid), " ".join(args)))


if __name__ == '__main__':
    bot.run(TOKEN)
