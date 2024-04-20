import discord 
import youtube_dl
import asyncio

# Store music queue and loop status if necessary
queue = []
loop = False

# Function to join voice channel
async def join_channel(ctx):
    try:
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return None
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()
        return ctx.voice_client
    except Exception as e:
        await ctx.send(f"An error occurred while joining the voice channel: {str(e)}")

# Function to play music
# Function to play music
async def play_music(ctx, query):
    try:
        # Check if the query is a valid URL
        if not (query.startswith("http://") or query.startswith("https://")):
            # If not a valid URL, perform a search
            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in info:
                    first_video = info['entries'][0]
                    url = first_video['url']
                    await ctx.send(f"Tocando agora: {first_video['title']}")
                else:
                    await ctx.send("Unable to find the song.")
                    return
        else:
            url = query

        # Play the music
        voice_client = await join_channel(ctx)
        if voice_client:
            global queue
            if not isinstance(queue, list):
                queue = []
            queue.append(url)
            if not voice_client.is_playing() and not voice_client.is_paused() and len(queue) == 1:
                await play_next(ctx)
    
        # Return title and duration
        return first_video['title'], first_video['duration'] if 'first_video' in locals() else None
    except Exception as e:
        await ctx.send(f"An error occurred while playing the music: {str(e)}")
        return None, None

# Function to stop music
async def stop_music(ctx):
    global queue  # Declare queue as global
    try:
        voice_client = ctx.voice_client
        if voice_client:
            if voice_client.is_playing():
                voice_client.stop()
            queue = []  # Clear the queue
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the music: {str(e)}")

# Function to play next song
async def play_next(ctx):
    global loop
    try:
        global queue
        voice_client = ctx.voice_client
        if len(queue) > 0:
            url = queue.pop(0)
            with youtube_dl.YoutubeDL({}) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: play_next(ctx))
            await ctx.send(f"Now playing: {info['title']}")
        elif loop:
            await play_music(ctx, url)  # If looping, play the same song again
        else:
            await voice_client.disconnect()
            queue = []  # Clear the queue when disconnecting
    except Exception as e:
        await ctx.send(f"An error occurred while playing the next song: {str(e)}")

