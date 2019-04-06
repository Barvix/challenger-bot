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

#https://discordapp.com/oauth2/authorize?&client_id=428972162779578368&scope=bot&permissions=336063568

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

fb_list = [line.rstrip('\n') for line in open('list.txt')]

@bot.event
async def on_ready():
    print('Logged in as')
    print("Challenge Bot")
    print(bot.user.id)
    print('------')
    chn = bot.get_channel("560534679229431808")
    await bot.send_message(chn, "Reset complete 😄")
    mygame = "Making Music 🎹 🎼 🎧 🎤"
    await bot.change_presence(game=discord.Game(name=str(mygame)))
    
    #for server in bot.servers:
    #    print(server.id+"\n")
    #    if server.id != "446157087211520030":
    #        await bot.leave_server(server) 
    
    thedate = datetime.datetime.today()
    thedate = thedate.weekday()
    print(str(thedate))
    if (thedate is 6):
        f = open("BotSampleList.txt", 'r')
        x = f.readlines()
        f.close()
        urls = str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)])
        #await bot.say(urls)
        rhythmchannel = bot.get_channel('560556421733810187')
        await bot.send_message(rhythmchannel, urls)
    
    dayofthemonth = datetime.datetime.today()
    dayofthemonth = dayofthemonth.day
    print(str(dayofthemonth))
    if ( (dayofthemonth is 1) or (dayofthemonth is 7) or (dayofthemonth is 14) or (dayofthemonth is 21) or (dayofthemonth is 28) ):
        serv = bot.get_server("446157087211520030")

        x = serv.members

        for member in x:
            role = discord.utils.get(serv.roles, name='Feedback')
            await bot.remove_roles(member, role)
        
