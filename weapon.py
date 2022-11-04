class Weapon:
    
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

