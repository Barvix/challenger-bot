import discord
from discord.ext import commands
from discord.utils import get
import os.path
import os
import datetime
import random
from dateutil.relativedelta import relativedelta
import datetime
import boto3
import botocore
import logging

#https://discordapp.com/oauth2/authorize?&client_id=428972162779578368&scope=bot&permissions=336063568

logging.basicConfig(level=logging.INFO)

description = '''Hi, I'm the Challenger!'''
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command('help')

session = boto3.Session(
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
)

s3 = boto3.client('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )

with open("list.txt") as f:
    fb_list=[]
    fb_points=[]
    for line in f:
        l,p = line.split(",")
        np = int(p)
        fb_list.append(l)
        fb_points.append(np)
#
def downloadfile(amount):
    global s3
    
    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )
    
    filename = "karma.txt"
    member = "428972162779578368"
    
    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    ky = os.environ['CLOUDCUBE_KEY']
    KEY = ky + "/" + filename # replace with your object key
    
    try:
        xs3.Bucket(BUCKET_NAME).download_file(KEY, filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":

            giv_file = open(filename, "w+")
            giv_file.write(member+","+str(amount)+"\n")
            giv_file.close()
            print("At the 404, almost upload")
            s3.upload_file(filename, BUCKET_NAME, ky + "/" +filename)
            return amount

        else:
            raise
        
def karmamod(member, amount, mod):
    amount = int(amount)
    
    karma = 0
    
    downloadfile(amount)
    
    global s3
    
    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )
    
    filename = "karma.txt"
    
    BUCKET_NAME = 'cloud-cube' # replace with your bucket name
    ky = os.environ['CLOUDCUBE_KEY']
    KEY = ky + "/" + filename # replace with your object key

    if os.path.exists('karma.txt'):
        if member in open('karma.txt').read():
            mlist = [line.rstrip('\n') for line in open("karma.txt")]

            for idx in range(len(mlist)):
                ln = mlist[idx]
                ln = mlist[idx]
                if ln.startswith(member):
                    pts = ln
                    uid, pt = pts.split(',')
                    intpt = int(pt.strip())
                    #intpt -= feedback_barrier
                    if (mod == "sub"):
                        intpt -= amount
                    if (mod == "add"):
                        intpt += amount
                    if (mod == "set"):
                        intpt = amount
                    karma = intpt
            
                    swrite = member + "," + str(intpt)
                    mlist[idx] = swrite
            
            fl = open("karma.txt", 'w')
            
            for ln in mlist:
                fl.write(ln+"\n")
            fl.close()
            s3.upload_file(filename, BUCKET_NAME, ky + "/" + filename)
            
            return karma

        else:
            fi = open(filename, "a")
            fi.write("\n"+member + ","+str(amount))
            fi.close()
            s3.upload_file(filename, BUCKET_NAME, KEY)
            
            return amount

@bot.event
async def on_ready():
    global s3
    print('Logged in as')
    print("Challenge Bot")
    print(bot.user.id)
    print('------')
    chn = bot.get_channel("560534679229431808")
    await bot.send_message(chn, "Reset complete 😄")
    mygame = "Making Music 🎹 🎼 🎧 🎤"
    await bot.change_presence(game=discord.Game(name=str(mygame)))
    
    xs3 = boto3.resource('s3', 
    aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'],
    region_name='us-west-1'
    )
    
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
            #await bot.remove_roles(member, role)
        
