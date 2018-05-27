import discord
from discord.ext import commands
import os.path
import os
import datetime
import random
#import dateutil
from dateutil.relativedelta import relativedelta
import datetime

#https://discordapp.com/oauth2/authorize?&client_id=428972162779578368&scope=bot&

description = '''Hi, I'm the Challenger!'''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print("Challenge Bot")
    print(bot.user.id)
    print('------')
    chn = bot.get_channel("376573686968221701")
    await bot.send_message(chn, "Reset complete 😄")
    mygame = "Making Music 🎹 🎼 🎧 🎤"
    await bot.change_presence(game=discord.Game(name=str(mygame)))

@bot.event
async def on_message(message):

    if (message.author == bot.user):
        return
    
    if "feedback leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.delete_message(message)
            print("track deleted")

    if "leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.delete_message(message)
            print("track deleted")
           
    await bot.process_commands(message)

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title="help", description="        This Command helps with commands for me", color=0x7abae8)
    embed.add_field(name="timer <month_number> <day_in_month>", value="        Sets a timer for the challenge", inline=False)
    embed.add_field(name="timeleft ", value="        Shows you how many days are left in a challenge", inline=False)
    embed.add_field(name="enter <link to song>", value="        Enters your song for a challenge", inline=False)
    embed.add_field(name="voting ", value="        Starts the voting of a challenge", inline=False)
    embed.add_field(name="reset_votes ", value="        Resets the votes to be blank for the next challenge", inline=False)
    embed.add_field(name="producer ", value="        Gives you the Producer role", inline=False)
    embed.add_field(name="rapper ", value="        Gives you the Rapper role", inline=False)
    embed.add_field(name="daw <daw name>", value="        Gives you a role for a specified daw. <fl studio> <ableton> <reason> <pro tools> <logic>", inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context = True)
async def heroku(ctx):
    await bot.say("We on live 24/7 now :D")
    