@bot.event
async def on_message(message):

    global fb_list
    
    if (message.author == bot.user):
        return
    
    if ("https://" in message.content and message.server.id == "446157087211520030"):
        print("Message: Read\n")
        user_join_day = message.author.joined_at.strftime("%d, %m, %y")
        message_day = datetime.datetime.now().strftime("%d, %m, %y")
        
        user_join_hour = int(message.author.joined_at.strftime("%H")) * 60 + int(message.author.joined_at.strftime("%m"))
        message_hour = int(datetime.datetime.now().strftime("%H")) * 60 + int(datetime.datetime.now().strftime("%m"))
        
        if (user_join_day == message_day):
            print("Same day delivery")
            sub_time = message_hour - user_join_hour
            if sub_time >= 60:
                print("They may now post")
            if sub_time < 60:
                if (message.channel.id == "560511832322736138"):
                    if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because your account here is still new, and to avoid leech behavior this track is being deleted. In addition, this channel is for feedbacks - which requires users to give a feedback before asking for one/posting a song. If you feel this is an error please let someone know.")
                        await bot.delete_message(message)
                        chn = bot.get_channel("560534679229431808")
                        await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
                    if "feedback" in [y.name.lower() for y in message.author.roles]:
                        print("They have feedback")
                if (message.channel.id != "560511832322736138"):
                    if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because your account here is still new. To avoid leech behavior here this track is being deleted. In the meantime, please try and engage with the community here a bit, and in up to an hour you can post your tracks. If you feel this is an error, please let someone know.")
                        await bot.delete_message(message)
                        chn = bot.get_channel("560534679229431808")
                        await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
                    if "feedback" in [y.name.lower() for y in message.author.roles]:
                        print("They have feedback")
    
    if "Timeout" in [y.name.lower() for y in message.author.roles]:
        await bot.delete_message(message)
    
    if "feedback leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because you have the role Feedback Leech, which means you've been leaching off the community or the feedback channel. If you feel this is an error, please let someone know.")
            await bot.delete_message(message)
            chn = bot.get_channel("560534679229431808")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            print("track deleted")

    if "leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content):
            await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because you have the role Feedback Leech, which means you've been leaching off the community or the feedback channel. If you feel this is an error, please let someone know.")
            await bot.delete_message(message)
            chn = bot.get_channel("560534679229431808")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            print("track deleted")
            
    if ("nigger" in message.content.lower() or "fag" in message.content.lower() or "aggot" in message.content.lower()):
        await bot.delete_message(message)
            
    mod_feedback = True
            
    if (mod_feedback is True):
        
        if ( (message.channel.id == "560511832322736138") and ("https://" in message.content or "soundcloud.com" in message.content)):
            if "🎧🎧🎧feedback giver🎧🎧🎧" not in [y.name.lower() for y in message.author.roles]:
                 if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, in order to post here you must have the feedback role, and it looks like you don't have it - which means you have never given **quality** feedback yet. If you want the feedback role, *YOU HAVE TO GIVE SOMEBODY QUALITY FEEDBACK IN THIS CHANNEL* If you think this is an error please let someone know.")
                        await bot.delete_message(message)
                        #donothin = message.channel
                 if "feedback" in [y.name.lower() for y in message.author.roles]:
                    return
            if "🎧🎧🎧feedback giver🎧🎧🎧" in [y.name.lower() for y in message.author.roles]:
                return
        
    if ("thank" in message.content.lower() and "@" in message.content.lower() and message.channel.id == "560511832322736138"):
        old,kar = message.content.split("@")
        fb,other = kar.split(">")
        fb = fb.replace("!", "")
        
        if (fb == message.author.id):
            return
        
        server = message.server
        feedbacker = server.get_member(fb)
        
        role = discord.utils.get(message.server.roles, name="Feedback")
        
        await bot.add_roles(feedbacker, role)
        
    if (message.channel.id == "560511832322736138"):
        
        old,kar = message.content.split("@")
        fb,other = kar.split(">")
        fb = fb.replace("!", "")
        
        if (fb == message.author.id):
            print("Same ID error")
            return
        
        if (fb == "428972162779578368"):
            if ("feedback" in message.content.lower()):
                rand_feedback = random.randint(0, 19)
                feedback_message = "test text"
                if (rand_feedback == 0): feedback_message = "Yo fam, this shit bangs in the whip. Like as soon as I play this in my Honda Pilot, the whip bangs bro, and not like the porn studios. I fuck with it."
                if (rand_feedback == 1): feedback_message = "Not gonna lie fam, this shit weak. The fuck is going on with that bass? Is it outta tune? Just a weak melody? A lame ass bass I banged in my whip 500000000 times? fuck outta here with this lame shit"
                if (rand_feedback == 2): feedback_message = "Ayy, this is pretty hot. Like I could just right now spread some oil on this, and fry some chicken on this song it's so hot. brb finna fry some chicken"
                if (rand_feedback == 3): feedback_message = "brrr bruh. beat's so cold i gotta wear a thicc ass hoodie man. i mean im already wearing one, but now I gotta wear another. It's a struggle man."
                if (rand_feedback == 4): feedback_message = "First of all the fuck are you doing with this EQ nonsense? You don't know - exactly. Secondly, who the fuck taught you how to compress? Some bitch on Youtube? Bitch I roast the fuck out of those little shits for a living, so don't tell me you actually know how to mix. Cus listen here bitch, you don't know shit about music. I am music, and you don't know shit about me or my story. Thank you for coming to my TED talk, bitch."
                if (rand_feedback == 5): feedback_message = "Okay, honey, stop. Just fucking stop. Are you even producing, or are you just mashing random buttons on your shitty keyboard hoping they can make you the next Metro Boomin? Cus mmmm honey listen here - nobody can be Metro Boomin. Metro Boomin is a sexy god who I worship every night - so when I say no one can be him or be like him, I know what the fuck I am talking about. So just stop."
                if (rand_feedback == 6): feedback_message = "Okay so I just played this to my friends and they melted. On the good side, I fucking hated them. On the bad side, now I have to find friends again. Wanna be my friend?"
                if (rand_feedback == 7): feedback_message = "So uh, this is pretty terrible chief. So terrible I am going to steal this and sell it to some high-up artist and take all the credit for it. Skrrt"
                if (rand_feedback == 8): feedback_message = "Listened to this shit while meditating around my stacks of cash and my diamonds. Very good for the mood, I felt like Future."
                if (rand_feedback == 9): feedback_message = "I played this to a good friend of mine, Mr. Travis Scottington, you wouldn't know him. He liked it so much he kept saying something about something being straight up? I think he might have a weird fascination with his dick. Tbf, so do I."
                if (rand_feedback == 10): feedback_message = "I came back from a hot tub in the back of my F150 with my hot cousins to listen to this? Chief if you tag me again, I will have Mr. Boomin officially not trust you."
                if (rand_feedback == 11): feedback_message = "I played this to Drake, and he likes the beat because of how young it is."
                if (rand_feedback == 12): feedback_message = "Yo i spit out my Arizona tea as soon as that bass dropped man. Kinda came a little, too. Now that last part might have to do with the hentai I was watching, but I don't think so because I don't even like hentai."
                if (rand_feedback == 13): feedback_message = "Can i have sex with this beat? Cus this beat, especially the low ends of it man, are fine as hellllllll"
                if (rand_feedback == 14): feedback_message = "This mix would be balanced if my monitors only had tweeters"
                if (rand_feedback == 15): feedback_message = "This one could use some Waves Abbey Road Ultra de-distorter V4 to remove some overtones"
                if (rand_feedback == 16): feedback_message = "Real music is made with physical instruments and that is a fact. Dont @ me."
                if (rand_feedback == 17): feedback_message = "Yoo bro this one is sicko mode! It bumps in my grandmas Camry 03 :ok_hand: "
                if (rand_feedback == 18): feedback_message = "Sounds good Can i post mine now??"
                if (rand_feedback == 19): feedback_message = "There's something off about this but idk anyway check mine out!"
                chn = bot.get_channel("560511832322736138")
                await bot.send_message(chn, feedback_message)
        
        print("It knows the message exists")
        
        if any(fbr in message.content.lower() for fbr in fb_list):
            print("it knows the role should be added")
            role = discord.utils.get(message.server.roles, name="Feedback")
        
            await bot.add_roles(message.author, role)
    #print(url_string)
           
    await bot.process_commands(message)