@bot.event
async def on_message(message):

    global fb_list
    global fb_points
    
    if (message.author == bot.user):
        return
    
    if (message.server.id == "446157087211520030"):
        if ("crack" in message.content.lower() or "pirate" in message.content.lower() or "torrent" in message.content.lower() or "legionmuzik" in message.content.lower()):
            if "mod" not in [y.name.lower() for y in message.author.roles]:
                chn = bot.get_channel("560534679229431808")
                await bot.send_message(chn, "<@"+str(message.author.id)+">: " + message.content)
                await bot.delete_message(message)
    
    #if (message.channel.id == "567801985374355476"):
    #    if message.attachments:
    #        pic = message.attachments[0]['url']
    #        picext = ['.png','.jpeg','.jpg',".bmp"]
    #        for ext in picext:
    #            if ext in pic:
    
    if (message.channel.id == "472402996378992650"):
        if message.attachments:
            pic = message.attachments[0]['url']
            picext = ['.wav','.mp3','.m4a',".flac"]
            for ext in picext:
                if ext in pic:
                    if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel, "Hey <@"+str(message.author.id)+">, please be sure to give feedback to a track. Don't be that guy. Nobody likes that guy.")
                        await bot.delete_message(message)
    
    if ("music producer/engineer here based on nyc" in message.content.lower()):
        await bot.delete_message(message)
    
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
                if (message.channel.id is "560511832322736138"):
                    if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because your account here is still new, and to avoid leech behavior this track is being deleted. In addition, this channel is for feedbacks - which requires users to give a feedback before asking for one/posting a song. If you feel this is an error please let someone know.")
                        await bot.delete_message(message)
                        chn = bot.get_channel("560534679229431808")
                        await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
                        await bot.send_message(chn, message.content)
                    if "feedback" in [y.name.lower() for y in message.author.roles]:
                        print("They have feedback")
                if (message.channel.id is not "560511832322736138"):
                    if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because your account here is still new. To avoid leech behavior here this track is being deleted. In the meantime, please try and engage with the community here a bit, and in up to an hour you can post your tracks. If you feel this is an error, please let someone know.")
                        await bot.delete_message(message)
                        chn = bot.get_channel("560534679229431808")
                        await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
                        await bot.send_message(chn, message.content)
                    if "feedback" in [y.name.lower() for y in message.author.roles]:
                        print("They have feedback")
    
    if "Timeout" in [y.name.lower() for y in message.author.roles]:
        await bot.delete_message(message)
        
    if "discord.gg/" in message.content:
        if "mod" in [y.name.lower() for y in message.author.roles]:
            print("allowed to post track")
        if "mod" not in [y.name.lower() for y in message.author.roles]:
            await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because you are posting a discord link. If you would like to have your server promoted, please see #rules and #other-discord-promotion for more info on how to get your link shared.")
            await bot.delete_message(message)
            chn = bot.get_channel("560534679229431808")
            await bot.send_message(chn, "Deleted discord link posted by <@"+str(message.author.id)+">")
    
    if "feedback leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content or "http://" in message.content):
            await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because you have the role Feedback Leech, which means you've been leaching off the community or the feedback channel. If you feel this is an error, please let someone know. To get the role removed you should have at least 10 Karma, which you can get by giving people Feedback.")
            await bot.delete_message(message)
            chn = bot.get_channel("560534679229431808")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            print("track deleted")

    if "leech" in [y.name.lower() for y in message.author.roles]:
        if ("https://" in message.content or "soundcloud.com" in message.content or "http://" in message.content or "http://" in message.content):
            await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, you're getting this message because you have the role Feedback Leech, which means you've been leaching off the community or the feedback channel. If you feel this is an error, please let someone know. To get the role removed you should have at least 10 Karma, which you can get by giving people Feedback.")
            await bot.delete_message(message)
            chn = bot.get_channel("560534679229431808")
            await bot.send_message(chn, "Deleted track posted by <@"+str(message.author.id)+">")
            await bot.send_message(chn, message.content)
            print("track deleted")
            
    if ("nigger" in message.content.lower() or "fag" in message.content.lower() or "aggot" in message.content.lower()):
        chn = bot.get_channel("560534679229431808")
        await bot.send_message(chn, "<@"+str(message.author.id)+">: " + message.content)
        await bot.delete_message(message)
            
    mod_feedback = True
        
    if (mod_feedback is True):
        
        feedback_barrier = 2
        
        if (message.channel.id == "560511832322736138"):
            if message.attachments:
                mat = message.attachments[0]['url']
                mus_ext = ['.wav','.mp3','.flax',".aiff",".ogg",".aiff",".alac"]
                for ext in mus_ext:
                    if ext in mat:
                        cnn = feedback_barrier;
                        if "feedback" in [y.name.lower() for y in message.author.roles]: cnn = 2;
                        if "good feedback" in [y.name.lower() for y in message.author.roles]: cnn = 2;
                        if "🎧🎧🎧quality feedback giver🎧🎧🎧" in [y.name.lower() for y in message.author.roles]: cnn = 2;
                        km = karmamod(message.author.id, cnn, "sub")
                        if (km < feedback_barrier):
                            role = discord.utils.get(message.server.roles, name="Feedback")
                            await bot.remove_roles(message.author, role)
                        else:
                            return
        
        if ( (message.channel.id == "472402996378992650") and ("https://" in message.content or "soundcloud.com" in message.content or "http://" in message.content)):
            if "feedback" not in [y.name.lower() for y in message.author.roles]:
                await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, in order to post here you must have the feedback role, and it looks like you don't have it. To get the feedback role you must give someone feedback first. Please remember this is a **feedback** channel, not a promotion channel.")
                await bot.delete_message(message)
        
        if (message.channel.id == "472402996378992650" and ("http" not in message.content.lower())):    
            if any(fbr in message.content.lower() for fbr in fb_list):
                role = discord.utils.get(message.server.roles, name="Feedback")
                await bot.add_roles(message.author, role)
        
        if ( (message.channel.id == "560511832322736138") and ("https://" in message.content or "soundcloud.com" in message.content or "http://" in message.content)):
            if "🎧🎧🎧quality feedback giver🎧🎧🎧" not in [y.name.lower() for y in message.author.roles]:
                 if "feedback" not in [y.name.lower() for y in message.author.roles]:
                        await bot.send_message(message.channel , "Hey now <@"+str(message.author.id)+">, in order to post here you must have the feedback role, and it looks like you don't have it. To get the feedback role you need at least " + str(feedback_barrier) + " Karma, which you get automatically by giving people quality feedback.")
                        await bot.delete_message(message)
                        chn = bot.get_channel("560534679229431808")
                        await bot.send_message(chn, message.content)
                        #donothin = message.channel
                 if "feedback" in [y.name.lower() for y in message.author.roles]:
                    cnn = feedback_barrier;
                    if "feedback" in [y.name.lower() for y in message.author.roles]: cnn = 2;
                    if "good feedback" in [y.name.lower() for y in message.author.roles]: cnn = 1;
                    if "🎧🎧🎧quality feedback giver🎧🎧🎧" in [y.name.lower() for y in message.author.roles]: cnn = 0;
                    km = karmamod(message.author.id, cnn, "sub")
                    if (km < feedback_barrier):
                        role = discord.utils.get(message.server.roles, name="Feedback")
                        await bot.remove_roles(message.author, role)
                    else:
                        return
                            
            if "🎧🎧🎧quality feedback giver🎧🎧🎧" in [y.name.lower() for y in message.author.roles]:
                return
            
        if (message.channel.id == "560511832322736138" and ("http" not in message.content.lower())):    
            if any(fbr in message.content.lower() for fbr in fb_list):
                role = discord.utils.get(message.server.roles, name="Feedback")
                gfb = discord.utils.get(message.server.roles, name="Good Feedback")
                qfb = discord.utils.get(message.server.roles, name="🎧🎧🎧Quality Feedback Giver🎧🎧🎧")
                leech = discord.utils.get(message.server.roles, name="Leech")
                
                mg = message.content.split()
                
                points = 0
                
                mgr  = [word for word in mg if word.lower() in fb_list]
                
                for i in mgr:
                    index = fb_list.index(i)
                    pz = fb_points[index]
                    if (points > 0 and pz < 0):
                        return
                    if (pz >= 0):
                        points+=pz
                    if (pz < 0 and points < 1):
                        points += pz
                    
                print("points from feedback " + str(points))
                
                xo = karmamod(message.author.id, points, "add")
                if (xo >= feedback_barrier):
                    await bot.add_roles(message.author, role)
                if (xo >= 10):
                    await bot.remove_roles(message.author, leech)
                    await bot.add_roles(message.author, gfb)
                if (xo >= 20):
                    await bot.remove_roles(message.author, leech)
                    await bot.add_roles(message.author, qfb)
        
    if ("@" in message.content.lower()):
        
        old,kar = message.content.split("@")
        fb,other = kar.split(">")
        fb = fb.replace("!", "")
        
        #if (fb == message.author.id):
        #    print("Same ID error")
        #    return
        
        if (fb == "428972162779578368"):
            
            if ("lyrics" in message.content.lower() and not "feedback" in message.content.lower()):
                rand_lyrics = [
                    "i popped a percy now i'm swerving and im crashing just to hurt me",
                    "yuh yuh yuh yuh yuh yuh",
                    "Hoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\nHoes Mad\n",
                    "Beatin off to dead shit like a fuckin dead beat",
                    "im the shit IM STILL IN DIAPERS",
                    "the school thotty didn't think i was a hotty so i went to get my shotty",
                    "fuck the old me, don’t worry, i use protection",
                    "Innocent til she start sippin\nThighs so sore she starts limpin",
                    "Logging on minecraft and i get some iron\nI don't like fortnite and i'm very tired",
                    "Dap on them haters ya yeet i got some beetroot seeds and im going to stuff them down your knees and my mac 10 be sprayin out cheese and i got to leave because i just ejaculated On my peas",
                    "Ride like piranha, she eat me like soup",
                    "Screamin' eagles on my shoulders, tryin' my best to not get older. Figured out your girls number, plaguing outwards within the thunder",
                    "Y'all can't fuck with me\nchain around my neck, same color as pee",
                    "Pullin up in pull ups cus I'm shitting on you niggas",
                    "im so fresh you can suck my nuts",
                    "I'm snapping her pussy like legos",
                    "I love my wife!",
                    "Open up my brain and you’ll see that my thoughts go insane",
                    "Slurp on my gurp cus you know it's purp",
                    "Shit is real, i poop jerusalem",
                    "bath water tickles my beard like that activis when I'm sipping",
                    "she feeds me grapes when i eat her face",
                    "Blow on her cheek like a cartridge\nI paint on her face like an artist",
                    "Got some pics of us using toys in bed now that's a great story",
                    "You need some praise girl, get that ass raised girl",
                    "every conflict that I'm in I have a right to win\nto the people I'm a breath of fresh air like nitrogen",
                    "I got bands like woodstock\nhand on my dick I got my wood cocked",
                    "none of us would be here WITHOUT CUM",
                    "Now if I fuck this model\nAnd she just bleached her asshole\nAnd I get bleach on my T-shirt\nI'mma feel like an asshole",
                    "I drowned in the pussy so I swam in her butt",
                    "I'm rapping 25/7 cus I'm ahead of the game",
                    "She gave me head like an Atari",
                    "wish a nibba would like a tree in this bitch",
                    "I don't fuck with hoes but don't fuck up with wayne cuz when it wayne's it pours .",
                    "I'm on a roll like Cottonelle, I was made for all this shit",
                    "She calls me Angel Soft but I'm Angel Hard when I'm in her ass",
                    "I'm all ears. In otherwords, I'm hear for ya.",
                    "I'm trying to move a safe, like the safe was a safe house",
                    "Hey guys, Adolphany Hitlertano here with another 6/10 Kanye review",
                    "I guess when the stars align, you do like a solar system and planet out",
                    "she doing tricks with her pussy, I guess she a vagician",
                    "I'm rubbing her neck like Crayola",
                    "my fans love my music, they'll always want to rep this\nwhen I drop, they'll be foaming at the mouth like tetanus",
                    "She put the thong on my groin, then it go boing",
                    "She's licking my tongue like a pikachu",
                    "Paint her face rainbow like a tic-tac",
                    "She said she's bisexual so she got off with a good bye",
                    "your girl annoying, everywhere I go, she follow me\nI have to tell her where to put her mouth like geology",
                    "She said what happened to our chemistry?\nI said we lost the bond like telemetry",
                    "I'm the best at this rappin'\neverything I say is so fly like an arachnid",
                    "Y'all pissin yellow but I'm hydrated so I'm pissin jello",
                    "She stabbin me in the back so I seized her like I'm Plato",
                    "Deus Vult",
                    "She said let's party like it's the 60s cus we got the Great Depression",
                    "https://drive.google.com/open?id=1GBV07Uzy9pXKaUN-7OB11cgO8uoxFj6m",
                    "music so hot, it'll have your speakers meltin'\nthermometers would read over 95 Kelvin",
                    "i am cool\nu droll\ni have shame\nyou are lame\nyou are a shame\nand a disgrace\nto the human race\nyour face looks\nlike a mace\nand your name is ace\nand you like ass\nand you are a male\nwhich means you are a big rainbow homo\nand you like unicorns because YOU IS A BITCH!111"
                    "This is an excellent opportunity to learn to fly like David Bowie",
                    "These are some of the best people I've ever met",
                    "I want to fuck the devil",
                    "This one was so cool, I went over his words and his words were like shit, like, shit... he's like fucking a dude",
                    "I'm on the run, get me into the safehouse, and take me out!",
                    "What I mean is I've had sex and I'm hard as hell",
                    "Well then it's not fair for you to be in her ass while she gets her pussy washed",
                    "I may not find her beautiful yet, but I do find her incredibly sexy. I'm not trying to say that what I'm doing is wrong or that I'm a slavophile for wanting to feel the way I feel about the beautiful naked body of her. When I talk about my sex life and the fantasies of my mind I'm not just describing what I've experienced, I'm trying to convey the experience that I've had, and trying to convey a more realistic picture of that."
                ]
                feedback_message = "test text"
                rlstein = random.randint(0,len(rand_lyrics)-1)
                feedback_message = rand_lyrics[rlstein]
                await bot.send_message(message.channel, feedback_message)
            
            if ("feedback" in message.content.lower()):
                rand_feedback = random.randint(0, 31)
                rand_fb = [
                    "Yo fam, this shit bangs in the whip. Like as soon as I play this in my Honda Pilot, the whip bangs bro, and not like the porn studios. I fuck with it.",
                    "Not gonna lie fam, this shit weak. The fuck is going on with that bass? Is it outta tune? Just a weak melody? A lame ass bass I banged in my whip 500000000 times? fuck outta here with this lame shit",
                    "Ayy, this is pretty hot. Like I could just right now spread some oil on this, and fry some chicken on this song it's so hot. brb finna fry some chicken",
                    "brrr bruh. beat's so cold i gotta wear a thicc ass hoodie man. i mean im already wearing one, but now I gotta wear another. It's a struggle man.",
                    "First of all the fuck are you doing with this EQ nonsense? You don't know - exactly. Secondly, who the fuck taught you how to compress? Some bitch on Youtube? Bitch I roast the fuck out of those little shits for a living, so don't tell me you actually know how to mix. Cus listen here bitch, you don't know shit about music. I am music, and you don't know shit about me or my story. Thank you for coming to my TED talk, bitch.",
                    "Okay, honey, stop. Just fucking stop. Are you even producing, or are you just mashing random buttons on your shitty keyboard hoping they can make you the next Metro Boomin? Cus mmmm honey listen here - nobody can be Metro Boomin. Metro Boomin is a sexy god who I worship every night - so when I say no one can be him or be like him, I know what the fuck I am talking about. So just stop.",
                    "Okay so I just played this to my friends and they melted. On the good side, I fucking hated them. On the bad side, now I have to find friends again. Wanna be my friend?",
                    "So uh, this is pretty terrible chief. So terrible I am going to steal this and sell it to some high-up artist and take all the credit for it. Skrrt",
                    "Listened to this shit while meditating around my stacks of cash and my diamonds. Very good for the mood, I felt like Future.",
                    "I played this to a good friend of mine, Mr. Travis Scottington, you wouldn't know him. He liked it so much he kept saying something about something being straight up? I think he might have a weird fascination with his dick. Tbf, so do I.",
                    "I came back from a hot tub in the back of my F150 with my hot cousins to listen to this? Chief if you tag me again, I will have Mr. Boomin officially not trust you.",
                    "I played this to Drake, and he likes the beat because of how young it is.",
                    "Yo i spit out my Arizona tea as soon as that bass dropped man. Kinda came a little, too. Now that last part might have to do with the hentai I was watching, but I don't think so because I don't even like hentai.",
                    "Can i have sex with this beat? Cus this beat, especially the low ends of it man, are fine as hellllllll",
                    "This mix would be balanced if my monitors only had tweeters",
                    "This one could use some Waves Abbey Road Ultra de-distorter V4 to remove some overtones",
                    "Real music is made with physical instruments and that is a fact. Dont @ me.",
                    "Yoo bro this one is sicko mode! It bumps in my grandmas Camry 03 :ok_hand: ",
                    "Sounds good Can i post mine now??",
                    "There's something off about this but idk anyway check mine out!",
                    "Okay dis hard",
                    "i like the 808 anyway here’s my whole mixtape please like and repost",
                    "https://lesterisdead.com/",
                    "Damn, this some IGOR type shit",
                    "Snare needs more high-end, it doesn't hurt my ears",
                    "dope, but i think you should pitch the vocals down an octave",
                    "nice, try side chaining the snare to the master",
                    "it sounded quiet, so i turned up my headphones a little",
                    "use a childhood photo for cover art",
                    "it sounded awful, i smoked a j, it sounds ok now",
                    "i could mix this to sound wayyy better, not trynna be cocky",
                    "why does it sound like the drummer fell into their set at 27 lol",
                    "I mean it's good, but I prefer the National Geotrappin remix.",
                    "Well, at least it doesn't have Yxng Squirtle rapping on it. So it has that going for it. Barely.",
                    "I kinda wanna drink myself to sleep so I can forget I ever even heard that song.",
                    "If this song played Smash Bros, it would main Captain Falcon.",
                    "This bass drop is similar to Kanye dropping Yandhi: it doesn't fucking exist",
                    "xD lmfao this so fire HAHAHA",
                    "It's not like its a bad song it's just a little too sweet for me *laughs*",
                    "Do you see yourself doing music forever? *laughs* Are you going to keep going in this field?",
                    "the snare needs to have a more pronounced 'click","the low frequency and high frequency are really similar, you should keep all of them, or stick to that",
                    "that's a good idea, the low frequencies should be boosted"
                ]
                feedback_message = "test text"
                rlstein = random.randint(0,len(rand_fb)-1)
                feedback_message = rand_fb[rlstein]
                await bot.send_message(message.channel, feedback_message)
           
    await bot.process_commands(message)

