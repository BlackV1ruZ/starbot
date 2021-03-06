import io
import json
import os
import smtplib
import ssl
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands

port = int(os.getenv("STARBOT_PORT", 465))
context = ssl.create_default_context()
sender_email = os.getenv("STARBOT_SENDER_EMAIL", "starbort.quanteedev@gmail.com")
receiver_email1 = os.getenv("STARBOT_RECEIVER_EMAIL", "balinticha3@gmail.com")
environment = os.getenv("STARBOT_ENVIRONMENT", "development")
version = "8"  # Just update it/commit or pr

if environment == "production":
    password = input(
        "Gmail autenthication requied: ")  # Comment this out or set the environment variable STARBOT_ENVIRONMENT to development while testing

bot = commands.Bot(command_prefix='!')

DISCORD_TOKEN = os.getenv("STARBOT_DISCORD_TOKEN", "excluded")  # excluded from source control
FAQFILE_PATH = os.getenv("STARBOT_FAQFILE_PATH", os.path.join("data", "faqfile.json"))

client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="ver")
async def bot_version_response(ctx):
    await ctx.send("Starbot version " + version + ", mode " + environment + " by Quantee155 and blackv1ruz")


@bot.command(name="faq", help="Frequently asked questions.")
async def bot_faq_response(ctx, *, faqobject="default"):
    if faqobject.lower() == "default":
        await ctx.send("Please enter a keyword")
    elif faqobject.lower() == "all":
        await ctx.send("All possible faq entries are: flare, indies, crystal, gas, metal, resource, mining, outclaiming, npc, fortress, outpost, claim, teams. More coming soon")  # todo Don't make this hardcoded
    else:
        with open("faqfile.json", 'r') as file:
            faq = json.load(file)
            for key in faq:
                if key in faqobject.lower():
                    await ctx.send(faq[key])


@bot.command(name="faq.add", help="Create a new faq entry")
@commands.has_role('Director')
async def bot_faq_add(ctx, key, *, despr):
    file = open("faqfile.json", "r")
    faq = json.load(file)
    file.close()
    with open("faqfile.json", "w+") as file:
        faq[key] = despr
        json.dump(faq, file)
        await ctx.send("Entry recorded.")


@bot.command(name="alert", help="Creates a formatted warning message.")
@commands.has_role('Director')
async def alert_message_response(ctx, type="announcement", *, message):
    if type.lower() == "announcement" or type.lower() == "ann":
        alert_channel = bot.get_channel(736303176042676339)
        end_message = "\n**ANNOUNCEMENT**\n\n" + message + "\n[|| @everyone ||]"  # todo Maybe format this more nicely
        await alert_channel.send(end_message)
    elif type.lower() == "warning":
        alert_channel = bot.get_channel(736303176042676339)
        end_message = "\n**WARNING**\n\n" + message + "\n[|| @everyone ||]"
        await alert_channel.send(end_message)
    else:
        await ctx.send("Unknown alert type")


@bot.command(name="say", help="Makes the bot say something")
@commands.has_role('Director')
async def say_message(ctx, channel_id, *, message):
    target_channel = bot.get_channel(int(channel_id))
    await target_channel.send(message)
    await ctx.send("Message successfully sent")


@bot.command(name="cat", help="Sends an adorable cute cat image. Don't spam this please.", )
async def show_cat(ctx, tag: str = ""):
    cat_url = "https://cataas.com/cat"
    if len(tag) > 0:
        if tag == "says":
            return await ctx.send("Cats cant talk, silly! (Soon...)")
        else:
            cat_url += "/" + tag
    async with aiohttp.ClientSession() as session:
        async with session.get(cat_url) as resp:
            if resp.status != 200:
                return await ctx.send("The cats are all asleep. sshhhh")
            data = io.BytesIO(await resp.read())
            contenttype = resp.content_type.split("/")
            if contenttype[0] != "image":
                return await ctx.send("unkown content-type: " + resp.content_type)
            else:
                filename = "cat?." + contenttype[1]
                return await ctx.send(file=discord.File(data, filename))


@bot.event
async def on_member_join(member):
    message = "Welcome " + str(
        member) + "!\nPlease make sure thet your discord name matches your ingame name, if not, please change your discord nickname. Please also tell us your ingame base coordinates. If instructed, message @woludyouliketoknow about your reason being here, othewise, please write it here."
    unresistrected = bot.get_channel(736303176042676336)
    await unresistrected.send(message)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        join_message = "Starbort alert\n" + str(
            member) + " joined SMC20 at " + dt_string + "!\n\nThis is an automatized message sent by Starbort.\nReport bugs to me."
        server.sendmail(sender_email, receiver_email1, join_message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(DISCORD_TOKEN)