client = discord.Client()
my_server = client.get_server('server id')
    
@bot.event
async def on_member_join(member):
    server = member.server.id
    #print(str(server))
    if (server == "446157087211520030"):
        message = 'Welcome {} to HipHop Creation Central! Please be sure to read the #rules! If you need help using me head to #bot-commands and type !help'.format(member.mention)
        chn = bot.get_channel("560542321490264076")
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
    embed.add_field(name="singer ", value="        Gives you the Singer role", inline=False)
    embed.add_field(name="artist ", value="        Gives you the Singer role", inline=False)
    embed.add_field(name="daw <daw name>", value="        Gives you a role for a specified daw. <fl studio> <ableton> <reason> <pro tools> <logic>", inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)

@bot.command(pass_context = True)
async def reset_feedback(ctx):
    serv = bot.get_server(ctx.message.server)
    
    y = serv.members
    
    for member in y:
        role = discord.utils.get(serv.roles, name='Feedback')
        await bot.remove_roles(member, role)
    
@bot.command(pass_context = True)
async def heroku(ctx):
    await bot.say("We on live 24/7 now :D")
  
@bot.command(pass_context = True)
async def vox23(ctx):
    await bot.say("https://cdn.discordapp.com/attachments/446169554197151744/548588579329146890/VOX_23.wav");

@bot.command(pass_context = True)
async def sample(ctx):
    
    f = open("BotSampleList.txt", 'r')
    x = f.readlines()
    f.close()
    urls = str(x[random.randrange(0, len(x)-1)])
    await bot.say(urls)

@bot.command(pass_context = True)
async def roulette(ctx):
    
    f = open("BotSampleList.txt", 'r')
    x = f.readlines()
    f.close()
    urls = str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)])
    await bot.say(urls)

@bot.command(pass_context = True)
async def yeet(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="Extremely politically correct")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def twitch(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="TwitchFeedback")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def edgy(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="Extremely politically correct")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def producer(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎹🎹🎹Producer🎹🎹🎹")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def freestyler(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="FREESTYLER")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def engineer(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎧🎧🎧Engineer🎧🎧🎧")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
  
@bot.command(pass_context = True)
async def feedback(ctx):
    #role = discord.utils.get(ctx.message.server.roles, name="🎧🎧🎧Engineer🎧🎧🎧")
    #await bot.add_roles(ctx.message.author, role)
    await bot.say("I probably just said you need to give somebody feedback in the feedback channel to get this role. It is not difficult to give somebody feedback. c'mon. don't be that guy.")

@bot.command(pass_context = True)
async def singer(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎤🎤🎤Singer🎤🎤🎤")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def artist(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎤🎤🎤Singer🎤🎤🎤")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def daw(ctx, *, dawname : str):
    role = discord.utils.get(ctx.message.server.roles, name="NONE") 
    if (dawname.lower() == "fl studio"):
        role = discord.utils.get(ctx.message.server.roles, name="FL STUDIO")
    if (dawname.lower() == "ableton"):
        role = discord.utils.get(ctx.message.server.roles, name="ABLETON")
    if (dawname.lower() == "reason"):
        role = discord.utils.get(ctx.message.server.roles, name="REASON")
    if (dawname.lower() == "pro tools"):
        role = discord.utils.get(ctx.message.server.roles, name="PRO TOOLS")
    if (dawname.lower() == "reaper"):
        role = discord.utils.get(ctx.message.server.roles, name="REAPER")
    if (dawname.lower() == "lmms"):
        role = discord.utils.get(ctx.message.server.roles, name="LMMS")
    if (dawname.lower() == "garage band" or dawname.lower() == "garageband"):
        role = discord.utils.get(ctx.message.server.roles, name="GARAGE BAND")
    if (dawname.lower() == "logic pro x" or dawname.lower() == "logic pro" or dawname.lower() == "logic"):
        role = discord.utils.get(ctx.message.server.roles, name="LOGIC PRO X")
    if (role is not discord.utils.get(ctx.message.server.roles, name="NONE")):
        await bot.add_roles(ctx.message.author, role)
        await bot.say("Role successfully added!")
    if (role is discord.utils.get(ctx.message.server.roles, name="NONE")):
        #await bot.add_roles(ctx.message.author, role)
        await bot.say("Role not found :(")

@bot.command(pass_context = True)
async def rapper(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎤🎤🎤Rapper🎤🎤🎤")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def lotto(ctx):
    if "lotto ban" in [y.name.lower() for y in ctx.message.author.roles]:
        await bot.say("Whoa buddy, it appears as if you have been banned from the lotto. If you have any questions about this please talk to a mod.")
    if "lotto ban" not in [y.name.lower() for y in ctx.message.author.roles]:
        role = discord.utils.get(ctx.message.server.roles, name="Lotto")
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
