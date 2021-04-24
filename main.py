# bot.py
import os
import discord
from dotenv import load_dotenv


prefix = "!"
mytoken = ""

load_dotenv()
TOKEN = os.getenv(mytoken)
client = discord.Client()
global debug
invites = {}
games = {}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for commands with " + prefix))



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    text = message.content.lstrip(prefix)
    if message.content.startswith(prefix):
        if str(message.guild.id) == "831797977466404915":
            args = text.split(" ")
            channel = message.channel
    ####################################### COMMANDS HERE
            if args[0] == "invite":
                if str(channel).startswith("emoji-battle-lobby"):
                    await channel.send("Hey, " + args[1])
                    await displayembed(channel, (str(message.author) + " has invited you to join a game!"), ("Type *" + prefix + "join* to join!"))
                    invites[args[1]] = message.author
                    invites[args[1] + "channel"] = channel
                else:
                    await channel.send("Sorry, you must do this in an emoji battle lobby!")
            elif args[0] == "join":
                try:
                    defaultstats = {}
                    try:
                        games[invites['<@!' + str(message.author.id) + '>' + "channel"]][message.author] = defaultstats
                    except:
                        games[invites['<@!' + str(message.author.id) + '>' + "channel"]] = {message.author: defaultstats, invites[('<@!' + str(message.author.id) + '>')]: defaultstats}
                    await channel.send("You joined the battle at " + str(invites['<@!' + str(message.author.id) + '>' + "channel"]))
                    del invites[('<@!' + str(message.author.id) + '>')]
                    del invites['<@!' + str(message.author.id) + '>' + "channel"]
                except KeyError:
                    await channel.send("You have no invite!")
            elif args[0] == "players":
                    y = ""
                    for x in games[message.channel]:
                        y = y + "<@!" + str(x.id) + ">\n"
                    await displayembed(channel, "**Players**", y)
    ########help
            elif args[0] == "help":
                helpdata = {
                    "help": {"desc": "Gets help on a command, or just a list of commands.", "syntax": "help [command]"},
                    "invite": {"desc": "Invites somebody to play a game *Emoji Battle*!", "syntax": "invite <user>"},
                    "join": {"desc": "Joins who latest invited you", "syntax": "join"},
                    "players": {"desc": "Gets the players in a match.", "syntax": "players"},
                    "debug": {"desc": "Some debug commands", "syntax": "None of yar buissness! ||It isn't because I'm to lazy to scroll down in my codespace ;)||"},
                    "mimic": {"desc": "Force the bot to send a message. Requires Manage Messages", "syntax": "mimic <message>"}
                }
                try:
                    await displayembed(channel, "**Help**", "**Description**:\n" + helpdata[args[1]]["desc"] + "\n**Syntax**:\n" + prefix + helpdata[args[1]]["syntax"])
                except:
                    helpinfo = ""
                    for x in helpdata:
                        helpinfo = helpinfo + "\n**" + str(x) + "**:\n" + prefix + helpdata[str(x)]["syntax"] + "\n" + helpdata[str(x)]["desc"]
                    await displayembed(channel, "Commands:", helpinfo)
    ########help
            elif args[0] == "mimic":
                if message.author.guild_permissions.manage_messages:
                    await message.delete()
                    await channel.send(text.lstrip("mimic"))
    ###########Debug

            elif args[0] == "debug":
                    #try:
                    if args[1] == "sender":
                        await channel.send(message.author)
                        await channel.send(message.author.id)
                    if args[1] == "call":
                        await channel.send(channel)
                    if args[1] == "var":
                        if args[2] == "set":
                            debug = args[3]
                        if args[2] == "get":
                            await channel.send(debug)
                    if args[1] == "invites":
                        await channel.send(invites)
                    if args[1] == "games":
                        await channel.send(games)
                #except:
                #    await channel.send("An error was raised.")
    ############Debug
            else:
                await channel.send("Unknown command. Try using " + prefix + "help")
        else:
            await message.channel.send("Bruh how is the bot here it isn't supposed to work here\n\nOr is it?")
    ####################################### COMMANDS HERE


#embed: Channel,Tile,Description

async def displayembed(ctx, title, desc):
    embed = discord.Embed(title=str(title), description=str(desc)) #,color=Hex code
    await ctx.send(embed=embed)


client.run(mytoken)
print(client)
