# bot.py
import os
import sys
from io import StringIO
import discord
from dotenv import load_dotenv
from discord.ext import commands
from enesy import get_current_games, get_recent_game
from player_db import try_get_player_id, try_remove_player_id, try_add_player

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='mystats')
async def on_get_mystats(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return 
    
    recent_game_response = get_recent_game(player_id)
    await command.channel.send(recent_game_response.get_player_output(player_id))
    
@bot.command(name='wer')
async def on_get_wer(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return 
    
    recent_game_response = get_recent_game(player_id)
    await command.channel.send(recent_game_response.get_player_wer_output(player_id))
    
@bot.command(name='gamestats')
async def on_get_gamestats(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return 
    
    recent_game_response = get_recent_game(player_id)
    await command.channel.send(recent_game_response.get_output())

@bot.command(name='blame')
async def on_get_elo(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return
    
    recent_game_response = get_recent_game(player_id)
    await command.channel.send(recent_game_response.get_worst_player_output(player_id))

@bot.command(name='carry')
async def on_get_elo(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return
    
    recent_game_response = get_recent_game(player_id)
    await command.channel.send(recent_game_response.get_best_player_output(player_id))
    
@bot.command(name='games')
async def on_get_games(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await command.channel.send(f'Not Registered')
        return
    
    current_games_response = get_current_games(player_id)
    # TODO

@bot.command(name='unregister')
async def on_unregister(command):
    if try_get_player_id(command.author) is None:
        await command.channel.send(f'Not Registered')
        return
        
    if try_remove_player_id(command.author):
        await command.channel.send(f'Unregistered')
    else:
        await command.channel.send(f'Failed to Unregister')
        
@bot.command(name='register')
async def on_unregister(command):
    if try_get_player_id(command.author):
        await command.channel.send(f'Already Registered')
        return
    
    if try_add_player(command.author, command.message.content[10:]):
        await command.channel.send('Registered')
    else:
        await command.channel.send('Failed to Register')

bot.run(TOKEN)