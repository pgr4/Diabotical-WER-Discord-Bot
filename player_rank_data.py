class PlayerRankData:
    def __init__(self, player, rank, mmr_total, wer_total):
        self.player = player
        self.rank = rank
        self.expected_wer = (rank.mmr / mmr_total) * wer_total
        
    @property
    def player_id(self):
        return self.player.player_id
    
    @property
    def wer(self):
        return self.player.wer
    
    @property
    def mmr(self):
        return self.rank.mmr
    
    @property
    def difference_factor(self):
        return self.wer - self.expected_wer 
    
    def get_output(self):
        return f"""`MMR \t{int(self.mmr)}
WER \t{'%0.2f' % (self.wer)}
WERe\t{'%0.2f' % (self.expected_wer)}`"""
        