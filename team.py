from player import Player

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

    def get_output(self):
        return  f"""
{self.players[0].get_output()}
    
{self.players[1].get_output()}

{self.players[2].get_output()}

{self.players[3].get_output()}
"""