from audio import Download
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio , Intents

intents = Intents.all()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)

# region dc_command

@client.command(pass_context = True)
async def play(ctx, url):
    """
    將機器人加入頻道中, 並將url影片放到下載佇列中處理
    """
    ctx.channel.purge(limit=1)  
    result = await join(ctx)
    if result:
        await ctx.send('downloading...')
        path = await Download(url)
        await ctx.send('download success.')
        push(ctx, path)

@client.command(pass_context = True)
async def join(ctx):
    """
    [指令]進入命令者的語音頻道
    """
    if not ctx.author.voice:
        await ctx.send('please enter a voice channel.')
        return False
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        return True
    elif voice.channel != ctx.author.voice.channel:
        await ctx.send('The bot is busy.')
        return False
    return True

@client.command(pass_context = True)
async def pause(ctx):
    """
    [指令]暫停音樂
    """
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('There is no audio playing.')

@client.command(pass_context = True)
async def resume(ctx):
    """
    [指令]繼續音樂
    """
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Audio is playing already.')

@client.command(pass_context = True)
async def skip(ctx):
    """
    [指令]切歌
    """
    guild_id = ctx.guild.id
    play_Queues[guild_id].pop(0)
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice:
        voice.stop()

# endregion

# region Audio treatment

def push(ctx, path):

    # 取得伺服器id
    guild_id = ctx.message.guild.id

    # 將音樂放入伺服器撥放佇列
    if guild_id in play_Queues:
        play_Queues[guild_id].append(path)
    else:
        play_Queues[guild_id] = [path]

    def after(guild_id, voice):

        # 如果 list 是空的，结束播放
        if not play_Queues[guild_id]:
            return
        
        # 如果有下一首歌，撥放下一首歌，不然就重複撥放
        if len(play_Queues[guild_id]) > 1:
            play_Queues[guild_id].pop(0)
        path = play_Queues[guild_id][0]

        # 播放歌曲
        source = FFmpegPCMAudio(path)
        voice.play(source, after=lambda _: after(guild_id, voice))
        return
            
    # 如果音樂還未撥放，開始撥放
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice = ctx.guild.voice_client
        path = play_Queues[guild_id][0]
        source = FFmpegPCMAudio(path)
        voice.play(source, after=lambda x: after(guild_id, voice))

# endregion

if __name__ == '__main__':
    play_Queues = {}
    token = ''
    client.run(token)