client = discord.Client()
my_server = client.get_server('server id')
    
@bot.event
async def on_member_join(member):
    server = member.server.id
    if (server == "446157087211520030"):
        rules = bot.get_channel('560535198769348631')
        getarole = bot.get_channel('560551182586609712')
        feedbacks = bot.get_channel('560511832322736138')
        message = 'Welcome {0.mention} to HipHop Creation Central! Please be sure to read the {1.mention}! If you need help using me head to {2.mention} and type !help\nPlease note if you want to post in {3.mention} you must first give quality feedback to someone.'.format(member,rules,getarole,feedbacks)
        chn = bot.get_channel("560542321490264076")
        await bot.send_message(chn, message)
    
@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title="help", description="        This Command helps with commands for me", color=0x7abae8)
    embed.add_field(name="producer ", value="        Gives you the Producer role", inline=False)
    embed.add_field(name="rapper ", value="        Gives you the Rapper role", inline=False)
    embed.add_field(name="singer ", value="        Gives you the Singer role", inline=False)
    embed.add_field(name="artist ", value="        Gives you the Singer role", inline=False)
    embed.add_field(name="engineer ", value="        Gives you the Engineer role", inline=False)
    embed.add_field(name="freestyler ", value="        Gives you the Freestyler role", inline=False)
    embed.add_field(name="twitch ", value="        Gives you the Twitch Feedback role for the twitch streams done here sometimes", inline=False)
    embed.add_field(name="roulette ", value="        Gives you 3 samples from youtube", inline=False)
    embed.add_field(name="sample ", value="        Gives you 1 sample from youtube", inline=False)
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
async def vox23(ctx):
    await bot.say("https://cdn.discordapp.com/attachments/446169554197151744/548588579329146890/VOX_23.wav");

