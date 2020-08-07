import discord                      #---------------
from discord.ext import commands    #At this part we import all modules we need
from discord.utils import get       #
import requests                     #
import json                         #
import smtplib, ssl                 #
from datetime import datetime       #---------------


                                                    #At this part we set up the nesescary variables for gmail autenthication
                                                    #Variables store specified data
                                                    #
port = 465                                          #In this case the variable named "port" get the value of '465'
context = ssl.create_default_context()              #We assign the background context of the gmail login to a variable
sender_email = "starbort.quanteedev@gmail.com"      #We assign the email adress the bot use to send emails to a variable
receiver_email1 = "balinticha3@gmail.com"           #The emails i have to send the emails to. There could be receiver_email1, receiver_email2, and so on

password = input("Gmail autenthication requied: ")  #Upon starting the bot we ask for the gmail password of sender_email(starbort.quanteedev@gmail.com)

bot = commands.Bot(command_prefix='!')              #We set the prefix of the bot

DISCORD_TOKEN = ''   #This is similar to a password to your discord account
                     #this is excluded from the public code for security reasons

client = discord.Client()

# debugChannel = bot.get_channel(739114380775653467)

@bot.event
async def on_ready():                                               #if the bot logged in with discord
    print(f'{bot.user.name} has connected to Discord!')             #we show a confirmation message in the console

@bot.command(name="bot.test", help="Bot test command. todo remove this from full release")  #function for the bot.test command
async def bot_test_response(ctx):                            #discord will automatically assign the value to the variable ctx
    await ctx.send("Command successfull on @ bot.command")   #this is the line for sending a message via discord
                                                             #the variable ctx contains which channel and server the bot should send a message.


@bot.command(name="faq", help="Frequently asked questions.")
async def bot_faq_response(ctx, *, faqobject="default"):    #the faqobject is the variable that contains the requested elements. (for example
                                                            #, if the command was !faq What is a flare , faqobject will be "what is a flare")

    if faqobject.lower() == "default":                      #we check if the faqobject is empty
        await ctx.send("Please enter a keyword")            #if yes, we do this
    elif faqobject.lower() == "all":                        #if not, we check if the faqobject is equal to "all"
        await ctx.send("All possible faq entries are: flare, indies, crystal, gas, metal, resource, mining, outclaiming, npc, fortress, outpost, claim, teams. More coming soon")
    else:                                                   #if not, we do this:
        with open("faqfile.json", 'r') as file:             #we open the faqufile.json file in my machine
            faq =  json.load(file)                          #we basically load the data from it
            for key in faq:                                 #and compare our faqobject with the keys in it
                if key in faqobject.lower():                #keys like "flare, blueprint, aa, stuff
                    await ctx.send(faq[key])                #if we found a match, we send the matching key's value

@bot.command(name="faq.add", help="Create a new faq entry")
@commands.has_role('Director')                              #we check if the sender has the role "Director"
async def bot_faq_add(ctx, key, *, despr):
    file = open("faqfile.json", "r")                        #we open the file in read-only mode
    faq = json.load(file)                                   #we load the data from it
    file.close()                                            #we close the file
    with open("faqfile.json", "w+") as file:                #we open he file in write-read mode and clear its content
        faq[key] = despr                                    #we add the new faq entry to the data
        json.dump(faq, file)                                #we save the data to our file
        await ctx.send("Entry recorded.")


@bot.command(name="alert", help="Creates a formatted warning message.")
@commands.has_role('Director')
async def alert_message_response(ctx, alertType="announcement", *, message):
    if alertType.lower() == "announcement" or alertType.lower() == "ann":
        alertChannel = bot.get_channel(736303176042676339)      #we get the channel by the channels ID
        endMessage = "\n**ANNOUNCEMENT**\n\n" + message + "\n[|| @everyone ||]"
        await alertChannel.send(endMessage)
    elif alertType.lower() == "warning":
        alertChannel = bot.get_channel(736303176042676339)
        endMessage = "\n**WARNING**\n\n" + message + "\n\[|| @everyone ||]"
        await alertChannel.send(endMessage)
    else:
        await ctx.send("Unknown alert type")

@bot.command(name="say", help="Makes the bot say something")
@commands.has_role('Director')
async def say_message(ctx, channelId, *, message):
    targetChannel =  bot.get_channel(int(channelId))
    await targetChannel.send(message)
    await ctx.send("Message successfully sent")

@bot.command(name="cat", help="Sends an adorable cute cat image. Don't spam this please.")
async def show_cat(ctx):
    try:
        response = requests.get('https://aws.random.cat/meow')      #we try to connect to https://aws.random.cat/meow and get a cat image
        data = response.json()                                      #we store the image in a variable
        await ctx.send(data['file'])                                #we send that variable(image) in a message
    except:
        await ctx.send("Random.cat API unreachable. try again later")   #if we can't connect to random.cat, we saend the error message

@bot.command(name="remind.record", help="Record a reminder")
@commands.has_role("Director")                                      #this is not implemented yet
async def reminder_record(ctx, reminderName, reminderContent):
    print("Todo") #todo

@bot.event                          #if a new member joins we do this
async def on_member_join(member):
    message = "Welcome " + str(member) + "!\nPlease make sure thet your discord name matches your ingame name, if not, please change your discord nickname. Please also tell us your ingame base coordinates. If instructed, message @woludyouliketoknow about your reason being here, othewise, please write it here."
    unresistrected = bot.get_channel(736303176042676336)
    await unresistrected.send(message)                 #we send our welcome message to the unresistrected channel
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:   #we initate a secure connection with gmail's servers
        server.login(sender_email, password)                                    #we login to gmail with our email and password we got earlier
        now = datetime.now()                                                    #we get the current date and time and assign it to te now variable
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")                           #we format the now variables content nicely and put it in the dt_string variable
        join_message = "Starbort alert\n" + str(member) + " joined SMC20 at " + dt_string + "!\n\nThis is an automatized message sent by Starbort.\nReport bugs to me." #we create a nicely formatted email message
        server.sendmail(sender_email, receiver_email1, join_message)            #we send that message to the receiver eails

@bot.event                                                                      #we do this if someone does not have roles for a specific command
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(DISCORD_TOKEN)                                                          #we run the bot and login with the token
