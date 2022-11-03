class WeaponStat:
    
    def __init__(self, weapon_stat, time_played):
        # Is used
        self.is_used = weapon_stat is not None
        # Time Played
        self.time_played = time_played
        
        if self.is_used:
            # Is WeeBall
            self.is_weeball = weapon_stat.i == 13 or weapon_stat.i == 14 or weapon_stat.i == 15 or weapon_stat.i == 16
            # Damage
            self.damage = weapon_stat.di
            # Damage Taken
            self.damage_taken = weapon_stat.dt
            # Kills
            self.frags = weapon_stat.f
            # ID
            self.id = weapon_stat.i
            # Shots Fired
            self.shots_fired = weapon_stat.sf
            # Shots Hit
            self.shots_hit = weapon_stat.sh
        
    
    @property
    def accuracy(self):
        if self.shots_fired == 0:
            return 0
        else:
            return round(100 * (self.shots_hit / self.shots_fired))
     
    @property
    def dps(self):
        return self.damage / self.time_played
    
    def get_output(self):
        if self.is_used:
            return '%-10s %-10s %-10s %s' % (self.frags, self.damage, "%0.2f" % (self.dps), self.accuracy)
        else:
            return '%-10s %-10s %-10s %s' % ('----------', '----------', '----------', '----------')

class Player:
    
    def __init__(self, client):
        # User Id
        self.user_id = client.user_id
        # Name
        self.name = client.name
        # Assists
        self.assists = client.stats.a
        # Deaths
        self.deaths = client.stats.d
        # Damage Given
        self.damage_given = client.stats.di
        # Damage Take
        self.damage_taken = client.stats.dt
        # Kills
        self.frags = client.stats.f
        # Self Heal
        self.heal_self = client.stats.oh
        # Score
        self.score = client.stats.s
        # Team Heal
        self.heal_team = client.stats.th
        # Time Played
        self.time_played = client.time_played
        
        # Melee i==0
        self.melee = WeaponStat((list(filter(lambda t: t.i == 0, client.stats.w)) or [None])[0], self.time_played)
        # MG i==1
        self.mg = WeaponStat((list(filter(lambda t: t.i == 1, client.stats.w)) or [None])[0], self.time_played)
        # Plasma i==2
        self.plasma = WeaponStat((list(filter(lambda t: t.i == 2, client.stats.w)) or [None])[0], self.time_played)
        # Shotgun i==3
        self.shotgun = WeaponStat((list(filter(lambda t: t.i == 3, client.stats.w)) or [None])[0], self.time_played)
        # Rocket i==4
        self.rocket = WeaponStat((list(filter(lambda t: t.i == 4, client.stats.w)) or [None])[0], self.time_played)
        # LG i==5
        self.lg = WeaponStat((list(filter(lambda t: t.i == 5, client.stats.w)) or [None])[0], self.time_played)
        # Rail i==7
        self.rail = WeaponStat((list(filter(lambda t: t.i == 7, client.stats.w)) or [None])[0], self.time_played)
        # Grenade i==8
        self.grenade = WeaponStat((list(filter(lambda t: t.i == 8, client.stats.w)) or [None])[0], self.time_played)
        # Void i==19
        self.void = WeaponStat((list(filter(lambda t: t.i == 19, client.stats.w)) or [None])[0], self.time_played)
        
        # Grav Ball i==13
        self.grav_ball =  WeaponStat((list(filter(lambda t: t.i == 13, client.stats.w)) or [None])[0], self.time_played)
        # Slow Ball i==14
        self.slow_ball =  WeaponStat((list(filter(lambda t: t.i == 14, client.stats.w)) or [None])[0], self.time_played)
        # Knock Ball i==15
        self.knock_ball =  WeaponStat((list(filter(lambda t: t.i == 15, client.stats.w)) or [None])[0], self.time_played)
        # Smoke Ball i==16
        self.smoke_ball =  WeaponStat((list(filter(lambda t: t.i == 16, client.stats.w)) or [None])[0], self.time_played)
    
    @property
    def all_weapons(self):
        return [self.melee, self.mg, self.plasma, self.shotgun, self.rocket, self.lg, self.rail, self.grenade, self.void, self.grav_ball, self.slow_ball, self.knock_ball, self.smoke_ball]
    
    @property
    def used_weapons(self):
        return list(filter(lambda t: t.is_used == True, self.all_weapons))
    
    @property
    def shots_hit(self):
        return sum(map(lambda t: t.shots_hit, self.used_weapons))
    
    @property
    def shots_fired(self):
        return sum(map(lambda t: t.shots_fired, self.used_weapons))
        
    @property
    def accuracy(self):
        if self.shots_fired == 0:
            return 0
        else:
            return round(100 * (self.shots_hit / self.shots_fired))
     
    @property
    def dps(self):
        return self.damage_given / self.time_played   
    
    @property
    def damage_difference(self):
        return self.damage_given - self.damage_taken   
    
    @property
    def impact(self):
        return self.damage_given + self.damage_taken + self.heal_team + self.heal_self
    
    @property
    def wer(self):
        return ((self.impact / self.deaths) + (self.impact / (self.time_played / 60))) / 50

    def get_total_output(self):
        return '%-10s %-10s %-10s %s' % (self.frags, self.damage_given, "%0.2f" % (self.dps), self.accuracy)

    def get_output(self):
        return  f"""`{self.name}
Rocket:   {self.rocket.get_output()}
LG:       {self.lg.get_output()}
Rail:     {self.rail.get_output()}
Total:    {self.get_total_output()}`"""  

    def get_full_output(self):
        return  f"""`{self.name}
{'%-10s %-10s %-10s %-10s %s' % ('', 'Frags', 'Damage', 'DPS', 'Accuracy')}
Melee:    {self.melee.get_output()}
MG:       {self.mg.get_output()}
Plasma:   {self.plasma.get_output()}
Shotgun:  {self.shotgun.get_output()}
Rocket:   {self.rocket.get_output()}
LG:       {self.lg.get_output()}
Rail:     {self.rail.get_output()}
Grenade:  {self.grenade.get_output()}
Void:     {self.void.get_output()}
Total:    {self.get_total_output()}`""" 
        
    
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

class Match:
    
    def __init__(self, match):
        self.match_map = match.match_map
        self.match_mode = match.match_mode
        self.create_ts = match.create_ts
        self.match_time = match.match_time
        self.team_1 = Team(match.teams[0], list(filter(lambda t: t.team_idx == 0, match.clients)))
        self.team_2 = Team(match.teams[1], list(filter(lambda t: t.team_idx == 1, match.clients)))
        
    def get_player_from_teams(self, player_id):    
        return (list(filter(lambda t: t.user_id == player_id, self.team_1.players)) or [None])[0] or (list(filter(lambda t: t.user_id == player_id, self.team_2.players)) or [None])[0]
        
    def get_team_for_player(self, player_id):
        if any(filter(lambda t: t.user_id == player_id, self.team_1.players)):
            return self.team_1
        elif any(filter(lambda t: t.user_id == player_id, self.team_2.players)):
            return self.team_2
        
        return None 

    def get_worst_player_output(self, player_id):
        players_team = self.get_team_for_player(player_id)
        
        if players_team is None:
            return None
        
        worst_player = players_team.worst_player

        if worst_player.user_id == player_id:
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

        if best_player.user_id == player_id:
            leading_str = 'Look at me carrying...'
        else:
            leading_str = 'Thanks for the carry...'

        return f"""`{leading_str}`
{best_player.get_full_output()}"""

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
    
    
        