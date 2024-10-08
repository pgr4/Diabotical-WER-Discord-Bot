from player import Player

class PlayerRankData:
    def __init__(self, player: Player, rank, mmr_total: float, wer_total: float):
        self.player = player
        self.rank = rank
        self.expected_wer = (self.mmr / mmr_total) * wer_total
        
    @property
    def player_id(self) -> str:
        return self.player.player_id
    
    @property
    def player_name(self) -> str:
        return self.player.name
    
    @property
    def wer(self) -> float:
        return self.player.wer
    
    @property
    def mmr(self) -> int:
        return self.rank.mmr
    
    @property
    def difference_factor(self) -> float:
        return self.wer - self.expected_wer 
    
    @property
    def difference_factor_formatted(self) -> str:
        if self.difference_factor == 0:
            return '0.0'
        elif self.difference_factor < 0:
            return '%0.2f' % (self.difference_factor)
        else:
            return '+%0.2f' % (self.difference_factor)
    
    def get_output(self) -> str:
        return f"""{'%-20s %-10s' % ('MMR:', int(self.mmr))}
{'%-20s %-10s' % ('WER:', '%0.2f' % self.wer)}
{'%-20s %-10s' % ('WERe:', '%0.2f' % self.expected_wer)}"""

    def get_full_output(self) -> str:
        return f"""{self.player.get_full_output()}
    
{self.get_output()}"""
        