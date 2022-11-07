from player import Player
from rank import Rank
from player_rank_data import PlayerRankData
from enesy import get_rank_response

class Team:
    
    def __init__(self, team, clients):
        self.score = team.score
        self.players = []
        for client in clients:
            self.players.append(Player(client))
        
        self.players.sort(key=lambda t: t.wer, reverse=True)
        
    @property
    def best_player(self):
        return self.players[0]
         
    @property
    def worst_player(self):
        return self.players[len(self.players) - 1]

    def get_player_rank_data(self):
        ret = []
        
        wer_total = 0
        mmr_total = 0
        
        player_ranks = []
        
        # Make get_rank calls for each player
        for player in self.players:
            rank = Rank(get_rank_response(player.player_id))
            
            wer_total = wer_total + player.wer
            mmr_total = mmr_total + rank.mmr
            
            player_ranks.append(rank)
        
        for index, player in enumerate(self.players):
            rank = player_ranks[index]
            ret.append(PlayerRankData(player, rank, mmr_total, wer_total))
        
        return list(ret)
    
    def get_player_wer_adjusted_output(self):
        ret = ''
        player_rank_data = self.get_player_rank_data()
        player_rank_data.sort(key=lambda t: t.mmr, reverse=True)
        for player_rank_data in player_rank_data:
            ret = ret + '%-20s %-10s %-10s %-10s\n' % (player_rank_data.player_name, int(player_rank_data.mmr), '%0.2f' % (player_rank_data.expected_wer), '%0.2f' % (player_rank_data.wer))
        return ret

    def get_output(self):
        return  f"""
{self.players[0].get_output()}
    
{self.players[1].get_output()}

{self.players[2].get_output()}

{self.players[3].get_output()}
"""