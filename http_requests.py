import requests
import json
from types import SimpleNamespace

def convertToObject(response: requests.Response) -> any:
    return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

def makeGetRequest(url) -> any:
    return convertToObject(requests.get(url))

def get_current_games():
    response = makeGetRequest(f'https://diabotical.cool/api/v1/servers/')
    return response.data.data

def get_rank_response(player_id) -> any:
    return makeGetRequest(f'https://api.diabotical.com/api/v0/diabotical/users/{player_id}/rating')

def get_match_response(match_id) -> any:
    return makeGetRequest(f'https://diabotical.cool/api/v1/match/{match_id}').match
    
def get_recent_game_response(player_id, match) -> any:
    return get_match_response(makeGetRequest(f'https://diabotical.cool/api/v1/player/{player_id}').matches.matches[match].match_id)

def get_recent_game_diaboticool_url(player_id, match) -> any:
    response = makeGetRequest(f'https://diabotical.cool/api/v1/player/{player_id}')
    return f'https://diabotical.cool/match/{response.matches.matches[match].match_id}'

def get_all_recent_games_response(player_id) -> any:
    return list(map(lambda t: t.match_id, list(filter(lambda t: t.match_mode == 'wipeout', makeGetRequest(f'https://diabotical.cool/api/v1/player/{player_id}').matches.matches))))