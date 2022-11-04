import requests
import json
from types import SimpleNamespace

match_mode = 'wipeout'

def convertToObject(response: requests.Response):
    return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

def convertToString(response: requests.Response):
    return json.dumps(json.loads(response.text), indent=4, sort_keys=True)

def makeGetRequest(url):
    response = requests.get(url)
    return convertToObject(response)

def get_current_games():
    response = makeGetRequest(f'https://diabotical.cool/api/v1/servers/')
    return response.data.data.customs

def get_rank_response(player_id):
    response = makeGetRequest(f'https://api.diabotical.com/api/v0/diabotical/users/{player_id}/rating')
    return response

def get_recent_game_response(player_id):
    response1 = makeGetRequest(f'https://diabotical.cool/api/v1/player/{player_id}')
    response2 = makeGetRequest(f'https://diabotical.cool/api/v1/match/{response1.matches.matches[0].match_id}')
    return response2.match

def get_recent_game_diaboticool_url(player_id):
    response = makeGetRequest(f'https://diabotical.cool/api/v1/player/{player_id}')
    return f'https://diabotical.cool/match/{response.matches.matches[0].match_id}'