import httpx
import requests
import discord
import asyncio 
import json
from discord.ext import commands
import os
import re
from colorama import init, Fore, Style
import logging
init()

#file stuff/token stuff
folder_sb = os.path.dirname(os.path.realpath(__file__)) # checks for config.json within the file path if it is missing creates then reads from the file
json_file = os.path.join(folder_sb, 'config.json')
if os.path.exists(json_file):

    with open(json_file, 'r') as file:
        sb = json.load(file)
else:
    sb = {}

TOKEN = sb.get("TOKEN", "").strip() # checks for TOKEN within config.json if there is no TOKEN prompts the user to enter it then writes to the file
if not TOKEN:
    TOKEN = input("Enter your token >.< ")
    sb["TOKEN"] = TOKEN


    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

bot = commands.Bot(command_prefix='`', self_bot=True,) 

#nitro sniper code
coderegex = re.compile(r"(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
ready = False 

@bot.event
async def on_message(ctx):
    """checks messages for nitro gift links"""
    global ready
    if not ready:
        ready = True

    # checks messages for discord gift links
    if coderegex.search(ctx.content):
        code = coderegex.search(ctx.content).group(2)
        asyncio.create_task(redeemgiftcode(ctx.channel.id, code))    
    await bot.process_commands(ctx)  # idk what this does but it fixes all my problems so its here now ig

async def redeemgiftcode(channel_id, code): # redeems the code
    """redeems a gift code"""
    async with httpx.AsyncClient() as client:
        try:
            result = await client.post(
                f'https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem',
                json={'channel_id': str(channel_id)},
                headers={'authorization': TOKEN, 'user-agent': 'Mozilla/5.0'}
            )

            
            if result.status_code == 200:
                print('\033[32m' + 'Successfully redeemed gift code!' + '\033[0m')  # success message in pretty green
            else:
                print('\033[31m' + json.dumps(result.json(), indent=4) + '\033[0m')  # evil error message in red to show its evil
        except Exception as e:
            print('\033[31m' + f'An error occurred: {str(e)}' + '\033[0m')  # same thing as the other one in red


catart = r'''
       ,
       \`-._           __
        \\  `-..____,.'  `.
         :`.         /    \` .
         :  )       :      : \
          ;'        '   ;  |  :
          )..      .. .:.`.;  :
         /::...  .:::...   ` ;
         ; _ '    __        /: \
         `:o>   /\o_>      ;:. `.
        `-`.__ ;   __..--- /:.   \
        === \_/   ;=====_.':.     ;
         ,/'`--'...`--....        ;
              ;                    ;
            .'                      ;
          .'                        ;
        .'     ..     ,      .       ;
       :       ::..  /      ;::.     |
      /      `.;::.  |       ;:..    ;
     :         |:.   :       ;:.    ;
     :         ::     ;:..   |.    ;
      :       :;      :::....|     |
      /\     ,/ \      ;:::::;     ;
    .:. \:..|    :     ; '.--|     ;
   ::.  :''  `-.,,;     ;'   ;     ;
.-'. _.'\      / `;      \\,__:      \
`---'    `----'   ;      /    \\,.,,,/
                   `----`              nitro sniper by lawcan
'''
def printwithgradient(text):
    """prints art with a gradient"""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)
    print(Style.RESET_ALL)

printwithgradient(catart)
logging.disable()
bot.run(TOKEN,log_handler=None)


