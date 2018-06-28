import discord
from discord.ext import commands
import os.path
import os
import datetime
import random
#import dateutil
from dateutil.relativedelta import relativedelta
import datetime
import boto3
import botocore

#https://discordapp.com/oauth2/authorize?&client_id=428972162779578368&scope=bot&

description = '''Hi, I'm the Challenger!'''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')

session = boto3.Session(
    #aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
    #aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
)

s3 = boto3.client('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )

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
    
    thedate = datetime.datetime.today()
    thedate = thedate.weekday()
    print(str(thedate))
    if (thedate is 3):
        f = open("BotSampleList.txt", 'r')
        x = f.readlines()
        f.close()
        urls = str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)])
        #await bot.say(urls)
        await bot.send_message(chn, urls)
    
    serv = bot.get_server("446157087211520030")
    
    x = serv.members
    
    for member in x:
        role = discord.utils.get(serv.roles, name='Feedback')
        await bot.remove_roles(member, role)

@bot.event
async def on_message(message):

    if (message.author == bot.user):
        return
    
    if "feedback leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.delete_message(message)
            chn = bot.get_channel("376573686968221701")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            print("track deleted")

    if "leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.delete_message(message)
            chn = bot.get_channel("376573686968221701")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            print("track deleted")
            
    if ("nigger" in message.content.lower() or "fag" in message.content.lower() or "queer" in message.content.lower()):
        await bot.delete_message(message)
            
    mod_feedback = False
            
    if (mod_feedback is True):
        
        if (message.channel.id == "446168661607186434" and ("https://" in message.content or "soundcloud.com" in message.content)):
            if "🎧🎧🎧feedback giver🎧🎧🎧" not in [y.name.lower() for y in message.author.roles]:
                 if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now, you must first give feedback before asking for some. If you think you got this message in error, please contact a mod or admin.")
                        await bot.delete_message(message)
                 if "feedback" in [y.name.lower() for y in message.author.roles]:
                    return
            if "🎧🎧🎧feedback giver🎧🎧🎧" in [y.name.lower() for y in message.author.roles]:
                return
        
    if ("thank" in message.content.lower() and "@" in message.content.lower()):
        old,kar = message.content.split("@")
        fb,other = kar.split(">")
        fb = fb.replace("!", "")
        
        if (fb == message.author.id):
            return
        
        server = message.server
        feedbacker = server.get_member(fb)
        
        role = discord.utils.get(message.server.roles, name="Feedback")
        
        await bot.add_roles(feedbacker, role)
           
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    server = member.server.id
    #print(str(server))
    if (server == "446157087211520030"):
        message = 'Welcome {} to HipHop Challenges Central! Please be sure to read the #rules! If you need help using me head to #bot-commands and type !help'.format(member.mention)
        chn = bot.get_channel("446171284142030858")
        await bot.send_message(chn, message)
    
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
async def roulette(ctx):
    f = open("BotSampleList.txt", 'r')
    x = f.readlines()
    f.close()
    urls = str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)])
    await bot.say(urls)

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
    challenge_name = ctx.message.channel.id

    global s3
    
    cname = ctx.message.channel.name
    cname = cname.replace('-',' ')
    
    if ("++" in [y.name.lower() for y in ctx.message.author.roles]) or ("+" in [y.name.lower() for y in ctx.message.author.roles]) or ("winners" in [y.name.lower() for y in ctx.message.author.roles]) or (ctx.message.author.id == "409223599757590538") or ("admin" in [y.name.lower() for y in ctx.message.author.roles]) or ("mod" in [y.name.lower() for y in ctx.message.author.roles]) or ("👑👑👑Challenge Winner👑👑👑" in [y.name.lower() for y in ctx.message.author.roles]):
        challenge_file = challenge_name + ".txt"
        filename = challenge_name+".txt"
        
        f = open(filename,"w+")
        f.write(month + "." + date)
        f.close()
        
        bucket_name = 'cloud-cube'

        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        s3.upload_file(filename, bucket_name, "cvxsngshjp1h/"+filename)

        await bot.say(cname + " set for " + month + "/" + date + ".")
        return
    await bot.say("You don't have permission to use this command. If you think this is an error please let someone know.")

