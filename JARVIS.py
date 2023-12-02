import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup

last_scraped_title = ""

intents = discord.Intents.all()
TOKEN = 'TOKE'
GUILD_ID = "Guild ID"
CHANNEL_ID = "Channel ID"
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=CHANNEL_ID)
    news_sender.start(channel)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '안녕':
        await message.channel.send('안녕하세요')

    # Check if the message is the command "/공지사항"
    if message.content.startswith('/공지사항'):
        channel = message.channel
        new_scraped_news = scrape_news()
        await send_news(channel, new_scraped_news)

@tasks.loop(minutes=360)
async def news_sender(channel):
    global last_scraped_title
    new_scraped_news = scrape_news()

    new_scraped_title = new_scraped_news["title"][0]
    if new_scraped_news != last_scraped_title:
        print(f"[New!]{new_scraped_title}")
        last_scraped_title = new_scraped_title

def scrape_news():
    baseurl = 'https://www.seoultech.ac.kr/service/info/notice/'
    resp = requests.get(baseurl)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.select('.body_tr a')

    title = []
    url = []

    for n in news:
        title.append(n.text.strip())
        url.append(n['href'].strip())

    return {"baseurl": baseurl, "title": title, "url": url}

async def send_news(channel, news):
    for i in range(len(news["title"])):
        link = news["title"][i]
        link_desc = news["baseurl"]
        link_href = news["url"][i]
        news_info = f'공지사항 : {link}\n- 원본 링크 : {link_desc}\n- 공지사항 링크 : {link_desc+link_href}'
        await channel.send(news_info)

bot.run(TOKEN)
