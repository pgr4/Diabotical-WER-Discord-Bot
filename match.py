from team import Team
from rank import Rank
from player import Player
from player_rank_data import PlayerRankData
from http_requests import get_rank_response
class Match:
    
    def __init__(self, match):
        self.match_map = str(match.match_map)
        self.match_mode = str(match.match_mode)
        self.create_ts = str(match.create_ts)
        self.match_time = int(match.match_time)
        self.team_1 = Team(match.teams[0], list(filter(lambda t: t.team_idx == 0, match.clients)))
        self.team_2 = Team(match.teams[1], list(filter(lambda t: t.team_idx == 1, match.clients)))
    
    @property
    def match_time_str(self):
        return f'{round(int(self.match_time) / 60)}:{int(self.match_time) % 60}'
    
    def get_player_from_teams(self, player_id) -> Player:    
        return (list(filter(lambda t: t.player_id == player_id, self.team_1.players)) or [None])[0] or (list(filter(lambda t: t.player_id == player_id, self.team_2.players)) or [None])[0]
        
    def get_team_for_player(self, player_id) -> Team:
        if any(filter(lambda t: t.player_id == player_id, self.team_1.players)):
            return self.team_1
        elif any(filter(lambda t: t.player_id == player_id, self.team_2.players)):
            return self.team_2
        
        return None 

    # Output Methods

    def get_best_player_adjusted_output(self, player_id) -> str:
        players_team = self.get_team_for_player(player_id)
         
        player_rank_datum = players_team.get_player_rank_data()
        player_rank_datum.sort(key=lambda t: t.difference_factor, reverse=True)
        player_rank_data = player_rank_datum[0]
        
        if player_rank_data.player_id == player_id:
            leading_str = 'Look at me carrying...'
        else:
            leading_str = 'Thanks for the carry...'

        return f"""{leading_str}
{player_rank_data.get_output()}
{player_rank_data.player.get_full_output()}"""

    def get_worst_player_adjusted_output(self, player_id) -> str:
        players_team = self.get_team_for_player(player_id)
        
        player_rank_datum = players_team.get_player_rank_data()
        player_rank_datum.sort(key=lambda t: t.difference_factor, reverse=False)
        player_rank_data = player_rank_datum[0]
        
        if player_rank_data.player_id == player_id:
            leading_str = 'I am getting carried...'
        else:
            leading_str = 'Look what I have to deal with...'

        return f"""{leading_str}
{player_rank_data.get_output()}
{player_rank_data.player.get_full_output()}"""

    def get_all_players_wer_adjusted_output(self) -> str:
        return f"""{'%-20s %-10s %-10s %-10s %-10s' % ('', 'MMR', 'WERe', 'WER', '+/-')}
Team 1:
{self.team_1.get_player_wer_adjusted_output()}
Team 2:
{self.team_2.get_player_wer_adjusted_output()}"""

    def get_match_summary_output(self) -> str:
         return  f"""
{'%-30s %-10s %s' % ('Time', 'Map', 'Length')}
{'%-30s %-10s %s' % (self.create_ts, self.match_map, self.match_time_str)}
     
{'%-10s %-10s %-10s %-10s %s' % ('', 'Score', 'Damage', 'Heal', 'Result')}
{self.team_1.get_summary_output()}
{self.team_2.get_summary_output()}

{'%-20s|%-5s|%-6s|%-5s|%-4s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s' % ('Team 1', 'Score', 'Damage', 'WER', 'Heal', 'M', '%', 'MG', '%', 'Plas', '%', 'SG', '%', 'Rock', '%', 'LG', '%', 'Rail', '%', 'Void', '%')}
{self.team_1.get_player_summary_output()}

{'%-20s|%-5s|%-6s|%-5s|%-4s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s|%-4s|%-3s' % ('Team 2', 'Score', 'Damage', 'WER', 'Heal', 'M', '%', 'MG', '%', 'Plas', '%', 'SG', '%', 'Rock', '%', 'LG', '%', 'Rail', '%', 'Void', '%')}
{self.team_2.get_player_summary_output()}
"""
    
