import discord
import keys

client = discord.Client()
global msg


@client.event
async def on_ready():
    global msg
    await client.get_channel(keys.CHANNEL_ID).send(msg)
    await client.close()


def send_message(message):
    global msg
    msg = message
    client.run(keys.BOT_TOKEN)
