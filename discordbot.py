import discord
import dotenv
import os

dotenv.load_dotenv()
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1139173944386125846)
    await channel.send("Hello! My name is Botbot, your personal AI assistant. Ask me anything.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(DISCORD_API_TOKEN)
