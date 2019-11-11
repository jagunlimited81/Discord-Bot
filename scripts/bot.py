# bot.py
import configparser
import discord
import praw
import random
from discord.ext import commands

# Discord
TOKEN = None
MENTION = None
BOT_PREFIX = None
# Discord Client
client = None

# Reddit praw
reddit = None
# This is a global variable to let the on_message function
# know that a command was done
didcommand = False


def initialize():
    global TOKEN, MENTION, BOT_PREFIX, client, reddit
    config = configparser.ConfigParser()
    config.read("keys.txt")
    # Discord config
    TOKEN = config["Discord"]["token"]
    MENTION = config["Discord"]["mention"]
    BOT_PREFIX = config["Discord"]["BOT_PREFIX"] \
        if config["Discord"]["BOT_PREFIX"].lower() != "default" \
        else MENTION + " "
    # Discord bot client
    client = commands.Bot(command_prefix=BOT_PREFIX)
    # Reddit config
    client_id = config["Reddit"]["client_id"]
    client_secret = config["Reddit"]["client_secret"]
    user_agent = config["Reddit"]["user_agent"]
    username = config["Reddit"]["username"]
    password = config["Reddit"]["password"]
    # Reddit Client
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=username,
                         password=password)
    print("initialized")
    client.remove_command("help")


# Set up configuration variables
initialize()


