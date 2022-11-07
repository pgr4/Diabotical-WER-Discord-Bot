import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from rank import Rank
from match import Match
from enesy import get_current_games, get_recent_game_response, get_recent_game_diaboticool_url, get_rank_response
from player_db import try_get_player_id, try_remove_player_id, try_add_player
from discord_formatter import send_in_codeblock

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='mystats')
async def on_get_mystats(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_player_output(player_id))
    
@bot.command(name='wer')
async def on_get_wer(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_player_wer_output(player_id))

@bot.command(name='wer*')
async def on_get_wer(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_player_wer_adjusted_output(player_id))

@bot.command(name='allwer')
async def on_get_wer(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_all_players_wer_adjusted_output())

@bot.command(name='gamestats')
async def on_get_gamestats(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return 
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_output())

@bot.command(name='blame')
async def on_get_blame(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_worst_player_output(player_id))

@bot.command(name='carry')
async def on_get_carry(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_best_player_output(player_id))

@bot.command(name='carry*')
async def on_get_carry(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_best_player_adjusted_output(player_id))
    
@bot.command(name='blame*')
async def on_get_carry(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    recent_game_response = Match(get_recent_game_response(player_id))
    await send_in_codeblock(command, recent_game_response.get_worst_player_adjusted_output(player_id))
    
@bot.command(name='games')
async def on_get_games(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    current_games_response = get_current_games(player_id)
    # TODO

@bot.command(name='cool')
async def on_get_cool(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    await send_in_codeblock(command, f'<{get_recent_game_diaboticool_url(player_id)}>')

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
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    await send_in_codeblock(command, f"""-----------------------------o_HOTHEAD_o's Diabotical Help Menu-----------------------------
!allwer         - Displays all players Ratings and WER scores
!blame*         - Displays the stats of the 'packetdog' on your team last match
!carry*         - Displays the stats of the player that carried your team last match
!cool           - Gets the Diabotical.cool link to your last match
!games          - [WIP] Displays the status of all the current games
!gamestats      - Displays all player stats from your last match
!help           - You know what this does
!mystats        - Displays full stats from your last match
!register xxxxx - Register using your player id (Can obtain through Diabotical.cool site) 
!unregister     - Can remove self to re-add or whatever
!wer*           - Displays your WER score of the last match""")
    
bot.run(TOKEN)

#    TODO: ALL WER/RATINGS