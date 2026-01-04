import discord
import requests
from bs4 import BeautifulSoup
import asyncio

TOKEN = ""  # pozostaw puste, token wstawimy w Railway
CHANNEL_ID = 0  # tu później wstawisz ID kanału

SEARCH_TERMS = [
    "iphone 13",
    "iphone 13 pro",
    "iphone 13 pro max",

    "iphone 14",
    "iphone 14 plus",
    "iphone 14 pro",
    "iphone 14 pro max",

    "iphone 15",
    "iphone 15 pro",
    "iphone 15 pro max",

    "iphone 16",
    "iphone 16 pro",
    "iphone 16 pro max"
]

checked_links = set()

async def check_olx(client):
    global checked_links
    while True:
        for term in SEARCH_TERMS:
            url = f"https://www.olx.pl/oferty/q-{term.replace(' ', '-')}/?search%5Bfilter_float_price%3Ato%5D=1500"
            html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
            soup = BeautifulSoup(html, "html.parser")

            offers = soup.select("a.css-rc5s2u")
            for o in offers:
                link = "https://www.olx.pl" + o["href"]

                if link in checked_links:
                    continue
                checked_links.add(link)

                title = o.get_text(strip=True)

                embed = discord.Embed(
                    title=title,
                    description=f"[Kliknij, aby zobaczyć ofertę]({link})",
                    color=0x00ff00
                )

                channel = client.get_channel(CHANNEL_ID)
                await channel.send(embed=embed)

        await asyncio.sleep(60)

class MyClient(discord.Client):
    async def on_ready(self):
        self.loop.create_task(check_olx(self))

intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)