@bot.command(pass_context = True)
async def sample(ctx):
    if (ctx.message.channel.id == "560556421733810187" or ctx.message.server.id != "446157087211520030"):
        f = open("BotSampleList.txt", 'r')
        x = f.readlines()
        f.close()
        urls = str(x[random.randrange(0, len(x)-1)])
        await bot.say(urls)
    if (ctx.message.channel.id != "560556421733810187" and ctx.message.server.id == "446157087211520030"):
        await bot.say("Please use <#560556421733810187> instead so this channel doesn't get cluttered")

@bot.command(pass_context = True)
async def roulette(ctx):
    
    if (ctx.message.channel.id == "560556421733810187" or ctx.message.server.id != "446157087211520030"):
        f = open("BotSampleList.txt", 'r')
        x = f.readlines()
        f.close()
        urls = str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)]) + "\n" + str(x[random.randrange(0, len(x)-1)])
        await bot.say(urls)
    if (ctx.message.channel.id != "560556421733810187" and ctx.message.server.id == "446157087211520030"):
        await bot.say("Please use <#560556421733810187> instead so this channel doesn't get cluttered")

@bot.command(pass_context = True)
async def yeet(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="Extremely politically correct")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def archive(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="archive")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
    
@bot.command(pass_context = True)
async def twitch(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="TwitchFeedback")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")
  
