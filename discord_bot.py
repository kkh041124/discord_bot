import discord
from discord.ext import commands

TOKEN = 'TOKEN'
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'봇이 로그인했습니다: {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '안녕':
        await message.channel.send('안녕하세요')
@bot.event
async def on_typing(channel, user, when):
    await channel.send(str(user)+"이 작성중!")
    return
bot.run(TOKEN)