class Weapon:
    
    def __init__(self, weapon_stat: any, time_played: int):
        # Is used
        self.is_used = weapon_stat is not None
        # Time Played
        self.time_played = time_played
        
        if self.is_used:
            # Is WeeBall
            self.is_weeball: bool = (weapon_stat.i == 13 or weapon_stat.i == 14 or weapon_stat.i == 15 or weapon_stat.i == 16)
            # Damage
            self.damage = int(weapon_stat.di)
            # Damage Taken
            self.damage_taken = int(weapon_stat.dt)
            # Kills
            self.frags = int(weapon_stat.f)
            # ID
            self.id = int(weapon_stat.i)
            # Shots Fired
            self.shots_fired = int(weapon_stat.sf)
            # Shots Hit
            self.shots_hit = int(weapon_stat.sh) 
    
    @property
    def accuracy(self) -> int:
        if self.shots_fired == 0:
            return 0
        else:
            return round(100 * (self.shots_hit / self.shots_fired))
     
    @property
    def dps(self) -> float:
        return self.damage / self.time_played
    
    # Output Methods
    
    def get_output(self) -> str:
        if self.is_used:
            return '%-10s %-10s %-10s %s' % (self.frags, self.damage, "%0.2f" % (self.dps), self.accuracy)
        else:
            return '%-10s %-10s %-10s %s' % ('----------', '----------', '----------', '----------')

    def get_summary_output(self) -> str:
        if self.is_used:
            return '%-4s|%-3s' % (self.damage, self.accuracy)
        else:
            return '%-4s|%-3s' % ('', '')