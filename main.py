import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from rank import Rank
from match import Match
from match_summary import MatchSummary
from http_requests import get_recent_game_response, get_recent_game_diaboticool_url, get_rank_response, get_all_recent_games_response, get_match_response, get_current_games
from player_db import try_get_player_id, try_remove_player_id, try_add_player, try_get_all_player_id, try_add_all_player
from queue_db import add_to_queue, get_queue_status, remove_from_queue
from discord_formatter import send_in_codeblock, get_match_from_command, get_player_from_command
import time

from team import Team

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

@bot.command(name='recent')
async def get_recent_data(command):
    player_id = try_get_player_id(command.author)
    if player_id is None:
        await send_in_codeblock(command, f'Not Registered')
        return
    
    match_count = get_match_from_command(command)
    
    limit = 10
    if match_count == 0:
        limit = match_count
    
    count = 0
    match_summaries: list[MatchSummary] = []
    for match_id in get_all_recent_games_response(player_id):
        match = Match(get_match_response(match_id))
        team: Team = match.get_team_for_player(player_id)
        list_player_rank_data = team.get_player_rank_data()
        
        is_win = team.won
        match_summary = MatchSummary(is_win, list(filter(lambda t: t.player_id == player_id, list_player_rank_data))[0], list(filter(lambda t: t.player_id != player_id, list_player_rank_data)))
        match_summaries.append(match_summary)
        time.sleep(1)
        
        count = count + 1
        if count == limit:
            break
        
    
    match_summary_wins = list(filter(lambda t: t.is_win == True, match_summaries))
    match_summary_losses = list(filter(lambda t: t.is_win == False, match_summaries))
    
    # WER +/- Per Win
    wer_plus_minus_per_win = sum(map(lambda t: t.plus_minus, match_summary_wins)) / len(match_summary_wins)
    # WER +/- Per Loss
    wer_plus_minus_per_loss = sum(map(lambda t: t.plus_minus, match_summary_losses)) / len(match_summary_losses)
    # WER Average Per Win
    wer_average_per_win = sum(map(lambda t: t.wer, match_summary_wins)) / len(match_summary_wins)
    # WER Average Per Loss
    wer_average_per_loss = sum(map(lambda t: t.wer, match_summary_losses)) / len(match_summary_losses)
    # WER Best
    wer_best = sorted(match_summaries, key=lambda t: t.wer, reverse=True)[0].wer
    # WER Worst
    wer_worst = sorted(match_summaries, key=lambda t: t.wer, reverse=False)[0].wer
    # WER +/- Best
    wer_plus_minus_best = sorted(match_summaries, key=lambda t: t.plus_minus, reverse=True)[0].plus_minus
    # WER +/- Worst
    wer_plus_minus_worst = sorted(match_summaries, key=lambda t: t.plus_minus, reverse=False)[0].plus_minus
    # WER +/- Lopsided W
    wer_plus_minus_lop_w = sorted(match_summary_wins, key=lambda t: t.plus_minus, reverse=False)[0].plus_minus
    # WER +/- Lopsided L
    wer_plus_minus_lop_l = sorted(match_summary_losses, key=lambda t: t.plus_minus, reverse=True)[0].plus_minus
    
    await send_in_codeblock(command, f'''
W/L:                    {len(match_summary_wins)} / {len(match_summary_losses)}
WER +/- Per Win:        {round(wer_plus_minus_per_win, 1)}
WER +/- Per Loss:       {round(wer_plus_minus_per_loss, 1)}
WER Average Per Win:    {round(wer_average_per_win, 1)}
WER Average Per Loss:   {round(wer_average_per_loss, 1)}
WER Best:               {round(wer_best, 1)}
WER Worst:              {round(wer_worst, 1)}
WER +/- Best:           {round(wer_plus_minus_best, 1)}
WER +/- Worst:          {round(wer_plus_minus_worst, 1)}
WER +/- Lopsided W:     {round(wer_plus_minus_lop_w, 1)}
WER +/- Lopsided L:     {round(wer_plus_minus_lop_l, 1)}
''')
  
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

