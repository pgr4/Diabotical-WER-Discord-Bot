from weapon import Weapon

class Player:
    
    def __init__(self, client):
        # User Id
        self.player_id = client.user_id
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
        self.melee = Weapon((list(filter(lambda t: t.i == 0, client.stats.w)) or [None])[0], self.time_played)
        # MG i==1
        self.mg = Weapon((list(filter(lambda t: t.i == 1, client.stats.w)) or [None])[0], self.time_played)
        # Plasma i==2
        self.plasma = Weapon((list(filter(lambda t: t.i == 2, client.stats.w)) or [None])[0], self.time_played)
        # Shotgun i==3
        self.shotgun = Weapon((list(filter(lambda t: t.i == 3, client.stats.w)) or [None])[0], self.time_played)
        # Rocket i==4
        self.rocket = Weapon((list(filter(lambda t: t.i == 4, client.stats.w)) or [None])[0], self.time_played)
        # LG i==5
        self.lg = Weapon((list(filter(lambda t: t.i == 5, client.stats.w)) or [None])[0], self.time_played)
        # Rail i==7
        self.rail = Weapon((list(filter(lambda t: t.i == 7, client.stats.w)) or [None])[0], self.time_played)
        # Grenade i==8
        self.grenade = Weapon((list(filter(lambda t: t.i == 8, client.stats.w)) or [None])[0], self.time_played)
        # Void i==19
        self.void = Weapon((list(filter(lambda t: t.i == 19, client.stats.w)) or [None])[0], self.time_played)
        
        # Grav Ball i==13
        self.grav_ball =  Weapon((list(filter(lambda t: t.i == 13, client.stats.w)) or [None])[0], self.time_played)
        # Slow Ball i==14
        self.slow_ball =  Weapon((list(filter(lambda t: t.i == 14, client.stats.w)) or [None])[0], self.time_played)
        # Knock Ball i==15
        self.knock_ball =  Weapon((list(filter(lambda t: t.i == 15, client.stats.w)) or [None])[0], self.time_played)
        # Smoke Ball i==16
        self.smoke_ball =  Weapon((list(filter(lambda t: t.i == 16, client.stats.w)) or [None])[0], self.time_played)
    
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
        return  f"""{self.name}
Rocket:   {self.rocket.get_output()}
LG:       {self.lg.get_output()}
Rail:     {self.rail.get_output()}
Total:    {self.get_total_output()}"""  

    def get_full_output(self):
        return  f"""{self.name}
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
Total:    {self.get_total_output()}"""