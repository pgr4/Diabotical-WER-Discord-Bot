from player import Player
from rank import Rank
from player_rank_data import PlayerRankData
from http_requests import get_rank_response

class Team:
    
    def __init__(self, team, clients):
        self.score = int(team.score)
        self.name = str(team.name)
        self.placement = bool(team.placement)
        self.players: list[Player] = []
        for client in clients:
            self.players.append(Player(client))
        
        self.players.sort(key=lambda t: t.wer, reverse=True)
        
    @property
    def best_player(self) -> Player:
        return self.players[0]
         
    @property
    def worst_player(self) -> Player:
        return self.players[len(self.players) - 1]

    @property
    def damage_given(self) -> int:
        return sum(map(lambda t: t.damage_given, self.players))
    
    @property
    def damage_taken(self) -> int:
        return sum(map(lambda t: t.damage_taken, self.players))
    
    @property
    def total_heal(self) -> int:
        return sum(map(lambda t: t.total_heal, self.players))
    
    @property
    def result_str(self) -> str:
        if self.placement:
            return 'WIN'
        else:
            return 'LOSS'

    def get_player_rank_data(self) -> list[PlayerRankData]:
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
    
    def get_player_wer_adjusted_output(self) -> str:
        ret = ''
        player_rank_data = self.get_player_rank_data()
        player_rank_data.sort(key=lambda t: t.mmr, reverse=True)
        for player_rank_data in player_rank_data:
            ret = ret + '%-20s %-10s %-10s %-10s %-10s\n' % (player_rank_data.player_name, int(player_rank_data.mmr), '%0.2f' % (player_rank_data.expected_wer), '%0.2f' % (player_rank_data.wer), player_rank_data.difference_factor_formatted)
        return ret

    def get_summary_output(self) -> str:
        return f"{'%-10s %-10s %-10s %-10s %s' % (self.name, self.score, self.damage_given, self.total_heal, self.result_str)}"
    
    def get_player_summary_output(self) -> str:
        return f"""====================╪=====╪======╪=====╪=====╪====╪====╪===╪====╪===╪====╪===╪====╪===╪====╪===╪====╪===╪====╪===╪====╪===
{self.players[0].get_summary_output()}
{self.players[1].get_summary_output()}
{self.players[2].get_summary_output()}
{self.players[3].get_summary_output()}"""
        