from team import Team
from rank import Rank
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
        
        if players_team is None:
            return None
        
        wer_total = 0
        mmr_total = 0
        
        player_ranks = []
        
        # Make get_rank calls for each player
        for player in players_team.players:
            rank = Rank(get_rank_response(player.player_id))
            
            wer_total = wer_total + player.wer
            mmr_total = mmr_total + rank.mmr
            
            player_ranks.append(rank)
        
        # (Score, Player, Rank)
        best_player_tuple = (None, None, None)
        
        for index, player in enumerate(players_team.players):
            rank = player_ranks[index]
            expected_score = (rank.mmr / mmr_total) * wer_total
            if best_player_tuple[0] == None or best_player_tuple[0] < expected_score:
                best_player_tuple = (expected_score, player, rank)
                
        best_player_expected_score = best_player_tuple[0]
        best_player = best_player_tuple[1]
        best_player_rank = best_player_tuple[2]
        
        if best_player.player_id == player_id:
            leading_str = 'Look at me carrying*...'
        else:
            leading_str = 'Thanks for the carry*...'

        return f"""`{leading_str}
MMR \t{best_player_rank.mmr}
WER \t{'%0.2f' % (best_player.wer)}
WER*\t{'%0.2f' % (best_player_expected_score)}`
{best_player.get_full_output()}"""

    def get_worst_player_adjusted_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
        
        if players_team is None:
            return None
        
        wer_total = 0
        mmr_total = 0
        
        player_ranks = []
        
        # Make get_rank calls for each player
        for player in players_team.players:
            rank = Rank(get_rank_response(player.player_id))
            
            wer_total = wer_total + player.wer
            mmr_total = mmr_total + rank.mmr
            
            player_ranks.append(rank)
        
        # (Score, Player, Rank)
        worst_player_tuple = (None, None, None)
        
        for index, player in enumerate(players_team.players):
            rank = player_ranks[index]
            expected_score = (rank.mmr / mmr_total) * wer_total
            if worst_player_tuple[0] == None or worst_player_tuple[0] > expected_score:
                worst_player_tuple = (expected_score, player, rank)
                
        worst_player_expected_score = worst_player_tuple[0]
        worst_player = worst_player_tuple[1]
        worst_player_rank = worst_player_tuple[2]

        if worst_player.player_id == player_id:
            leading_str = 'I am getting carried*...'
        else:
            leading_str = 'Look what I have to deal with*...'

        return f"""`{leading_str}`
MMR \t{int(worst_player_rank.mmr)}
WER \t{'%0.2f' % (worst_player.wer)}
WER*\t{'%0.2f' % (worst_player_expected_score)}`
{worst_player.get_full_output()}"""

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
          
    def get_output(self):
        return  f"""
`Team 1`
    {self.team_1.get_output()}
    
`Team 2`
    {self.team_2.get_output()}"""