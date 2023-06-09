import discord # pip install discord.py
from discord import app_commands

import asyncio
import os
import sys
import time
import requests #pip install requests
import numpy as np
import pickle

import Functions.second_to_hhmmss as STH
import Functions.PickRandom
from Functions.crawl_today_menu import today_menu
from Chat_OpenAI import get_chat # pip install openai
from Image_PyKakao import generate_image # pip install PyKakao
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




# General Information Command
@tree.command(name="info", description="General Information", 
              guild=discord.Object(id=1102965191580332092))
async def info(interaction: discord.Interaction) -> None:
    """Sends general information of Huyuko
    
    Args:
        interaction (discord.Interaction): Interaction
    """
    await interaction.response.send_message(f"CNUCSE23 bot ver. {version}, developed by CNUCSE23")

# Uptime Command
@tree.command(name= "uptime", description="returns uptime of AI Huyuko bot",
              guild=discord.Object(id=1102965191580332092))
async def uptime(interaction: discord.Interaction) -> None:
    """Sends Uptime
    
    Args:
        interaction (discord.Interaction): Interaction
    """
    second = int(time.time()-start_time)
    sth = STH.format_seconds_to_hhmmss(seconds=second)
    await interaction.response.send_message("uptime: "+ str(sth))

# Weather Command
@tree.command(name = "날씨", description="유성구의 날씨 정보를 보내드립니다",
              guild=discord.Object(id=1102965191580332092))
async def weather(interaction: discord.Interaction) -> None:
    """Sends current weather
    
    Args:
        interaction (discord.Interaction): _description_
        city (str): _description_
    """
    api_key = "340c5633e643b9e3390c96873b6791aa"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + "Daejeon"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_celsiuis = str(round(current_temperature - 273.15))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        weather_description = z[0]["description"]
        embed = discord.Embed(title=f"대전의 날씨입니당",
                            color=interaction.guild.me.top_role.color,)
                            # timestamp=interaction.message.created_at,)
        embed.add_field(name="날씨",
                        value=f"**{weather_description}**", inline=False)
        embed.add_field(name="기온(C)",
                        value=f"**{current_temperature_celsiuis}°C**", inline=False)
        embed.add_field(name="습도(%)",
                        value=f"**{current_humidity}%**", inline=False)
        embed.add_field(name="기압(hPa)",
                        value=f"**{current_pressure}hPa**", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("영어로 도시이름을 다시 쳐주세요...ㅠ")

# Crawl Today's Menu
@tree.command(name = "학식", description="오늘의 학식 정보를 알려드립니다",
              guild=discord.Object(id=1102965191580332092))
@app_commands.choices(arg1=[
    app_commands.Choice(name='아침', value='breakfast'),
    app_commands.Choice(name='점심', value='launch'),
    app_commands.Choice(name='저녁', value='dinner')
])
@app_commands.choices(arg2=[
    app_commands.Choice(name='학생', value='student'),
    app_commands.Choice(name='직원', value='staff')
])
@app_commands.choices(arg3=[
    app_commands.Choice(name='2학', value='2'),
    app_commands.Choice(name='3학', value='3'),
    app_commands.Choice(name='4학', value='4')
])
async def Food(interaction = discord.Interaction, *,
               arg1:app_commands.Choice[str],
               arg2:app_commands.Choice[str],
               arg3:app_commands.Choice[str]):
    menu = today_menu(arg1.value, arg2.value, arg3.value)
    await interaction.response.send_message(str(menu))

# Roll dice
@tree.command(name = "주사위", description="주사위를 굴려드립니당",
              guild=discord.Object(id=1102965191580332092))
async def roll_dice(interaction: discord.Interaction) -> None:
    """Rolls dice and returns a random number between 1 and 6
    
    Args:
        interaction (discord.Interaction): Interaction
    """
    dice = Functions.PickRandom.roll_dice()
    await interaction.response.send_message(dice)

# Restarting Command
def restart_bot():
    """Restart bot.py
    """
    os.execv(sys.executable, ['python'] + sys.argv)
@tree.command(name="restart", description="restart bot",
              guild=discord.Object(id=1102965191580332092))
async def restart(Interaction: discord.Interaction) -> None:
    """Command for Restarting Huyuko bot

    Args:
        Interaction (discord.Interaction): Interaction
    """
    await Interaction.response.send_message("Restarting bot...")
    restart_bot()

@tree.command(name="이미지", description='이미지를 생성해드립니다',
              guild=discord.Object(id=1102965191580332092))
async def image(Interaction:discord.Interaction, *, query:str) -> None:
    generate_image(query)
    with open('my_image.png', 'rb') as f:
        picture = discord.File(f)
        await Interaction.channel.send(file=picture)

@client.event
async def on_ready():
    """
    activated when bot is online
    """
    print('We have logged in as {}'.format(client))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    
    await tree.sync(guild=discord.Object(id=1102965191580332092))
    log_channel = client.get_channel(1107199193967247400)
    await log_channel.send('Online!')

    global start_time
    start_time = time.time()


@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'{member.mention}님 {guild.name}에 어서오세요!'
        await guild.system_channel.send(to_send)

@client.event
async def on_message(message:discord.message) -> None:
    if message.author == client.user:
        return
    if message.mentions:
        if message.mentions[0].id == 1110448602087686154:
            result = get_chat(message.content)
            await message.channel.send(result)

client.run(Discord_Token)