@bot.command(pass_context = True)
async def admin(ctx):
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
        await bot.say("Role not found :(")

@bot.command(pass_context = True)
async def rapper(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="🎤🎤🎤Rapper🎤🎤🎤")
    await bot.add_roles(ctx.message.author, role)
    await bot.say("Role successfully added!")

@bot.command(pass_context = True)
async def reset(ctx):
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):
        await bot.say("Resetting :D")
        exit()
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

@bot.command(pass_context = True)
async def givekarma(ctx, member: str):
    member = member.replace("@", "")
    member = member.replace("<", "")
    member = member.replace(">", "")
    member = member.replace("!", "")
    
    if (ctx.message.author.id == member):
        await bot.say("Hey now, you can't give yourself karma <:gtfo:479669715669745673>")
    else:
        yo = karmamod(ctx.message.author.id, 1, "sub")
        xo = karmamod(member, 1, "add")
        await bot.say("Gave them 1 karma")
        

@bot.command(pass_context = True)
async def setkarma(ctx, amt: int, member: str):

    if "mod" in [y.name.lower() for y in ctx.message.author.roles]:
        member = member.replace("@", "")
        member = member.replace("<", "")
        member = member.replace(">", "")
        member = member.replace("!", "")
        
        xo = karmamod(member, amt, "set")
        await bot.say("Set their karma to " + str(xo))

    if "mod" not in [y.name.lower() for y in ctx.message.author.roles]:
        await bot.say("Hey now, you can't use that")
        