@bot.command(pass_context = True)
async def timeleft(ctx):

    challenge_name = ctx.message.channel.id  
    
    global s3
    
    cname = ctx.message.channel.name
    cname = cname.replace('-',' ')
    
    challenge_file = challenge_name + ".txt"
    
    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    KEY = "cvxsngshjp1h/"+challenge_file # replace with your object key

    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )

    try:
        xs3.Bucket(BUCKET_NAME).download_file(KEY, challenge_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
            await bot.say("I'm sorry, it appears this challenge hasn't been added to my timer.")
            return
        else:
            raise
    f = open(challenge_file, "r")
    date = f.readline()
    month, day = date.split(".")
    td = datetime.datetime(2018, int(month), int(day)) - datetime.datetime.now()
    date_to = int(td.days) + 1
    if (date_to != 1):
        await bot.say("You have " + str(date_to) + " days to complete " + cname + ".")
    if (date_to == 1):
        await bot.say("You have " + str(date_to) + " day to complete " + cname + ".")

@bot.command(pass_context = True)
async def reset(ctx):
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):
        await bot.say("Resetting :D")
        exit()
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

@bot.command(pass_context = True)
async def enter(ctx, link : str):

    challenge_name = ctx.message.channel.id 
    cname = ctx.message.channel.name
    cname = cname.replace('-',' ')
    
    global s3

    challenge_file = "entries_"+challenge_name+".txt"
    
    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    KEY = "cvxsngshjp1h/"+challenge_file # replace with your object key

    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )
    
    name = str(ctx.message.author.nick)

    if (name=="None"):
        name = '{0.name}'.format(ctx.message.author)

    try:
        xs3.Bucket(BUCKET_NAME).download_file(KEY, challenge_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            
            c_file = open(challenge_file, "w+")
            c_file.write(""+name + " --- " + "<" + link + ">\n")
            c_file.close()
            s3.upload_file(challenge_file, BUCKET_NAME, "cvxsngshjp1h/"+challenge_file)
            await bot.say("Entry added!")
            
            return
        else:
            raise

    c_file = open(challenge_file, "a")
    c_file.write(""+name + " --- " + "<" + link + ">\n")
    c_file.close()
    s3.upload_file(challenge_file, BUCKET_NAME, "cvxsngshjp1h/"+challenge_file)
    await bot.say("Entry added!")

@bot.command(pass_context = True)
async def reset_votes(ctx):

    challenge_name = ctx.message.channel.id

    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    
    global s3
    
    cname = ctx.message.channel.name
    cname = cname.replace('-',' ')
    
    if ("++" in [y.name.lower() for y in ctx.message.author.roles]) or ("+" in [y.name.lower() for y in ctx.message.author.roles]) or ("winners" in [y.name.lower() for y in ctx.message.author.roles]) or (ctx.message.author.id == "409223599757590538") or ("admin" in [y.name.lower() for y in ctx.message.author.roles]) or ("mod" in [y.name.lower() for y in ctx.message.author.roles]) or ("👑👑👑Challenge Winner👑👑👑" in [y.name.lower() for y in ctx.message.author.roles]):
        challenge_file = "entries_"+challenge_name+".txt"
        c_file = open(challenge_file, "w+")
        c_file.close()
        s3.upload_file(challenge_file, BUCKET_NAME, "cvxsngshjp1h/"+challenge_file)
        await bot.say("Votes reset!")
        return
    await bot.say("You don't have permission to use this command. If you think this is an error please let someone know.")

@bot.command(pass_context = True)
async def voting(ctx):

    challenge_name = ctx.message.channel.id
    
    challenge_file = "entries_"+challenge_name+".txt"
    
    cname = ctx.message.channel.name
    cname = cname.replace('-',' ')

    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    KEY = "cvxsngshjp1h/"+challenge_file # replace with your object key

    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )
    
    try:
        xs3.Bucket(BUCKET_NAME).download_file(KEY, challenge_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            await bot.say("I'm sorry, this challenge doesn't appear to have been found.")
            return
        else:
            raise
    
    await bot.say("@everyone Come on out and vote for " + cname+"'s entries!\nPlease vote with <:upvote:423630753272823818> for the entry you wish to vote for, and please do not vote for yourself. If you entered in the challenge you must vote.")
    c_file = open(challenge_file, "r")
    with open(challenge_file) as cf:  
        for cnt, line in enumerate(cf):
            print("Line {}: {}".format(cnt, line))
            name, entry = line.split(" --- ")
            #entry = "<"+entry+">"
            await bot.say("Entry " + str(cnt+1) + " by " + name + "\n" + entry)
    c_file.close()

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
