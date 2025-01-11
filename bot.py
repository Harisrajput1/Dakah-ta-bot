import os
os.system("pip install --upgrade pip")
os.system("pip install setuptools") 
import json
import string
import discord, aiohttp
from discord.ext import commands, tasks
import requests
from colorama import Fore, Style
import qrcode
import asyncio
import requests
import sys
import random
from flask import Flask
from threading import Thread
import threading
import subprocess
import requests
import time
from discord import Color, Embed
import colorama
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
from io import BytesIO
import webbrowser
from bs4 import BeautifulSoup
import datetime
from pyfiglet import Figlet
from discord import Member
import openai
from dateutil import parser
from collections import deque
from googletrans import Translator, LANGUAGES
import image
import afk

colorama.init()

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.typing = True
intents.presences = True
intents.dm_messages = True
intents.messages = True
intents.members = True
intents.guild_messages = True

category_messages = {}
active_tasks = {}
sent_channels = set()

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

siddhu = commands.Bot(description='SELFBOT CREATED BY siddhu',
                           command_prefix=prefix,
                           self_bot=True,
                           intents=intents)
status_task = None

siddhu.remove_command('help')

siddhu.whitelisted_users = {}

siddhu.antiraid = False

red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[36m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[94m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"

@siddhu.event
async def on_ready():
      print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.red_to_purple,
            f""" ____ ___ ____  ____  _   _ _   _ 
/ ___|_ _|  _ \|  _ \| | | | | | |
\___ \| || | | | | | | |_| | | | |
 ___) | || |_| | |_| |  _  | |_| |
|____/___|____/|____/|_| |_|\___/ 
THE ALL IN ONE MULTIPURPOSE SELFBOT
                                  
• Discord Server : discord.gg/tzshop
• Instagram : whoiz.siddhu

[+] ------------------------------------ [+]
[=] S I D D H U  C O R D  V2 [=]
[=] CREATED BY :- siddhu.og [=]
[=] LOGGED IN AS :- {siddhu.user.name} [=]
[+] ------------------------------------ [+]
""",
                1,
            )
        )
    )


def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

time_rn = get_time_rn()