@bot.command(pass_context = True)
async def viewallkarma(ctx):
    #downloadfile(0)
    xo = karmamod("428972162779578368", 0, "add")
    msx = ""

    with open("karma.txt", "r") as kfile:

        for line in kfile:
            if (line is not '\n'):
                ping,count=line.split(',')
                ping = "<@"+ping+">"
                msx += ping+","+count
        #await bot.say(msx)
        await bot.send_file(ctx.message.channel, "karma.txt")
            
        
@bot.command(pass_context = True)
async def viewkarma(ctx, member : discord.Member = None):

    noun = "They"

    if (member is not None):
        member = str(member.id)
        member = member.replace("@", "")
        member = member.replace("<", "")
        member = member.replace(">", "")
        member = member.replace("!", "")
    if member is None:
        member = str(ctx.message.author.id)
        noun = "You"

    print (member)
    
    if (member == "428972162779578368"):
        noun = "I"
    
    xo = karmamod(member, 0, "add")
    
    await bot.say(noun + " have " + str(xo) + " karma.")

@bot.command(pass_context = True)
async def sayinchannel(ctx, roomid: str, *, msg_str: str):

    chn = bot.get_channel(roomid)
    
    id = str(ctx.message.author.id)
    
    if "admin" in [y.name.lower() for y in ctx.message.author.roles]:

        await bot.send_message(chn, msg_str)
        
    if "admin" not in [y.name.lower() for y in ctx.message.author.roles]:
        await bot.say("Hey now, you can't use that")
        
bot.run(os.environ['BOT_TOKEN'])
