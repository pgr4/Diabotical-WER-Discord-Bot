import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from rank import Rank
from match import Match
from http_requests import get_recent_game_response, get_recent_game_diaboticool_url, get_rank_response
from player_db import try_get_player_id, try_remove_player_id, try_add_player, try_get_all_player_id, try_add_all_player
from discord_formatter import send_in_codeblock, get_match_from_command, get_player_from_command

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='wer')
async def on_get_wer(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id, get_match_from_command(command)))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_all_players_wer_adjusted_output())

@bot.command(name='match')
async def on_get_match(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id, get_match_from_command(command)))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_match_summary_output())

@bot.command(name='mymatch')
async def on_get_mymatch(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id, get_match_from_command(command)))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_match_detail_for_player(player_id))
    
@bot.command(name='player')
async def on_get_player_match(command):
    player_id = try_get_all_player_id(get_player_from_command(command))
    if player_id is None:
        await send_in_codeblock(command, f'Player Not Found')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id, 0))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_match_summary_output())

@bot.command(name='carry')
async def on_get_carry(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id, get_match_from_command(command)))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_best_player_adjusted_output(player_id))
    
@bot.command(name='blame')
async def on_get_carry(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id, get_match_from_command(command)))
    add_all_players(recent_game_response)
    await send_in_codeblock(command, recent_game_response.get_worst_player_adjusted_output(player_id))

@bot.command(name='cool')
async def on_get_cool(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    await send_in_codeblock(command, get_recent_game_diaboticool_url(player_id, get_match_from_command(command)))

@bot.command(name='rank')
async def on_get_rank(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    await send_in_codeblock(command, Rank(get_rank_response(player_id)).get_output())
        
@bot.command(name='unregister')
async def on_unregister(command):
    if try_get_player_id(command.author) is None:
        await send_in_codeblock(command, f'Not Registered')
        return
        
    if try_remove_player_id(command.author):
        await send_in_codeblock(command, f'Unregistered')
    else:
        await send_in_codeblock(command, f'Failed to Unregister')
        
@bot.command(name='register')
async def on_unregister(command):
    if try_get_player_id(command.author):
        await send_in_codeblock(command, f'Already Registered')
        return
    
    if try_add_player(command.author, command.message.content[10:]):
        await send_in_codeblock(command, 'Registered')
    else:
        await send_in_codeblock(command, 'Failed to Register')    

@bot.command(name='help')
async def on_get_help(command):
    await send_in_codeblock(command, f"""-----------------------------o_HOTHEAD_o's Diabotical Help Menu-----------------------------
!blame          - Displays the stats of the 'packetdog' on your team
!carry          - Displays the stats of the player that carried
!cool           - Gets the Diabotical.cool link
!help           - You know what this does
!match          - Displays summary stats
!mymatch        - Displays your full stats of match
!player         - Displays another player's last match stats
!register       - Register using your player id (Can obtain through Diabotical.cool site). Place your id after register ex: "!register c9a979c899d64c6cb7bdd2dc3d815a04"
!unregister     - Can remove self to re-add or whatever
!wer            - Displays the rankings and relative scores""")

def add_all_players(match: Match):
    for player in match.team_1.players:
        try_add_all_player(player.name, player.player_id)
    for player in match.team_2.players:
        try_add_all_player(player.name, player.player_id)

bot.run(TOKEN)

#    TODO: ALL WER/RATINGS