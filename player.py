from weapon import Weapon
class Player:
    
    def __init__(self, client):
        # User Id
        self.player_id = str(client.user_id)
        # Name
        self.name = str(client.name)
        # Assists
        self.assists = int(client.stats.a)
        # Deaths
        self.deaths = int(client.stats.d)
        # Damage Given
        self.damage_given = int(client.stats.di)
        # Damage Take
        self.damage_taken = int(client.stats.dt)
        # Kills
        self.frags = int(client.stats.f)
        # Self Heal
        self.heal_self = int(client.stats.oh)
        # Score
        self.score = int(client.stats.s)
        # Team Heal
        self.heal_team = int(client.stats.th)
        # Time Played
        self.time_played = int(client.time_played)
        
        self.melee = Weapon((list(filter(lambda t: t.i == 0, client.stats.w)) or [None])[0], self.time_played, Weapon.MELEE)
        self.mg = Weapon((list(filter(lambda t: t.i == 1, client.stats.w)) or [None])[0], self.time_played, Weapon.MG)
        self.plasma = Weapon((list(filter(lambda t: t.i == 2, client.stats.w)) or [None])[0], self.time_played, Weapon.PLASMA)
        self.shotgun = Weapon((list(filter(lambda t: t.i == 3, client.stats.w)) or [None])[0], self.time_played, Weapon.SG)
        self.rocket = Weapon((list(filter(lambda t: t.i == 4, client.stats.w)) or [None])[0], self.time_played, Weapon.ROCKET)
        self.lg = Weapon((list(filter(lambda t: t.i == 5, client.stats.w)) or [None])[0], self.time_played, Weapon.LG)
        self.rail = Weapon((list(filter(lambda t: t.i == 7, client.stats.w)) or [None])[0], self.time_played, Weapon.RAIL)
        self.grenade = Weapon((list(filter(lambda t: t.i == 8, client.stats.w)) or [None])[0], self.time_played, Weapon.GRENADE)
        self.void = Weapon((list(filter(lambda t: t.i == 19, client.stats.w)) or [None])[0], self.time_played, Weapon.VOID)
        
        self.grav_ball =  Weapon((list(filter(lambda t: t.i == 13, client.stats.w)) or [None])[0], self.time_played, Weapon.GRAV_BALL)
        self.slow_ball =  Weapon((list(filter(lambda t: t.i == 14, client.stats.w)) or [None])[0], self.time_played, Weapon.SLOW_BALL)
        self.knock_ball =  Weapon((list(filter(lambda t: t.i == 15, client.stats.w)) or [None])[0], self.time_played, Weapon.KNOCK_BALL)
        self.smoke_ball =  Weapon((list(filter(lambda t: t.i == 16, client.stats.w)) or [None])[0], self.time_played, Weapon.SMOKE_BALL)
    
    @property
    def all_weapons(self) -> list[Weapon]:
        return [self.melee, self.mg, self.plasma, self.shotgun, self.rocket, self.lg, self.rail, self.grenade, self.void, self.grav_ball, self.slow_ball, self.knock_ball, self.smoke_ball]
    
    @property
    def used_weapons(self) -> int:
        return list(filter(lambda t: t.is_used == True, self.all_weapons))
    
    @property
    def shots_hit(self) -> int:
        return sum(map(lambda t: t.shots_hit, self.used_weapons))
    
    @property
    def shots_fired(self) -> int:
        return sum(map(lambda t: t.shots_fired, self.used_weapons))
        
    @property
    def accuracy(self) -> int:
        if self.shots_fired == 0:
            return 0
        else:
            return round(100 * (self.shots_hit / self.shots_fired))
     
    @property
    def dps(self) -> float:
        return self.damage_given / self.time_played   
    
    @property
    def damage_difference(self) -> int:
        return self.damage_given - self.damage_taken   
    
    @property
    def damage_difference_str(self) -> str:
        if self.damage_difference <= 0:
            return self.damage_difference
        else:
            return f'+{self.damage_difference}'   
    
    @property
    def total_heal(self) -> int:
        return self.heal_self + self.heal_team
    
    @property
    def impact(self) -> int:
        return self.damage_given + self.damage_taken + self.total_heal
    
    @property
    def wer(self) -> float:
        return ((self.impact / self.deaths) + (self.impact / (self.time_played / 60))) / 50

    # Output Methods 

    def get_total_output(self) -> str:
        return 

    def get_full_output(self) -> str:
        return f"""{self.name}

{self.get_weapon_output()}"""

    def get_weapon_output(self) -> str:
        return  f"""{'%-20s %-10s %-10s %-10s %-10s %-10s' % ('', 'Frags', 'Damage', '+/-', 'DPS', 'Accuracy')}
{self.melee.get_output()}
{self.mg.get_output()}
{self.plasma.get_output()}
{self.shotgun.get_output()}
{self.rocket.get_output()}
{self.lg.get_output()}
{self.rail.get_output()}
{self.void.get_output()}
{self.grenade.get_output()}
{'%-20s_%-10s_%-10s_%-10s_%-10s_%-10s' % ('____________________', '__________', '__________', '__________', '__________', '__________')}
{'%-20s %-10s %-10s %-10s %-10s %-10s' % ('Total:', self.frags, self.damage_given, self.damage_difference_str, "%0.2f" % (self.dps), self.accuracy)}"""

    def get_summary_output(self) -> str:
        return '%-20s|%-5s|%-6s|%-5s|%-5s|%-4s|%-8s|%-8s|%-8s|%-8s|%-8s|%-8s|%-8s|%-8s' % (self.name, self.frags, self.damage_given, self.damage_difference_str, '%0.2f' % (self.wer), self.total_heal, self.melee.get_summary_output(), self.mg.get_summary_output(), self.plasma.get_summary_output(), self.shotgun.get_summary_output(), self.rocket.get_summary_output(), self.lg.get_summary_output(), self.rail.get_summary_output(), self.void.get_summary_output())
        
        