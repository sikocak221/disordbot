import discord
from discord.ext import commands
import youtube_dl

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!')

# Check if the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Command to join a voice channel
@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

# Command to leave a voice channel
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

# Command to play music from YouTube
@bot.command()
async def play(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

    voice_channel = ctx.message.author.voice.channel
    voice_client = ctx.voice_client

    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))
        await ctx.send(f'Now playing: {info["title"]}')
    else:
        await ctx.send('The bot is already playing music.')

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')