@client.event
async def on_ready():
    try:
        print("Logged in as")
        print(client.user.name)
        print(client.user.id)
        print("------")
    except Exception as e:
        print(e)
    activity = discord.Activity(name="GodZilla movies", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


# These should be read from a file
greetings = ["hello",
             "hi",
             "hey",
             "good morning",
             "good afternoon",
             "good evening",
             "how are you doing",
             "sup",
             "good day",
             "wassup"]

suicidejokes = ["i wanna die",
                "i want death",
                "i want to die",
                "i want to kms",
                "i wanna kms",
                "i am sad",
                "im sad",
                "im gonna kill myself",
                "i am gonna kill myself",
                "i am gonna kms"
                "im gonna kms",
                "i have big sad",
                "i am big sad",
                "im big sad",
                "kill me",
                "kms"]

_8ballresponses = ['It is certain',
                   'Without a doubt',
                   'You may rely on it',
                   'Yes definitely',
                   'It is decidedly so',
                   'As I see it, yes',
                   'Most likely',
                   'Yes',
                   'Outlook good',
                   'Signs point to yes',
                   'Reply hazy try again',
                   'Better not tell you now',
                   'Ask again later',
                   'Cannot predict now',
                   'Concentrate and ask again',
                   'Don’t count on it',
                   'Outlook not so good',
                   'My sources say no',
                   'Very doubtful',
                   'My reply is no']

copypasta = ["Listen you son of a bitch, what the fuck’s your problem? You want to sit here and say that I’m "
             "a goddamn, fucking Russian. You get in my face with that I’ll beat your goddamn ass, you son of "
             "a bitch. You piece of shit. You fucking goddamn fucker. Listen fuckhead, you have fucking "
             "crossed a line. Get that through your goddamn fucking head. Stop pushing your shit. You’re the "
             "people that have fucked this country over and gangraped the shit out of it and lost an "
             "election. So stop shooting your mouth off claiming I’m the enemy. You got that you goddamn son "
             "of a bitch? Fill your hand.” I’m sorry, but I’m done. You start calling me a foreign agent, "
             "those are fucking fighting words. Excuse me.",

             "I don't give a fuck about you and your little fucking games haha ohh my fucking god you "
             "acutally think that you matter in this world holy shit what the fuck I'm fucking dying xD "
             "really wow just no you are NOTHING in this fucking world tell you what you are a fucking joke "
             "NO ONE CARES ABOUT YOU I HOPE YOU FUCKING GET CANCER AND THEN SURVIVE CANCER AND THEN THE "
             "CANCER COMES BACK AGAIN HOLY SHIT SERIOUSLY????? xDDDDDDDDDD WOW you are GARBAGE compared to me "
             "you're cock is smaller than a cockroach FAGGOT xDDDD SUCK MY GIRLFRIENDS COCK YOU FUCKING LOSER "
             "I HOPE A ANGRY JEWISH NIGGER FAGGOT COMES TO YOUR HOUSE AND RIPS YOUR INTESTINES OUT AND BLOOD "
             "GOES EVERYWHERE AND THEN HE SHOVES THE INTESTINES DOWN YOUR FUCKING LITTLE THROAT AND YOU CHOKE "
             "UNTIL YOUR ABOUT TO DIE BUT WAIT THERES MORE HE RIPS EACH OF YOUR LIMBS OFF AND YOU CRY IN PAIN "
             "THEN YOU DIE AND THEN HE BRINGS YOU BACK TO LIFE AND YOU FUCKING DIE AGAINNN!!!!!!!!!!!!!! I "
             "HATE YOU SO MUCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",

             "Wot the fok did ye just say 2 me m8? i dropped out of newcastle primary skool im the sickest "
             "bloke ull ever meet & ive nicked ova 300 chocolate globbernaughts frum tha corner shop. im "
             "trained in street fitin' & im the strongest foker in tha entire newcastle gym. yer nothin to me "
             "but a cheeky lil bellend w/ a fit mum & fakebling. ill waste u and smash a fokin bottle oer yer "
             "head bruv, i swer 2 christ. ya think u can fokin run ya gabber at me whilst sittin on yer arse "
             "behind a lil screen? think again wanka. im callin me homeboys rite now preparin for a proper "
             "scrap. A roomble thatll make ur nan sore jus hearin about it. yer a waste bruv. me crew be all "
             "over tha place & ill beat ya to a proper fokin pulp with me fists wanka. if i aint satisfied w/ "
             "that ill borrow me m8s cricket paddle & see if that gets u the fok out o' newcastle ya daft "
             "kunt. if ye had seen this bloody fokin mess commin ye might a' kept ya gabber from runnin. but "
             "it seems yea stupid lil twat, innit? ima ****e fury & ull drown in it m8. ur ina proper mess "
             "knob.",

             "The FUCK did you say to me you little shit!?",

             "Watch your fucking launguage!",

             "YOU’RE TEARING ME APART LISA!!!"]

swearwords = ["fuck", "shit", "ass", "damn", "bitch", "cunt", "boomer", "damn", "uwu", "owo", "dammit"]

im = ["im", "i am", "i'm"]

companies = ["mcdonalds", "brianna", "burger king", "wendys"]

shutup = "I will not tolerate you saying the words that consist of the letters 's h u t u p' being said in this " \
         "server, so take your own advice and close thine mouth in the name of the christian minecraft server owner. "


def isoneword(word: str):
    return len(word.split()) == 1


def hasgreet(message):
    for str in greetings:
        if str in message.content.lower():
            print(isoneword(str))
            if isoneword(str):
                if str in message.content.lower().split():
                    return True
            else:
                return True
    return False


def returngreet(message):
    for greeting in greetings:
        if greeting in message.content.lower():
            return message.content[message.content.lower().find(greeting):][:len(greeting)]
    return "good day"


@client.event
async def on_message(message):
    global didcommand
    # useful
    loweredmessage = message.content.lower()
    loweredmessagewords = message.content.lower().split()
    print(str(message.author)[:-5] + " >  ", message.content)

    # ensure that the message is not sent by the bot itself
    if message.author == client.user:
        return

    # check if commands were done
    await client.process_commands(message)
    if didcommand:
        didcommand = False
        return
    else:
        didcommand = False

    # swearing
    for swearword in swearwords:
        if swearword in loweredmessage:
            if swearword == "ass":
                if swearword in loweredmessagewords:
                    await message.channel.send(random.choice(copypasta))
                    return
            else:
                await message.channel.send(random.choice(copypasta))
                return

    # suicide enforcement
    if any(s.lower() in loweredmessage.replace("'", "") for s in suicidejokes):
        await message.channel.send(f"do it pussy {message.author.mention}")
        return

    # SILENCE, BRAND
    for company in companies:
        if company.lower() in loweredmessage.replace("'", ""):
            await message.channel.send("SILENCE, BRAND!!!")
            await message.channel.send(file=discord.File("brand.jpg"))
            return

    # dadbot hello son, I am dad!
    for occurence in im:
        if occurence in loweredmessagewords:
            await message.channel.send(
                f"hello {message.content[(loweredmessage.find(occurence) + len(occurence) + 1):]}! I'm "
                f"Pubert!")
            return

    # greetings
    if hasgreet(message):
        await message.channel.send(f"{returngreet(message)} {message.author.mention}!")
        return

    # response to gay
    if ("gay" in loweredmessagewords or "faggot" in loweredmessagewords) and \
            ("pubert" in loweredmessagewords or "<@!635370091277713409>" in loweredmessagewords):
        await message.channel.send(f"You're gay, faggot")
        return

    # response to bot
    if "bot" in loweredmessagewords or "pubert" in loweredmessagewords:
        await message.channel.send(f"I just want to be left alone")
        return

    # response to I want
    if loweredmessage.startswith("i want"):
        await message.channel.send(f"the only thing you should want is BONES!")
        return

    # response to I have
    if loweredmessage.startswith("i have"):
        await message.channel.send(f"not for long bitch")
        return

    # response to I need
    if loweredmessage.startswith("i need"):
        await message.channel.send(f"the only thing you need is calcium.")
        return

    # response to I love
    if loweredmessage.startswith("i love"):
        await message.channel.send(f"{message.author.mention} :heart:")
        return

    # response to I made
    if loweredmessage.startswith("i made"):
        await message.channel.send(f"nobody cares.")
        return

    # response to I wish
    if loweredmessage.startswith("i wish"):
        await message.channel.send(f"{message.author.mention} that will be $399.99")
        return

    # response to why
    if loweredmessage.startswith("why"):
        await message.channel.send(f"{message.author.mention} why not?")
        return

    # response to same
    if loweredmessage.startswith("same"):
        await message.channel.send(f"same")
        return

    # response to nice
    if loweredmessage.startswith("nice"):
        await message.channel.send(f"nice")
        return

    # response to wait
    if loweredmessage.startswith("wait"):
        await message.channel.send(f"I'm not gonna wait for this shit.")
        return

    # response to no
    if loweredmessage.startswith("no"):
        await message.channel.send(f"{message.author.mention} yes bitch")
        return

    # response to duty
    if "duty" in loweredmessagewords:
        await message.channel.send(f"{message.author.mention} said doody")
        return

    # response to yes
    if loweredmessage.startswith("yes"):
        await message.channel.send(f"faggot")
        return

    # response to idk
    if loweredmessage.startswith("idk"):
        await message.channel.send(f"{message.author.mention} you would know if you weren't so gay")
        return

    # response to omg or omfg
    if loweredmessage.startswith("omg") or loweredmessage.startswith("omfg"):
        await message.channel.send(f"omg becky")
        return

    # response to shut up
    if "shut" in loweredmessage and "up" in loweredmessage:
        await message.channel.send(f"Listen here {str(message.author)[:-5]}, " + shutup)
        return


@client.command()
async def ping(ctx):
    global didcommand
    didcommand = True
    await ctx.send(f"```\nPong {round(client.latency * 1000)}ms\n```")


@client.command()
async def watch(ctx, *, film):
    global didcommand
    didcommand = True
    activity = discord.Activity(name=film, type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


@client.command()
async def meme(ctx, subreddit="dankmemes", sort="hot"):
    global didcommand
    didcommand = True
    sort = sort.lower()
    if sort == "hot":
        memes_submissions = reddit.subreddit(subreddit).hot()
    elif sort == "new":
        memes_submissions = reddit.subreddit(subreddit).new()
    elif sort == "rising":
        memes_submissions = reddit.subreddit(subreddit).rising()
    else:
        memes_submissions = reddit.subreddit(subreddit).hot()

    post_to_pick = random.randint(1, 10)
    if sort == "top":
        post_to_pick = 1
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.channel.send(submission.url)


@client.command(aliases=['8ball', '8b'])
async def _8ball(ctx, *, question):
    global didcommand
    didcommand = True
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ballresponses)}')