@bot.command(pass_context = True)
async def producer(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎹🎹🎹Producer🎹🎹🎹")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def daw(ctx, *, dawname : str):
    role = discord.utils.get(ctx.message.server.roles, name="FL STUDIO") 
    if (dawname.lower() == "fl studio"):
        role = discord.utils.get(ctx.message.server.roles, name="FL STUDIO")
    if (dawname.lower() == "ableton"):
        role = discord.utils.get(ctx.message.server.roles, name="ABLETON")
    if (dawname.lower() == "reason"):
        role = discord.utils.get(ctx.message.server.roles, name="REASON")
    if (dawname.lower() == "pro tools"):
        role = discord.utils.get(ctx.message.server.roles, name="PRO TOOLS")
    if (dawname.lower() == "logic pro x" or dawname.lower() == "logic pro" or dawname.lower() == "logic"):
        role = discord.utils.get(ctx.message.server.roles, name="LOGIC PRO X")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def rapper(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎤🎤🎤Rapper🎤🎤🎤")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def timer(ctx, month : str, date : str):
    challenge_name = "UNDEF"
    if (ctx.message.channel.name == "the-lofi-flip"):
        challenge_name = "LFF"
    if (ctx.message.channel.name == "game-of-hip-hop"):
        challenge_name = "ghh"  
    if (ctx.message.channel.name == "one-kit-contest"):
        challenge_name = "OKC"    
    if (ctx.message.channel.name == "flip-this-challenge"):
        challenge_name = "ftc"   
    if (ctx.message.channel.name == "roulette"):
        challenge_name = "MHHR"   
    if (ctx.message.channel.name == "the-score"):
        challenge_name = "thescore"   
    if (ctx.message.channel.name == "showdown"):
        challenge_name = "showdown"   
    if (ctx.message.channel.name == "the-copy-cat"):
        challenge_name = "tcc"   
    if (ctx.message.channel.name == "remix-challenge"):
        challenge_name = "rc"   
    if (ctx.message.channel.name == "whos-your-master"):
        challenge_name = "wym"   

    if ("++" in [y.name.lower() for y in ctx.message.author.roles]) or ("+" in [y.name.lower() for y in ctx.message.author.roles]) or ("winners" in [y.name.lower() for y in ctx.message.author.roles]) or (ctx.message.author.id == "409223599757590538"):
        challenge_file = challenge_name + ".txt"
        c_file = open(challenge_file, "w+")
        c_file.write(month + "." + date)
        c_file.close()
        await bot.say(challenge_name + " set for " + month + "/" + date + ".")
        return
    await bot.say("You don't have permission to use this command. If you think this is an error please let someone know.")

@bot.command(pass_context = True)
async def timeleft(ctx):

    challenge_name = "UNDEF"
    if (ctx.message.channel.name == "the-lofi-flip"):
        challenge_name = "LFF"
    if (ctx.message.channel.name == "game-of-hip-hop"):
        challenge_name = "ghh"  
    if (ctx.message.channel.name == "one-kit-contest"):
        challenge_name = "OKC"    
    if (ctx.message.channel.name == "flip-this-challenge"):
        challenge_name = "ftc"   
    if (ctx.message.channel.name == "roulette"):
        challenge_name = "MHHR"   
    if (ctx.message.channel.name == "the-score"):
        challenge_name = "thescore"   
    if (ctx.message.channel.name == "showdown"):
        challenge_name = "showdown"   
    if (ctx.message.channel.name == "the-copy-cat"):
        challenge_name = "tcc"   
    if (ctx.message.channel.name == "remix-challenge"):
        challenge_name = "rc"   
    if (ctx.message.channel.name == "whos-your-master"):
        challenge_name = "wym"   
    
    challenge_file = challenge_name + ".txt"
    if (os.path.exists(challenge_file)):
        c_file = open(challenge_file, "r")
        date = c_file.readline()
        month, day = date.split(".")
        td = datetime.datetime(2018, int(month), int(day)) - datetime.datetime.now()
        date_to = int(td.days) + 1
        if (date_to != 1):
            await bot.say("You have " + str(date_to) + " days to complete " + challenge_name + ".")
        if (date_to == 1):
            await bot.say("You have " + str(date_to) + " day to complete " + challenge_name + ".")
    if (not os.path.exists(challenge_file)):
        await bot.say("I'm sorry, it appears this challenge hasn't been added to my timer.")

@bot.command(pass_context = True)
async def reset(ctx):
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):

        #await bot.delete_message(ctx.message)
        await bot.say("Resetting :D")
        exit()
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

@bot.command(pass_context = True)
async def enter(ctx, link : str):

    challenge_name = "UNDEF"
    if (ctx.message.channel.name == "the-lofi-flip"):
        challenge_name = "LFF"
    if (ctx.message.channel.name == "game-of-hip-hop"):
        challenge_name = "ghh"  
    if (ctx.message.channel.name == "one-kit-contest"):
        challenge_name = "OKC"    
    if (ctx.message.channel.name == "flip-this-challenge"):
        challenge_name = "ftc"   
    if (ctx.message.channel.name == "roulette"):
        challenge_name = "MHHR"   
    if (ctx.message.channel.name == "the-score"):
        challenge_name = "thescore"   
    if (ctx.message.channel.name == "showdown"):
        challenge_name = "showdown"   
    if (ctx.message.channel.name == "the-copy-cat"):
        challenge_name = "tcc"   
    if (ctx.message.channel.name == "remix-challenge"):
        challenge_name = "rc"   
    if (ctx.message.channel.name == "whos-your-master"):
        challenge_name = "wym"   

    challenge_file = "entries_"+challenge_name+".txt"

    name = str(ctx.message.author.nick)

    if (name=="None"):
        name = '{0.name}'.format(ctx.message.author)

    if (os.path.exists(challenge_file)):
        c_file = open(challenge_file, "a")
        c_file.write(""+name + " --- " + "<" + link + ">\n")
        c_file.close()
        await bot.say("Entry added!")
    if (not os.path.exists(challenge_file)):
        c_file = open(challenge_file, "w+")
        c_file.write(name + " --- " + link)
        c_file.close()
        await bot.say("Entry added!")

@bot.command(pass_context = True)
async def reset_votes(ctx):

    challenge_name = "UNDEF"
    if (ctx.message.channel.name == "the-lofi-flip"):
        challenge_name = "LFF"
    if (ctx.message.channel.name == "game-of-hip-hop"):
        challenge_name = "ghh"  
    if (ctx.message.channel.name == "one-kit-contest"):
        challenge_name = "OKC"    
    if (ctx.message.channel.name == "flip-this-challenge"):
        challenge_name = "ftc"   
    if (ctx.message.channel.name == "roulette"):
        challenge_name = "MHHR"   
    if (ctx.message.channel.name == "the-score"):
        challenge_name = "thescore"   
    if (ctx.message.channel.name == "showdown"):
        challenge_name = "showdown"   
    if (ctx.message.channel.name == "the-copy-cat"):
        challenge_name = "tcc"   
    if (ctx.message.channel.name == "remix-challenge"):
        challenge_name = "rc"   
    if (ctx.message.channel.name == "whos-your-master"):
        challenge_name = "wym"   

    if ("++" in [y.name.lower() for y in ctx.message.author.roles]) or ("+" in [y.name.lower() for y in ctx.message.author.roles]) or ("winners" in [y.name.lower() for y in ctx.message.author.roles]) or (ctx.message.author.id == "409223599757590538"):
        challenge_file = "entries_"+challenge_name+".txt"
        c_file = open(challenge_file, "w+")
        c_file.close()
        await bot.say("Votes reset!")
        return
    await bot.say("You don't have permission to use this command. If you think this is an error please let someone know.")

@bot.command(pass_context = True)
async def voting(ctx):

    challenge_name = "UNDEF"
    if (ctx.message.channel.name == "the-lofi-flip"):
        challenge_name = "LFF"
    if (ctx.message.channel.name == "game-of-hip-hop"):
        challenge_name = "ghh"  
    if (ctx.message.channel.name == "one-kit-contest"):
        challenge_name = "OKC"    
    if (ctx.message.channel.name == "flip-this-challenge"):
        challenge_name = "ftc"   
    if (ctx.message.channel.name == "roulette"):
        challenge_name = "MHHR"   
    if (ctx.message.channel.name == "the-score"):
        challenge_name = "thescore"   
    if (ctx.message.channel.name == "showdown"):
        challenge_name = "showdown"   
    if (ctx.message.channel.name == "the-copy-cat"):
        challenge_name = "tcc"   
    if (ctx.message.channel.name == "remix-challenge"):
        challenge_name = "rc"   
    if (ctx.message.channel.name == "whos-your-master"):
        challenge_name = "wym"   

    challenge_file = "entries_"+challenge_name+".txt"
    if (os.path.exists(challenge_file)):
        await bot.say("@everyone Come on out and vote for this challenge's entries!\nPlease vote with <:upvote:423630753272823818> for the entry you wish to vote for, and please do not vote for yourself. If you entered in the challenge you must vote.")
        c_file = open(challenge_file, "r")
        with open(challenge_file) as cf:  
            for cnt, line in enumerate(cf):
                #print("Line {}: {}".format(cnt, line))
                name, entry = line.split(" --- ")
                #entry = "<"+entry+">"
                await bot.say("Entry " + str(cnt+1) + " by " + name + "\n" + entry)
        c_file.close()
    if (not os.path.exists(challenge_file)):
        await bot.say("I'm sorry, this challenge doesn't appear to have been found.")

@bot.command(pass_context = True)
async def sayinchannel(ctx, roomid: str, *, msg_str: str):

    chn = bot.get_channel(roomid)
    
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):

        #await bot.delete_message(ctx.message)
        await bot.send_message(chn, msg_str)
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

#@bot.command()
#async def playing(*, mygame : str):
#    await bot.change_presence(game=discord.Game(name=str(mygame)))
        
bot.run(os.environ['BOT_TOKEN'])
