import discord
from instatools import Intsatools
from urllib.parse import urlparse
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)

instatools = Intsatools("sikocak221","LutfiAN32!")

@bot.event
async def on_ready():
    print(f'\n{Style.DIM}{Back.RED}{bot.user}{Back.RESET}{Style.NORMAL} is connected to the following server(s):\n')
    for server in bot.guilds:
        print(f'{Style.DIM}[{Style.NORMAL}{Fore.GREEN}+{Fore.RESET}{Style.DIM}]{Style.NORMAL} {server.name} ({Style.DIM}{Fore.BLUE}{server.id}{Style.NORMAL}{Fore.RESET})')
    print("")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"{Style.DIM}[{Style.NORMAL}{Fore.GREEN}{message.guild.name}{Fore.RESET}{Style.DIM}]{Style.NORMAL} {message.author}'s sent message {Fore.RESET}{Style.DIM}>>{Style.NORMAL} {message.content}")
    try:
        result = urlparse(message.content)
        if "instagram" in result.netloc and '/reel/' in result.path:
            caption, link_download = instatools.download_reels(message.content)
            if caption is not None and link_download is not None:
                await message.channel.send(f'{caption}\n[Download]({link_download})')
            else:
                await message.channel.send(f'# Video Not Found')
        elif message.content.startswith('!reply'):
            if message.mentions:
                mentioned_user = message.mentions[0]
                content_without_mention = message.content.replace(
                    f'!reply {mentioned_user.mention}', '')
                await mentioned_user.send(f'You said: {content_without_mention}')
            else:
                await message.channel.send('Please mention a user to reply to.')

    except ValueError:
        pass

bot.run('TOKEN_IS_HERE')
