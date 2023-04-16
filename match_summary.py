from player_rank_data import PlayerRankData


class MatchSummary:
    
    def __init__(self, is_win: bool, player: PlayerRankData, team: list[PlayerRankData]):
        self.is_win = is_win
        self.player = player
        self.team = team
        
    @property
    def wer(self): 
        return self.player.wer
    
    @property
    def plus_minus(self): 
        return self.wer - sum(map(lambda t: t.wer, self.team)) / len(self.team)