@bot.command(name='status')
async def on_status(command):
    data = get_current_games()

    warmups = list(filter(lambda t: t.state == 1, data.customs))
    actives = list(filter(lambda t: t.state == 2, data.customs))

    others = list(filter(lambda t: t.state != 1 and t.state != 2, data.customs))

    if len(others) > 0:
        pass

    hasWarmups = len(warmups) > 0
    hasActives = len(actives) > 0
    hasPickups = len(data.pickups) > 0

    strs = []

    if not hasWarmups and not hasActives and not hasPickups:
        await send_in_codeblock(command, 'No players online')
        return

    if hasActives:
        strs.append('-----------------------------Active----------------------------- \n')

        for game in actives:
            strs += getGameStrings(game)

    if hasWarmups:
        strs.append('-----------------------------Warmups----------------------------- \n')

        for game in warmups:
            strs += getGameStrings(game)

    if hasPickups:
        strs.append('-----------------------------Pickups----------------------------- \n')

        for pickup in data.pickups:
            strs.append(f'Mode: {pickup.mode.upper()}')
            strs.append(f'{len(pickup.users)} / {pickup.team_size * pickup.team_count}')
            strs.append(f'Players: {', '.join(map(lambda t: t.name, pickup.users))}')
            strs.append(f'\n')

    await send_in_codeblock(command, ' \n'.join(strs))

def getGameStrings(game):
    strs = []
    strs.append(f'Mode: {game.mode.upper()} Map: {game.map.upper()}')
    for team_id in list(set((map(lambda t: t.team_id, game.clients)))):
        strs.append(f'Team {team_id}: {', '.join(map(lambda t: t.name, filter(lambda t: t.team_id == team_id, game.clients)))}')
    strs.append(f'Score: {' - '.join(map(lambda t: f'{game.team_scores.__dict__[t]}', game.team_scores.__dict__.keys()))}')
    strs.append(f'\n')
    return strs

@bot.command(name='help')
async def on_get_help(command):
    await send_in_codeblock(command, f"""-----------------------------o_HOTHEAD_o's Diabotical Help Menu-----------------------------
!blame          - Displays the stats of the 'packetdog' on your team
!carry          - Displays the stats of the player that carried
!cool           - Gets the Diabotical.cool link
!dequeue        - Dequeues player from Queue
!enqueue        - Queues for the next n Hours ex: "!enqueue 5"
!help           - You know what this does
!match          - Displays summary stats
!mymatch        - Displays your full stats of match
!player         - Displays another player's last match stats
!queue          - Gets the Queue Status for the next n Hours ex: "!queue 5"
!register       - Register using your player id (Can obtain through Diabotical.cool site). Place your id after register ex: "!register c9a979c899d64c6cb7bdd2dc3d815a04"
!status         - Displays the current server status
!unregister     - Can remove self to re-add or whatever
!wer            - Displays the rankings and relative scores""")

@bot.command(name='enqueue')
async def on_enqueue(command):
    hours = get_match_from_command(command)
    if hours == 0:
        hours = 1
    add_to_queue(command.author, hours)

    queueStatus = get_queue_status(hours)

    await send_in_codeblock(command, str(queueStatus))

@bot.command(name='queue')
async def on_queue(command):
    hours = get_match_from_command(command)
    if hours == 0:
        hours = 1
    queueStatus = get_queue_status(hours)

    await send_in_codeblock(command, str(queueStatus))

@bot.command(name='dequeue')
async def on_queue(command):
    remove_from_queue(command.author)
    await send_in_codeblock(command, f'Removed {command.author} from Queue')

def add_all_players(match: Match):
    for player in match.team_1.players:
        try_add_all_player(player.name, player.player_id)
    for player in match.team_2.players:
        try_add_all_player(player.name, player.player_id)

bot.run(TOKEN)

#    TODO: ALL WER/RATINGS