@client.command()
async def rate(ctx, *, movie):
    global didcommand
    didcommand = True
    rating = random.randint(1, 10)
    if rating > 6:
        filename = "goodratings.txt"
    elif rating < 5:
        filename = "badratings.txt"
    else:
        filename = "neutralratings.txt"
    with open(filename) as file:
        responses = (line.rstrip() for line in file)
        responses = list(line for line in responses if line)  # Non-blank lines in a list
    file.close()
    await ctx.send(f'{movie}: {rating}/10 {random.choice(responses)}')


@client.command(aliases=["lr"])
async def listrate(ctx):
    global didcommand
    didcommand = True
    with open("ratings.txt") as f_in:
        responses = (line.rstrip() for line in f_in)
        responses = list(line for line in responses if line)  # Non-blank lines in a list
    f_in.close()
    await ctx.send(responses)


@client.command(aliases=["ars"])
async def addrateresponse(ctx, parameter="-n", *, rating):
    global didcommand
    didcommand = True
    if parameter == "-b":
        filename = "badratings.txt"
    elif parameter == "-g":
        filename = "goodratings.txt"
    elif parameter == "-n":
        filename = "neutralratings.txt"
    else:
        await ctx.send("Syntax is @Pubert ars parameter 'sentence'")
        await ctx.send("The available parameters are -n(eutral) -g(ood) -b(bad)")
        return
    with open(filename, "a") as f:
        f.write(rating + "\n")
    f.close()
    await ctx.send(f"added {rating}")