@siddhu.event
async def on_message(message):
    if message.author.bot:
        return

    # Auto-response handling
    with open('ar.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await siddhu.process_commands(message)
    
    # Auto-message handling
def load_auto_messages():
    try:
        with open("am.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_auto_messages(data):
    with open("am.json", "w") as f:
        json.dump(data, f, indent=4)
        
#Discord Status Changer Class
class DiscordStatusChanger:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User-Agent": "DiscordBot (https://discordapp.com, v1.0)",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def change_status(self, status, message, emoji_name, emoji_id):
        jsonData = {
            "status": status,
            "custom_status": {
                "text": message,
                "emoji_name": emoji_name,
                "emoji_id": emoji_id,
            }
        }
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=self.headers, json=jsonData)
        return r.status_code
    
class StatusRotator(commands.Cog):
    def __init__(self, siddhu, token):
        self.bot = siddhu
        self.token = config.get('token')
        self.discord_status_changer = DiscordStatusChanger(self.token)
        self.is_rotating = False  # New attribute to control rotation

    @commands.command()
    async def start_rotation(self, ctx):
        if not self.is_rotating:
            self.is_rotating = True
            await ctx.send("**Starting status rotation...**")
            await self.run_rotation(ctx)
        else:
            await ctx.send("**Status rotation is already running.**")

    @commands.command()
    async def stop_rotation(self, ctx):
        if self.is_rotating:
            self.is_rotating = False
            await ctx.send("Stopping status rotation...")
        else:
            await ctx.send("Status rotation is not currently running.")

    async def run_rotation(self, ctx):
        file_path = 'status.txt'
        while self.is_rotating:
            try:
                with open(file_path, 'r') as file:
                    messages = [line.strip() for line in file.readlines()]

                if not messages:
                    await ctx.send("No messages found in the file. Add messages to continue.")
                    await asyncio.sleep(30)
                    continue

                for message in messages:
                    message_parts = message.split(',')

                    if len(message_parts) >= 2:
                        emoji_id = None
                        emoji_name = message_parts[0].strip()

                        if emoji_name and emoji_name[0].isdigit():
                            emoji_id = emoji_name
                            emoji_name = ""

                        status_text = message_parts[1].strip()

                        status_code = self.discord_status_changer.change_status("dnd", status_text, emoji_name, emoji_id)
                        if status_code == 200:
                            print(f"Changed to: {status_text}")
                        else:
                            print("Failed to change status.")
                        await asyncio.sleep(10)
            
            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(10)  # Retry after 10 seconds
                
TOKEN = config.get('token')
siddhu.add_cog(StatusRotator(siddhu, TOKEN))


#task
tasks_dict = {}

@siddhu.command()
async def help(ctx):
    message = '''# __**SIDDHU CORD V2**__ <a:Basu_Crown:1272964582264012810>
<:devs:1272936553668415521> **HELP COMMANDS**

<:blue_crown:1259181768414597242> **MAIN COMMANDS :-**
<:star:1272968556052746370> **AutoRespond** :-
<:arrow:1273294763415834637> `.ar <trigger>, <response>`
<:star:1272968556052746370> **Remove Respond** :-
<:arrow:1273294763415834637> `.removear <triger>`
<:star:1272968556052746370> **AutoRespond List** :- `.ar_list`
<:star:1272968556052746370> **AutoMsg** :-
<:arrow:1273294763415834637> `.am <time> <chnl_id> <msg>`
<:star:1272968556052746370> **Stop AutoMsg** :- `.am_stop <chnl_id>`
<:star:1272968556052746370> **AutoMsg List** :- `.am_list`
<:star:1272968556052746370> **Afk** :- `.afk <reason>`
<:star:1272968556052746370> **Remove Afk** :- `.unafk`
<:star:1272968556052746370> **Srv Clone** :-
<:arrow:1273294763415834637> `.csrv <copy id> <target id>`
<:star:1272968551212384329> **Status Rotator** :- `.start_rotation`
<:star:1272968551212384329> **Stop Rotator** :- `.stop_rotation`

<:Settings:1272970945467781121> **UTILITY COMMANDS :-**
<:settings:1273199795661701141> **Get Avatar** :- `.avatar <@user>`
<:settings:1273199795661701141> **Get Banner** :- `.banner <@user>`
<:settings:1273199795661701141> **Get Icon Of Server** :- `.icon`
<:settings:1273199795661701141> **Get Image** :- `.get_image <query>`
<:settings:1273199795661701141> **User Info** :- `.user_info <@user>`

<a:frostmm_inr:1273294780423471139> **INR & LTC WALLET :-**
<:INR:1272964761742737529> **Upi Id** :- `.upi`
<:INR:1272964761742737529> **Qr Code** :- `.qr`
<:INR:1272964761742737529> **Custom Qr** :- `.upiqr <amt> <note>`
<a:LTC:1272936098535968829> **Ltc Wallet** :- `.wallet_help`
<:SA_PepeDetective:1272936556054970408> **TYPE `.crypto_prices` TO GET PRICES **

<:heart1:1273294776841670656> **EXTRA COMMANDS :-**
<a:Heart:1272936099978674249> **Gen Joke** :- `.joke`
<a:Heart:1272936099978674249> **Gen Meme** :- `.meme`
<a:Heart:1272936099978674249> **Check Promo** :- `.checkpromo <promo>`
<a:Heart:1272936099978674249> **Check Token** :- `.checktoken <token>`

<:moneyWhite:1273294774765617193> **CALCULATION COMMANDS :-**
<:money:1272936106463330366> **Calculate** :- `.math <equation>`
<:money:1272936106463330366> **Inr To Crypto** :- `.i2c <inr amount>`
<:money:1272936106463330366> **Crypto To Inr** :- `.c2i <crypto amount>`

<:Staff_Apply:1273296686160285747> **ACTIVITY COMMANDS :-**
<:Partner:1272936558122635265> **Stream** :- `.stream <title>`
<:Partner:1272936558122635265> **Play** :- `.play <title>`
<:Partner:1272936558122635265> **Watch** :- `.watch <title>`
<:Partner:1272936558122635265> **Listen** :- `.listen <title>`
<:Partner:1272936558122635265> **Stop Activity** :- `.stopactivity`

<:IconStatusWebDND:1273294772739772456> **EXTRA COMMANDS :-**
<:lr_tick_1:1272936560068788398> **Snipe Deleted Msg** :- `.snipe`
<:lr_tick_1:1272936560068788398> **translate Msg** :- `.translate <msg>`
<:lr_tick_1:1272936560068788398> **Vouch** :- `.vouch <product for price>`
<:lr_tick_1:1272936560068788398> **Exch Vouch** :- `.exch <which to which>`

<:srn_heartmessage:1273294768121581659> **MESSEGE COMMANDS :-**
<:devloper:1273630361926107156> **Spam Msg** :- `.spam <amount> <msg>`
<:devloper:1273630361926107156> **Clear Msg** :- `.clear <amount>`
<:devloper:1273630361926107156> **Direct Msg** :- `.dm <@user> <msg>`
<:devloper:1273630361926107156> **Send Msg Ticket Create** :-
<:arrow:1273294763415834637> `.sc <cg-id> <msg>`
<:devloper:1273630361926107156> **Remove Msg Ticket Create** :- 
<:arrow:1273294763415834637> `.stopsc <cg-id>`

<:Ownership:1273294766028623999> **SELFBOT SUPPORT :-**
<:8534purpleowner:1272936103946747946> **Show All Commands** :- `.help`
<:8534purpleowner:1272936103946747946> **Support** :- `.support <problem>`
<:8534purpleowner:1272936103946747946> **Selfbot Info** :- `.selfbot`'''
    await ctx.send(message)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@siddhu.command()
async def upi(ctx):
    message = (f"<:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529> **UPI** <:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529> <:INR:1272964761742737529>")
    message2 = (f"{Upi}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@siddhu.command()
async def qr(ctx):
    message = (f"{Qr}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@siddhu.command()
async def addy(ctx):
    message = (f"<a:LTC:1272936098535968829> <a:LTC:1272936098535968829> <a:LTC:1272936098535968829> <a:LTC:1272936098535968829> **LTC ADDY** <a:LTC:1272936098535968829> <a:LTC:1272936098535968829> <a:LTC:1272936098535968829> <a:LTC:1272936098535968829> ")
    message2 = (f"{LTC}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@siddhu.command()
async def math(ctx, *, equation):
    # Send the equation to the math API for calculation
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'<a:Diamonds:1272969331596198010> **EQUATION**: `{equation}`\n\n<a:Diamonds:1272969331596198010> **Result**: `{result}`')
        await ctx.message.delete()
    else:
        await ctx.reply('<a:Diamonds:1272969331596198010> **Failed**')
        
@siddhu.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount / I2C_Rate
    await ctx.send(f"<a:Diamonds:1272969331596198010> **EQUATION**: `{amount}/{I2C_Rate}`\n\n<a:Diamonds:1272969331596198010> **Result** : `${inr_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}I2C DONE ✅ ")
    
@siddhu.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.send(f"<a:Diamonds:1272969331596198010> **EQUATION**: `{amount}*{C2I_Rate}`\n\n<a:Diamonds:1272969331596198010> **Result** : `₹{usd_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}C2I DONE ✅ ")
    
spamming_flag = True
# SPAM 
@siddhu.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print("{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN}SPAMMING SUCCESFULLY✅ ")
    
@siddhu.command(aliases=[])
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("<a:Diamonds:1272969331596198010> `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("<a:Diamonds:1272969331596198010> `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"<a:LTC:1272936098535968829> **ADDY**: `{LTC}` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n\n"

    await ctx.send(message)
    await ctx.message.delete()
    
@siddhu.command(aliases=['ltcbal'])
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("<a:Diamonds:1272969331596198010> `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("<a:Diamonds:1272969331596198010> `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"<a:LTC:1272936098535968829> **ADDY**: `{ltcaddress}` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n"
    message += f"<a:LTC:1272936098535968829> **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` <a:LTC:1272936098535968829>\n\n"

    await ctx.send(message)
    await ctx.message.delete()
          
@siddhu.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/https://Wallibear",
    )
    await siddhu.change_presence(activity=stream)
    await ctx.send(f"<a:Diamonds:1272969331596198010> **Stream Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@siddhu.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await siddhu.change_presence(activity=game)
    await ctx.send(f"<a:Diamonds:1272969331596198010> **Status For PLAYZ Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@siddhu.command(aliases=["watch"])
async def watching(ctx, *, message):
    await siddhu.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"<a:Diamonds:1272969331596198010> **Watching Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()
V4 = "ooks/11561870928088965"

@siddhu.command(aliases=["listen"])
async def listening(ctx, *, message):
    await siddhu.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"<a:Diamonds:1272969331596198010> **Listening Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@siddhu.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await siddhu.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED}STREAM SUCCESFULLY STOPED⚠️ ")

@siddhu.command()
async def exch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT | EXCHANGED {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} EXCH VOUCH✅ ")

@siddhu.command()
async def vouch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT SELLER | GOT {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    await ctx.send(f'**NO VOUCH NO WARRANTY OF PRODUCT**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} VOUCH SENT✅ ")
    
@siddhu.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<a:Diamonds:1272969331596198010> **The Price Of Ltc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} LTC PRICE SENT✅ ")
    else:
        await ctx.send("**<a:Diamonds:1272969331596198010> Failed To Fetch**")

@siddhu.command(aliases=['csol'])
async def solprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/solana'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<a:Diamonds:1272969331596198010> **The Price Of Sol Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SOL PRICE SENT✅ ")
    else:
        await ctx.send("**<a:Diamonds:1272969331596198010> Failed To Fetch**")

@siddhu.command(aliases=['cusdt'])
async def usdtprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/tether'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<a:Diamonds:1272969331596198010> **The Price Of Usdt Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} USDT PRICE SENT✅ ")
    else:
        await ctx.send("**<a:Diamonds:1272969331596198010> Failed To Fetch**")

@siddhu.command(aliases=['cbtc'])
async def btcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<a:Diamonds:1272969331596198010> **The Price Of Btc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} BTC PRICE SENT✅ ")
    else:
        await ctx.send("**<a:Diamonds:1272969331596198010> Failed To Fetch**")
        
@siddhu.command()
async def ar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('ar.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('ar.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'<a:Diamonds:1272969331596198010> **Auto Response Has Added.. !** **{trigger}** - **{response}**')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND ADDED✅ ")



@siddhu.command()
async def removear(ctx, trigger: str):
    with open('ar.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('ar.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'<a:Diamonds:1272969331596198010> **Auto Response Has Removed** **{trigger}**')
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND REMOVE✅ ")
    else:
        await ctx.send(f'<a:Diamonds:1272969331596198010> **Auto Response Not Found** **{trigger}**')
        
@siddhu.command()
async def ar_list(ctx):
    with open ("ars.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] ar_list Command Used")

@siddhu.command()
async def am_list(ctx):
    with open ("am.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] am_list Command Used")

@siddhu.command()
async def csrv(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = siddhu.get_guild(source_guild_id)
    target_guild = siddhu.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("<a:Diamonds:1272969331596198010> **Guild Not Found**")
        return

    # Delete all channels in the target guild
    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    # Delete all roles in the target guild except for roles named "here" and "@everyone"
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    # Clone roles from source to target
    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD")
            await asyncio.sleep(0)

            # Update role permissions after creating the role
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    # Clone channels from source to target
    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}  # to store mapping between source and target categories

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                # If the channel has a category, create it if not created yet
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                # Create the channel within the category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    # Check if the voice channel already exists in the category
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

                # Update channel permissions after creating the channel
                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)  # Add delay here
            else:
                # Create channels without a category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                    # Update channel permissions after creating the channel
                    for overwrite in channel.overwrites:
                        if isinstance(overwrite.target, discord.Role):
                            target_role = target_guild.get_role(overwrite.target.id)
                            if target_role:
                                await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                        elif isinstance(overwrite.target, discord.Member):
                            target_member = target_guild.get_member(overwrite.target.id)
                            if target_member:
                                await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                    await asyncio.sleep(0)  # Add delay here

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")
            
@siddhu.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        value = float(value.strip('$'))
        message = await ctx.send(f"<a:Diamonds:1272969331596198010> **Sending {value}$ To :-** {addy}")
        url = "https://api.tatum.io/v3/litecoin/transaction"
        
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=ltc")
        r.raise_for_status()
        usd_price = r.json()['usd']['ltc']
        topay = usd_price * value
        
        payload = {
        "fromAddress": [
            {
                "address": ltc_addy,
                "privateKey": ltc_priv_key
            }
        ],
        "to": [
            {
                "address": addy,
                "value": round(topay, 8)
            }
        ],
        "fee": "0.00005",
        "changeAddress": ltc_addy
    }
        headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        await message.edit(content=f"<a:Diamonds:1272969331596198010> **Successfully Sent {value}$ To {addy}**\nhttps://live.blockcypher.com/ltc/tx/{response_data["txId"]}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}LTC SEND SUCCESS✅ ")
    except:
        await ctx.send(content=f"<a:Diamonds:1272969331596198010> **Failed to send LTC Because** :- {response_data["cause"]}")

@siddhu.command(aliases=['purge, clear'])
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"<a:Diamonds:1272969331596198010> **Deleted {times} Messages**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PURGED SUCCESFULLY✅ ")
    
@siddhu.command()
async def user_info(ctx, user:discord.User):
    info = f'''## User Info
    - **Name** : `{user.name}`
    - **Display *Name** : `{user.display_name}`
    - **User Id** : `{user.id}`
    - **User Avater** : {user.avatar_url}
    `'''
    await ctx.send(info)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}USER INFO SUCCESFULLY✅ ")
    
@siddhu.command()
async def am(ctx, time_in_sec: int, channel_id: int, *, content: str):
    channel = siddhu.get_channel(channel_id)
    await ctx.message.delete()
    
    if channel is None:
        await ctx.send("<a:Diamonds:1272969331596198010> `Channel not found.`")
        return

    if time_in_sec <= 0:
        await ctx.send("<a:Diamonds:1272969331596198010> `Time must be greater than 0.`")
        return

    auto_messages = load_auto_messages()

    if str(channel_id) in auto_messages:
        await ctx.send(f"<a:Diamonds:1272969331596198010> **Auto Message already exists for channel {channel_id}.**")
        return

    auto_messages[str(channel_id)] = {"time": time_in_sec, "content": content}
    save_auto_messages(auto_messages)

    @tasks.loop(seconds=time_in_sec)
    async def auto_message_task():
        await channel.send(content)

    auto_message_task.start()
    tasks_dict[channel_id] = auto_message_task
    
    await ctx.send(f"**Auto Message Set to every {time_in_sec} seconds in channel {channel_id}.**")
    print("[+] Automessage Set Succesfully")

@siddhu.command()
async def am_stop(ctx, channel_id: int):
    await ctx.message.delete()
    if channel_id in tasks_dict:
        tasks_dict[channel_id].stop()
        del tasks_dict[channel_id]

        auto_messages = load_auto_messages()
        auto_messages.pop(str(channel_id), None)
        save_auto_messages(auto_messages)
        
        await ctx.send(f"<a:Diamonds:1272969331596198010> **Auto Message Stopped for channel {channel_id}.**")
        print("Automessage Stoped Succesfully")
    else:
        await ctx.send("<a:Diamonds:1272969331596198010> `No auto message task found for this channel.`")
        
def generate_upi_qr(amount, note):
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn={note}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return buffer
        
@siddhu.command(name='upiqr')
async def upiqr(ctx, amount: str,*,note: str):
    await ctx.message.delete()
    try:
        buffer = generate_upi_qr(amount, note)
        await ctx.send(file=discord.File(fp=buffer, filename='upi_qr.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    
@siddhu.command(name='joke')
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    await ctx.send(f"<a:Diamonds:1272969331596198010> {joke['setup']} - {joke['punchline']}")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}JOKE ✅ ")

@siddhu.command(name='meme')
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    meme = response.json()
    await ctx.send(meme['url'])
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MEME ✅ ")
    
@siddhu.command()
async def dm(ctx, user: discord.User, *, message):
    await ctx.message.delete()
    try:
        await user.send(f"{message}")
        await ctx.send(f"[+] Successfully DM {user.name}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} DM SENT✅ ")
    except discord.Forbidden:
        await ctx.send(f"[-] Cannot DM {user.name}, permission denied.")
    except discord.HTTPException as e:
        await ctx.send(f"[-] Failed to DM {user.name} due to an HTTP error: {e}")
    except Exception as e:
        await ctx.send(f"[-] An unexpected error occurred when DMing {user.name}: {e}")

@siddhu.command()
async def l2u(ctx, ltc_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = ltc_amt * ltc_to_usd_rate
        await ctx.send(f"<a:Diamonds:1272969331596198010> **EQUATION**: `{ltc_amt}*{ltc_to_usd_rate}`\n\n<a:Diamonds:1272969331596198010> `{ltc_amt} LTC = {output} USD`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} L2U✅ ")
    except requests.RequestException as e:
        await ctx.send(f"<a:Diamonds:1272969331596198010> `Error fetching Litecoin price: {e}`")

@siddhu.command()
async def u2l(ctx, usd_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = usd_amt / ltc_to_usd_rate
        await ctx.send(f"<a:Diamonds:1272969331596198010> **EQUATION**: `{usd_amt}/{ltc_to_usd_rate}`\n\n<a:Diamonds:1272969331596198010> `{usd_amt} USD = {output} LTC`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}U2L ✅ ")
    except requests.RequestException as e:
        await ctx.send(f"<a:Diamonds:1272969331596198010> `Error fetching Litecoin price: {e}`")
        
@siddhu.command()
async def support(ctx,*, message):
    await ctx.message.delete()
    msg = {
        "content": f"## Received New Support Message\n- **Message Sent By {ctx.author.name} ID {ctx.author.id}**\n**Message Content** = `{message}`"
    }
    try:
        r = requests.post("https://discord.com/api/webhooks/1273194714987888691/Qjb4BKW-JP_sop7UeqXpNXZiz8UAsg4uwm-BdpeatvSpS7R62AmMWNgXEMmbAtsVe6GE" , json=msg)
        print("[+] Support Message Sent Succesfully")
        await ctx.send("**Support Message Sent Succesfully**")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}SUPPORT✅ ")
    except:
        await ctx.send("**Failed. Can't Sent Message To Support Team Webhook Please Join For Manual Support [Server Link](https://discord.gg/siddhustore) **")
                    
@siddhu.command()
async def selfbot(ctx):
    await ctx.send('''# __SIDDHU CORD V2__ <a:Basu_Crown:1272964582264012810>  
**<:AsT_dot:1272936095771918417>VERSION - `SELFCORD V2`
<:AsT_dot:1272936095771918417>CREATOR - `siddhu.og`
<:AsT_dot:1272936095771918417>SUPPORT SERVER - [LINK](https://discord.gg/tzshop) 
<:AsT_dot:1272936095771918417>BUY HERE - [AUTOBUY](https://siddhu.sellauth.com/)
<:AsT_dot:1272936095771918417>FOR ANY HELP CONTACT SIDDHU

<:blue_crown:1259181768414597242> SIDDHU CORD IS ONE OF THE BEST SELFBOT WITH MANY COMMANDS & FEATURES, IT HAS INBUILT CUSTOM QR GENERATOR, TOKEN CHECKER & LTC SELF WALLET !!**''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}SELFBOT INFO✅ ")
    
@siddhu.command()
async def wallet_help(ctx):
    await ctx.send('''# <:woods_ltc:1273294778599084054> **LTC SELF WALLET :-**
<a:LTC:1272936098535968829> **Send Ltc** :- `.send <addy> <amount>`
<a:LTC:1272936098535968829> **Check Balance** :- `.bal <addy>`
<a:LTC:1272936098535968829> **Check Mybal** :- `.mybal`
<a:LTC:1272936098535968829> **Ltc Addy** :- `.addy`
<a:LTC:1272936098535968829> **Ltc To Usd** :- `.l2u <ltc amount>`
<a:LTC:1272936098535968829> **Usd To Ltc** :- `.u2l <usd amount>`''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}WALLET INFO✅ ")
    
@siddhu.command()
async def crypto_prices(ctx):
    await ctx.send('''# <:SA_PepeDetective:1272936556054970408> **CRYPTO PRICES :-**
<:RULES_RULES:1272972421011607552> **Ltc Price In Usd** :- `.ltcprice`
<:RULES_RULES:1272972421011607552> **Btc Price In Usd** :- `.btcprice`
<:RULES_RULES:1272972421011607552> **Sol Price In Usd** :- `.solprice`
<:RULES_RULES:1272972421011607552> **Usdt Price In Usd** :- `.usdtprice`''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}CRYPTO PRICES✅ ")
    
@siddhu.command()
async def checkpromo(ctx, *, promo_links):
    await ctx.message.delete()
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code, ctx)
                await ctx.send(result)
            else:
                await ctx.send(f'**INVALID LINK** : `{link}`')

async def check_promo(session, promo_code, ctx):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'**Code:** {promo_code}\n**Status:** ALREADY CLAIMED'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return (f'**Code:** {promo_code}\n'
                        f'**Expiry Date:** {days} days\n'
                        f'**Expires At:** {exp_at}\n'
                        f'**Title:** {title}')
                
        elif response.status == 429:
            return '**RARE LIMITED**'
        else:
            return f'**INVALID CODE** : `{promo_code}`'

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code

deleted_messages = {}

@siddhu.event
async def on_message_delete(message):
    if message.guild:
        if message.channel.id not in deleted_messages:
            deleted_messages[message.channel.id] = deque(maxlen=5)  # Store up to 5 messages

        deleted_messages[message.channel.id].append({
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at
        })

@siddhu.command()
async def snipe(ctx):
    await ctx.message.delete()
    channel_id = ctx.channel.id
    if channel_id in deleted_messages and deleted_messages[channel_id]:
        messages = deleted_messages[channel_id]
        for msg in messages:
            timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f'''### Snipped Deleted Message
{timestamp} | Message Content : `{msg["content"]}`

Message sent By `{msg['author']}`''')
    else:
        await ctx.send("<a:Diamonds:1272969331596198010> No messages to snipe in this channel.")
        
@siddhu.command()
async def checktoken(ctx , tooken):
    await ctx.message.delete()
    headers = {
        'Authorization': tooken
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user_info = r.json()
        await ctx.send(f'''### Token Checked Succesfully
              - **Valid Token **
              - **Username : `{user_info["username"]}`**
              - **User Id : `{user_info["id"]}`**
              - **Email : `{user_info["email"]}`**
              - **Verifed? `{user_info["verified"]}`**
              ''')
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TOKEN CHECKED✅ ")
    else:
        await ctx.send("<a:Diamonds:1272969331596198010> Invalid Token or Locked or flagged")
        
translator = Translator()

@siddhu.command()
async def translate(ctx, *, text: str):
    await ctx.message.delete()
    try:
        detection = translator.detect(text)
        source_language = detection.lang
        source_language_name = LANGUAGES.get(source_language, 'Unknown language')

        translation = translator.translate(text, dest='en')
        translated_text = translation.text

        response_message = (
            f"**Original Text:** {text}\n"
            f"**Detected Language:** {source_language_name} ({source_language})\n"
            f"**Translated Text:** {translated_text}"
        )

        await ctx.send(response_message)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MSG TRANSLATED✅ ")

    except Exception as e:
        await ctx.send("<a:Diamonds:1272969331596198010> **Error**: Could not translate text. Please try again later.")
        
@siddhu.command()
async def avatar(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        await ctx.send(user.avatar_url)
    except:
        await ctx.send("<a:Diamonds:1272969331596198010> User Don't Have Avatar")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AVATAR✅ ")
        
@siddhu.command()
async def banner(ctx, user: discord.User):
    await ctx.message.delete()
    banner_url = user.banner_url
    if banner_url:
        await ctx.send(banner_url)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}BANNER✅ ")
    else:
        await ctx.send("<a:Diamonds:1272969331596198010> This user does not have a banner.")

@siddhu.command()
async def icon(ctx):
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon_url if ctx.guild.icon else "<a:Diamonds:1272969331596198010> No server icon"
    await ctx.send(server_icon_url)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ICON ✅ ")

@siddhu.command()
async def get_image(ctx, query):
    await ctx.message.delete()
    params = {
        "query": query,
        'per_page': 1,
        'orientation': 'landscape'
    }
    headers = {
        'Authorization': f'Client-ID F1kSmh4MALfMKjHRxk38dZmPEV0OxsHdzuruBS_Y7to'
    }
    try:
        r = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            await ctx.send(f"Here is your image for `{query}`:\n{image_url}")
            print("Successfully Generated Image")
        else:
            await ctx.send('No images found.')
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        await ctx.send(f"`Error fetching image: {e}`")

@siddhu.command()
async def sc(ctx, category_id: int, *, message: str):
    await ctx.message.delete()
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server.")
        return

    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category is None:
        await ctx.send("Category not found.")
        return

    if category_id in active_tasks:
        await ctx.send("A message task is already running for this category. Please stop it first using `.stopmsg`.")
        return

    category_messages[category_id] = message
    active_tasks[category_id] = True

    await ctx.send(f"**Sending Msg In Ticket Create Category Id: {category.name}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY SET ✅ ")

@siddhu.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        category_id = channel.category_id
        if category_id in active_tasks and active_tasks[category_id]:
            await asyncio.sleep(1)  # Optional delay before sending the message
            await channel.send(category_messages[category_id])

@siddhu.command()
async def stopsc(ctx, category_id: int):
    await ctx.message.delete()
    if category_id not in active_tasks:
        await ctx.send("No message task is running for this category.")
        return

    active_tasks[category_id] = False
    await ctx.send(f"**Stopped Sending Msg In Ticket Create Category Id: {category_id}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY REMOVED ✅ ")
    
siddhu.load_extension("afk")

siddhu.run(token, bot=False)