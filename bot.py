import discord
from discord.ext import commands
import check
from rps import Rps

TOKEN = 'OTEyNTA3OTE3OTUxOTYzMTQ2.YZw9OQ.WoCuEOHRVD-GlYSaRON4sm_eDns'

client = discord.Client()


games = []
games_to_remove = []
temp_inps = {}
challengers = {}


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global games, games_to_remove
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if user_message.lower()[:1] == '!':
        command = user_message[1:].split(' ')
        print(command)

        if command[0] == 'test':
            print(client.get_all_members())
            await message.channel.send(f'Success, {username}!')
            return

        if command[0] == 'rps':
            print('detected')
            game_commands = ('r', 'p', 's', 'challenge', 'accept', 'decline', 'rock', 'paper', 'scissors')

            challengers_to_delete = []
            for challenger in challengers:
                if challengers[challenger][2].elapsed() > 60:
                    challengers_to_delete.append(challenger)

            for challenger in challengers_to_delete:
                del challengers[challenger]

            if command[1] not in game_commands:
                pass

            if command[1] == 'challenge':
                if username not in challengers:
                    challengers[username] = [command[2], command[3], check.Time()]
                    await message.channel.send(f'Challenged, {command[2]}!')
                    return

                else:
                    await message.channel.send(f'Could not challenge at this time, {username}!')

            if command[1] == 'accept':
                if command[2] in challengers and challengers[command[2]][0] == username:
                    player1 = command[2]
                    player2 = username

                    mode = challengers[player1][1]
                    bo = 1
                    if mode:
                        if mode == 'bo1':
                            bo = 1
                        elif mode == 'bo3':
                            bo = 3
                        elif mode == 'bo5':
                            bo = 5

                    games.append(Rps(player1, player2, bo))
                    await message.channel.send(f"{username} accepted {command[2]}'s game")
                    return

                else:
                    await message.channel.send(f'Could not accept a game at this moment, {username}')

            if command[1] == 'decline':
                if command[2] in challengers and challengers[command[2]][0] == username:
                    del challengers[command[2]]
                    await message.channel.send(f'Declined, {command[2]}')
                    return

                else:
                    await message.channel.send(f'No game to decline, {username}, maybe it has timed out')
                    return

            if command[1] in game_commands:
                for game in games:
                    if username == game.p1 or username == game.p2:
                        if command[1] in ('rock', 'paper', 'scissors', 'r', 'p', 's'):
                            temp_inps[username] = command[1][:1]

                    if game.p1 in temp_inps and game.p2 in temp_inps:
                        output = game.rps(temp_inps[game.p1], temp_inps[game.p2])
                        del temp_inps[game.p1]
                        del temp_inps[game.p2]
                        print(output)

                        if output == 'tie':
                            await message.channel.send('Tie!')
                            return

                        elif 'Round Winner:' in output:
                            await message.channel.send(f"Round Winner: {output.replace('Round Winner: ', '')}")
                            return

                        elif 'Game Winner: ' in output:
                            games_to_remove.append(game)
                            del challengers[game.p1]
                            await message.channel.send(f"Game Winner: {output.replace('Game Winner: ', '')}")
                            return

                for game in games_to_remove:
                    games.remove(game)

    else:
        if 'https://discord' in user_message and 'https://discord.com' not in user_message: #make better, deletes scams
            message.delete()


client.run(TOKEN)
