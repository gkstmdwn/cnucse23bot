import discord # pip install discord.py
from discord import app_commands

import asyncio
import os
import sys
import time
import requests #pip install requests
import numpy as np
import genshin as genshin # pip install genshin
import pickle

from token_1 import Discord_Token

# python 3.8 or higher
# discordpy 2.2.0

version = "1.0.0"
discord_token = Discord_Token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)





@tree.command(name="info", description="General Information", 
              guild=discord.Object(id=1110447281011961856))
async def info(interaction: discord.Interaction) -> None:
    """Sends general information of Huyuko
    
    Args:
        interaction (discord.Interaction): Interaction
    """
    await interaction.response.send_message(f"Huyuko bot ver. {version}, developed by CNUCSE23")





@client.event
async def on_ready():
    """activated when bot is online
    """
    print('We have logged in as {}'.format(client))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    
    await tree.sync(guild=discord.Object(id=1110447281011961856))
    log_channel = client.get_channel(1110447281011961859)  # '로그'Channel
    await log_channel.send('Online!')

    global start_time
    start_time = time.time()


@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'{member.mention}님 {guild.name}에 어서오세요!'
        await guild.system_channel.send(to_send)












client.run(Discord_Token)