import os
import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands
from music_functions import *


# Security
load_dotenv()

# Define intents 
intents = discord.Intents.all()
intents.typing = True
intents.presences = True
intents.messages = True

# The Bot first steps
bot = commands.Bot(command_prefix='!', intents=intents)

# # Store music queue and loop status if necessary
# queue = []
# loop = False

# # Function to join voice channel
# async def join_channel(ctx):
#     try:
#         if ctx.author.voice is None or ctx.author.voice.channel is None:
#             await ctx.send("You need to be in a voice channel to use this command.")
#             return None
#         voice_channel = ctx.author.voice.channel
#         if ctx.voice_client is not None:
#             await ctx.voice_client.move_to(voice_channel)
#         else:
#             await voice_channel.connect()
#         return ctx.voice_client
#     except Exception as e:
#         await ctx.send(f"An error occurred while joining the voice channel: {str(e)}")

# # Function to play music
# async def play_music(ctx, url):
#     try:
#         voice_client = await join_channel(ctx)
#         if voice_client:
#             global queue
#             if not isinstance(queue, list):
#                 queue = []
#             queue.append(url)
#             if not voice_client.is_playing() and not voice_client.is_paused() and len(queue) == 1:
#                 await play_next(ctx)
#     except Exception as e:
#         await ctx.send(f"An error occurred while playing the music: {str(e)}")

# #Function to stop music
# async def stop_music(ctx):
#     try:
#         voice_client = ctx.voice_client
#         if voice_client:
#             if voice_client.is_playing():
#                 voice_client.stop()
#             queue.clear()
#     except Exception as e:
#         await ctx.send(f"An error occurred while stopping the music: {str(e)}")

# # Function to play next song
# async def play_next(ctx):
#     try:
#         global queue
#         voice_client = ctx.voice_client
#         if len(queue) > 0:
#             url = queue.pop(0)
#             with youtube_dl.YoutubeDL({}) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 url2 = info['formats'][0]['url']
#             voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: play_next(ctx))
#             await ctx.send(f"Now playing: {info['title']}")
#         elif loop:
#             await play_music(ctx, url)  # If looping, play the same song again
#         else:
#             await voice_client.disconnect()
#             queue = []  # Clear the queue when disconnecting
#     except Exception as e:
#         await ctx.send(f"An error occurred while playing the next song: {str(e)}")

# Command to join voice channel
@bot.command()
async def join(ctx):
    try:
        await join_channel(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred while joining the voice channel: {str(e)}")

# Command to play + search music
@bot.command()
async def play(ctx, *, query):
    try:
        await play_music(ctx, query)
    except Exception as e:
        await ctx.send(f"An error occurred while playing the voice channel: {str(e)}")

# Command to pause music
@bot.command()
async def pause(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.pause()
    except Exception as e:
        await ctx.send(f"An error occurred while pausing the music: {str(e)}")

# Command to resume music
@bot.command()
async def resume(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()
    except Exception as e:
        await ctx.send(f"An error occurred while resuming the music: {str(e)}")

# Command to stop music
@bot.command()
async def stop(ctx):
    try:
        await stop_music(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the music: {str(e)}")

# Command to stop and disconnect the bot from voice channel
@bot.command()
async def leave(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            queue = [] # Clear the queue when disconnecting
    except Exception as e:
        await ctx.send(f"An error occurred while leaving the voice channel: {str(e)}")

# Command to show current playing queue
@bot.command()
async def queue(ctx):
    try:
        global queue  # Indicando que 'queue' é uma variável global
        if len(queue) > 0:
            await ctx.send("Current queue:")
            for index, url in enumerate(queue):
                await ctx.send(f"{index + 1}: {url}")
        else:
            await ctx.send("Queue is empty.")
    except Exception as e:
        await ctx.send(f"An error occurred while showing the queue: {str(e)}")

# Command to toggle loop
@bot.command()
async def loop(ctx):
    try:
        global loop
        loop = not loop
        if loop:
            await ctx.send("Looping enabled.")
        else:
            await ctx.send("Looping disabled.")
    except Exception as e:
        await ctx.send(f"An error occurred while toggling loop: {str(e)}")

# Command to display help
@bot.command(name='commands')
async def show_commands(ctx):
    try:
        embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
        embed.add_field(name="!join", value="Makes the bot join the voice channel.", inline=False)
        embed.add_field(name="!play [url]", value="Plays a song from the given URL.", inline=False)
        embed.add_field(name="!pause", value="Pauses the currently playing song.", inline=False)
        embed.add_field(name="!resume", value="Resumes the paused song.", inline=False)
        embed.add_field(name="!leave", value="Stops the music and disconnects the bot from the voice channel.", inline=False)
        embed.add_field(name="!queue", value="Displays the current music queue.", inline=False)
        embed.add_field(name="!loop", value="Toggles looping on/off.", inline=False)
        embed.add_field(name="!commands", value="Displays this help message.", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred while displaying help: {str(e)}")

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run bot
bot.run(os.getenv('DISCORD_TOKEN'))