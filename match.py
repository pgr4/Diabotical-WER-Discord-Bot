from team import Team
from rank import Rank
from player_rank_data import PlayerRankData
from enesy import get_rank_response
class Match:
    
    def __init__(self, match):
        self.match_map = match.match_map
        self.match_mode = match.match_mode
        self.create_ts = match.create_ts
        self.match_time = match.match_time
        self.team_1 = Team(match.teams[0], list(filter(lambda t: t.team_idx == 0, match.clients)))
        self.team_2 = Team(match.teams[1], list(filter(lambda t: t.team_idx == 1, match.clients)))
        
    def get_player_from_teams(self, player_id):    
        return (list(filter(lambda t: t.player_id == player_id, self.team_1.players)) or [None])[0] or (list(filter(lambda t: t.player_id == player_id, self.team_2.players)) or [None])[0]
        
    def get_team_for_player(self, player_id):
        if any(filter(lambda t: t.player_id == player_id, self.team_1.players)):
            return self.team_1
        elif any(filter(lambda t: t.player_id == player_id, self.team_2.players)):
            return self.team_2
        
        return None 

    def get_worst_player_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
        
        if players_team is None:
            return None
        
        worst_player = players_team.worst_player

        if worst_player.player_id == player_id:
            leading_str = 'I am getting carried...'
        else:
            leading_str = 'Look what I have to deal with...'

        return f"""`{leading_str}`
{worst_player.get_full_output()}"""

    def get_best_player_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
        
        if players_team is None:
            return None
        
        best_player = players_team.best_player

        if best_player.player_id == player_id:
            leading_str = 'Look at me carrying...'
        else:
            leading_str = 'Thanks for the carry...'

        return f"""`{leading_str}`
{best_player.get_full_output()}"""

    def get_best_player_adjusted_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
         
        player_rank_datum = players_team.get_player_rank_data()
        player_rank_datum.sort(key=lambda t: t.difference_factor, reverse=True)
        player_rank_data = player_rank_datum[0]
        
        if player_rank_data.player_id == player_id:
            leading_str = 'Look at me carrying*...'
        else:
            leading_str = 'Thanks for the carry*...'

        return f"""`{leading_str}`
{player_rank_data.get_output()}
{player_rank_data.player.get_full_output()}"""

    def get_worst_player_adjusted_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
        
        player_rank_datum = players_team.get_player_rank_data()
        player_rank_datum.sort(key=lambda t: t.difference_factor, reverse=False)
        player_rank_data = player_rank_datum[0]
        
        if player_rank_data.player_id == player_id:
            leading_str = 'I am getting carried*...'
        else:
            leading_str = 'Look what I have to deal with*...'

        return f"""`{leading_str}`
{player_rank_data.get_output()}
{player_rank_data.player.get_full_output()}"""

    def get_player_output(self, player_id):
        player = self.get_player_from_teams(player_id)

        if player == None:
            return None
        
        return player.get_full_output()
    
    def get_player_wer_output(self, player_id):
        player = self.get_player_from_teams(player_id)
        
        if player == None:
            return None
        
        return f'`Check out my WER Score: {"%0.2f" % (player.wer)} - thanks enesy`'

    def get_player_wer_adjusted_output(self, player_id):
        team = self.get_team_for_player(player_id)
        
        if team == None:
            return None
        
        player_rank_data = list(filter(lambda t: t.player_id == player_id, team.get_player_rank_data()))[0]
        
        return f'`Check out my WERe Score: {"%0.2f" % (player_rank_data.expected_wer)} WER: {"%0.2f" % (player_rank_data.wer)} MMR: {int(player_rank_data.mmr)} - thanks enesy`'

    def get_output(self):
        return  f"""
`Team 1`
    {self.team_1.get_output()}
    
`Team 2`
    {self.team_2.get_output()}"""