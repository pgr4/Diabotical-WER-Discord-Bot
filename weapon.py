class Weapon:
    MELEE = 0
    MG = 1
    PLASMA = 2
    SG = 3
    ROCKET = 4
    LG = 5
    RAIL = 7
    GRENADE = 8
    VOID = 19
    
    GRAV_BALL = 13
    SLOW_BALL = 14
    KNOCK_BALL = 15
    SMOKE_BALL = 16
    
    def __init__(self, weapon_stat: any, time_played: int, id: int):
        # Is used
        self.is_used = weapon_stat is not None
        # Time Played
        self.time_played = time_played
        # ID
        # self.id = int(weapon_stat.i)
        self.id = id
        
        if self.is_used:
            # Is WeeBall
            self.is_weeball: bool = (weapon_stat.i == 13 or weapon_stat.i == 14 or weapon_stat.i == 15 or weapon_stat.i == 16)
            # Damage
            self.damage_given = int(weapon_stat.di)
            # Damage Taken
            self.damage_taken = int(weapon_stat.dt)
            # Kills
            self.frags = int(weapon_stat.f)
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
    def name(self) -> str:
        if self.id == self.MELEE:
            return 'Melee'
        elif self.id == self.MG:
            return 'Machine Gun'
        elif self.id == self.PLASMA:
            return 'Plasma'
        elif self.id == self.SG:
            return 'Shotgun'
        elif self.id == self.ROCKET:
            return 'Rocket'
        elif self.id == self.LG:
            return 'Lightning Gun'
        elif self.id == self.RAIL:
            return 'Rail'
        elif self.id == self.GRENADE:
            return 'Grenade Launcher'
        elif self.id == self.VOID:
            return 'Void Cannon'
        elif self.id == self.GRAV_BALL:
            return 'Grav Wee-Ball'
        elif self.id == self.SLOW_BALL:
            return 'Slow Wee-Ball'
        elif self.id == self.KNOCK_BALL:
            return 'Knock Wee-Ball'
        elif self.id == self.SMOKE_BALL:
            return 'Smoke Wee-Ball'
        else:
            return ''
    
    # Output Methods
    
    def get_output(self) -> str:
        if self.is_used:
            return '%-20s %-10s %-10s %-10s %-10s %-10s' % (self.name + ':', self.frags, self.damage_given, self.damage_difference_str, "%0.2f" % (self.dps), self.accuracy)
        else:
            return '%-20s %-10s %-10s %-10s %-10s %-10s' % (self.name + ':', '----------', '----------', '----------', '----------', '----------')

    def get_summary_output(self) -> str:
        if self.is_used:
            return '%-4s|%-3s' % (self.damage_given, self.accuracy)
        else:
            return '%-4s|%-3s' % ('', '')