@client.command(aliases=['clean', 'wipe', 'purge'])
async def clear(ctx, *, amount):
    global didcommand
    didcommand = True
    if "all" in amount:
        await ctx.channel.purge(limit=10000)
        await ctx.send(f"Deleted all messages {ctx.message.author.mention}")
    elif amount.isdigit():
        amount = int(amount)
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {amount} messages {ctx.message.author.mention}")
    else:
        amount = 10
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {amount} messages {ctx.message.author.mention}")


@client.command()
async def say(ctx, *, phrase):
    global didcommand
    didcommand = True
    await ctx.message.delete(delay=None)
    await ctx.send(phrase)


@client.command(pass_context=True)
async def help(ctx, command=""):
    global didcommand
    didcommand = True
    embed = discord.Embed(
        title="Pubert's help",
        color=discord.colour.Color.purple()
    )
    embed.set_author(name="Pubert Bot, by jagunlimited81")

    if command == "":
        embed.add_field(name="help ('command')",
                        value="displays this message",
                        inline=False)
        embed.add_field(name="ping",
                        value="returns pong and the time in miliseconds from the bot to discord",
                        inline=False)
        embed.add_field(name="clear ('all' or integer)",
                        value="purges chat",
                        inline=True)

        embed.add_field(name="8ball 'sentence'",
                        value="returns your fortune",
                        inline=False)
        embed.add_field(name="rate 'object'",
                        value="returns a rating of the object",
                        inline=False)
        embed.add_field(name="listrate",
                        value="broken atm",
                        inline=False)
        embed.add_field(name="addrateresponse 'parameter' 'sentence'",
                        value="takes one parameter [-n(eutral) -g(ood) -b(bad)] and a sentence",
                        inline=False)
        embed.add_field(name="say 'sentence'",
                        value="makes Pubert say 'sentence'",
                        inline=False)
        embed.add_field(name="meme ('subreddit' 'sort')",
                        value="makes Pubert do a meme",
                        inline=False)

    elif command == "help":
        embed.add_field(name="help ('command')",
                        value="Displays the help screen. If a command is placed after the help command, it will"
                              "display specific help.",
                        inline=False)
    elif command == "ping":
        embed.add_field(name="ping",
                        value="Returns the ping value fom Pubert to the Discord servers.",
                        inline=False)
    elif command == "clear":
        embed.add_field(name="clear ('all' or integer)",
                        value="Deletes 10 messages by default. Overrideable by "
                              "providing an integer value or 'all'",
                        inline=False)
    elif command == "8ball":
        embed.add_field(name="8ball 'sentence'",
                        value="Returns an 8ball fortune for said 'sentence'",
                        inline=False)
    elif command == "rate":
        embed.add_field(name="rate 'object'",
                        value="Pubert will rate the 'object' out of ten, then say his "
                              "official verbal analysis of what he thought about it.",
                        inline=False)
    elif command == "listrate":
        embed.add_field(name="listrate",
                        value="broken atm",
                        inline=False)
    elif command == "addrateresponse":
        embed.add_field(name="addrateresponse 'parameter' 'sentence'",
                        value="Adds a 'sentence' to the pool of possible sentences for the rate command. It requires "
                              "one parameter [-n(eutral) -g(ood) -b(bad)] and a 'sentence'",
                        inline=False)
    elif command == "say":
        embed.add_field(name="say 'sentence'",
                        value="Makes Pubert say 'sentence'",
                        inline=False)
    elif command == "meme":
        embed.add_field(name="meme ('subreddit' 'sort')",
                        value="Pubert grabs a meme from that subreddit with the specified sorting order",
                        inline=False)
    else:
        embed.add_field(name=command,
                        value="Doesn't make Pubert do shit",
                        inline=False)
        await ctx.send(embed=embed)
        return

    await ctx.send(embed=embed)


# run the bot
client.run(TOKEN)
