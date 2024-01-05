import os

# discord files needed for bot
import discord
from discord.ext import commands

# needed for environment created for the bot key
from dotenv import load_dotenv

# beautiful soup imports for web scraping
import requests
from bs4 import BeautifulSoup

# numpy for dictionary file
import numpy as np

# for randomization
import random

# loads the environment that holds the discord token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents().default()
intents.members = True
intents.message_content = True        

bot = commands.Bot(command_prefix='!', intents = intents)

# list for all accounts
playerAccounts = {}

# used for list retrieval for bot txt files
contents = []

# retrieve all discord members' (that added their account to paimon bot) genshin player accounts
# this would be used for several account info retrieval for the bot in multiple methods
def get_playerAccounts():
    with open("playerAccounts.txt") as file:
        contents = file.readlines()

        # while reading the file receive the user accounts contained in the bot's txt file and add them to a list for easy access
        for line in contents:
            (user, acct_id) = line.split(": ")
            playerAccounts[user] = acct_id.strip("\n")

# connect the bot to the discord server
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    get_playerAccounts()


# Adds a player to given file of player accounts
@bot.command()
async def register(msg, accountId):

    player_name = msg.message.author.name # discord user name
    player_tag = msg.message.author.discriminator # number tag for each discord account
    player_id = str(msg.message.author.id) # discord id
    print(player_id)
    player = player_name + str(player_tag)

    # add member account info to the bot's save file
    with open("playerAccounts.txt", 'a') as file:
        file.write(player_id + ": " + accountId + "\n")

    # add discord member's account id to the list
    playerAccounts[player_id] = accountId
    response = "`You have been added to Paimon's system! ehe ଘ(੭ˊᵕˋ)੭* ੈ✩‧˚`"

    await msg.send(response)

# webscrap wiki and build for requested characters
@bot.command()
async def chars(msg, character):
    
    wiki_link =  character.title() + " Wiki:\n" + "https://genshin-impact.fandom.com/wiki/" + character    
    build_link = character.title() + " Build:\n" + "https://genshin-builds.com/character/" + character.lower()

    await msg.send(wiki_link)
    await msg.send(build_link)

# load player's genshin impact account as a link to the requested discord member
@bot.command()
async def player(ctx, user: discord.User):

    userId = str(user.id)
    
    # create the user account url
    url1 = "https://act.hoyolab.com/app/community-game-records-sea/index.html?bbs_presentation_style=fullscreen&bbs_auth_required=true&gid=2&user_id=" + playerAccounts[userId]
    url2 = "&utm_source=hoyolab&utm_medium=gamecard&bbs_theme=dark&bbs_theme_device=1#/ys"
    final_url = url1 + url2
    
    # add fancy style to look more discord like
    embed = discord.Embed(color = 0xFBFBAB)
    embed.set_author(name = user.name + " genshin stats", url = final_url, icon_url = user.avatar)

    await ctx.send(embed = embed)

# Paimon's random quotes when requested by user
@bot.command()
async def quote(ctx):
    
    # quote url
    URL = "https://www.thyquotes.com/paimon/"
    page = requests.get(URL)
    
    # read, seperate, and get the quotes from the site
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id = 'z') # get quotes on page
    quotes = results.find_all('p') # select only paimon quotes to get from a list
    
    # get a random quote
    new_quote = random.choice(quotes)
    
    # get only the body of the quote
    response = new_quote.get_text()
    
    # random paimon quote to be sent out to user
    embed = discord.Embed(title = "Paimon Says... ʕ•̀ω•́ʔ✧", description = response, color = 0xF5B5D1)

    await ctx.send(embed = embed)

# lists all the commands that paimon can use
@bot.command()
async def cmds(ctx):

    # title
    embed = discord.Embed(title = "Command List ʕっ• ᴥ • ʔっ", color = 0x9FC3ED)

    # pic on right
    embed.set_thumbnail(url="https://imgur.com/YZSybCY.jpeg")

    # commands w/ description
    embed.add_field(name="!register <Account ID>", value="register your genshin account to Paimon's system", inline=False)
    embed.add_field(name="!chars <character first name>", value="wiki/build for a specific character", inline=False)
    embed.add_field(name="!player <player name>", value="stats for a specific player", inline=False)
    embed.add_field(name="!quote", value="displays a random quote from paimon", inline=False)
    embed.add_field(name="!cmds", value="displays all of Paimon's commands", inline=False)

    await ctx.send(embed=embed)

bot.run(TOKEN)
