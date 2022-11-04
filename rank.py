class Rank:
    BASE_MMR = 630.5
    INCREMENT = 39
    explorer_I		= BASE_MMR
    explorer_II		= explorer_I + 		INCREMENT
    explorer_III	= explorer_II + 	INCREMENT
    explorer_IV		= explorer_III + 	INCREMENT
    explorer_V		= explorer_IV + 	INCREMENT
    artisan_I		= explorer_V + 		INCREMENT
    artisan_II		= artisan_I + 		INCREMENT
    artisan_III		= artisan_II + 		INCREMENT
    artisan_IV		= artisan_III + 	INCREMENT
    artisan_V		= artisan_IV + 		INCREMENT
    scout_I			= artisan_V + 		INCREMENT
    scout_II		= scout_I + 		INCREMENT
    scout_III		= scout_II + 		INCREMENT
    scout_IV		= scout_III + 		INCREMENT
    scout_V			= scout_IV + 		INCREMENT
    hunter_I		= scout_V + 		INCREMENT
    hunter_II		= hunter_I + 		INCREMENT
    hunter_III		= hunter_II + 		INCREMENT
    hunter_IV		= hunter_III + 		INCREMENT
    hunter_V		= hunter_IV + 		INCREMENT
    tactician_I		= hunter_V + 		INCREMENT
    tactician_II	= tactician_I + 	INCREMENT
    tactician_III	= tactician_II + 	INCREMENT
    tactician_IV	= tactician_III + 	INCREMENT
    tactician_V		= tactician_IV + 	INCREMENT
    sentinel_I		= tactician_V + 	INCREMENT
    sentinel_II		= sentinel_I + 		INCREMENT
    sentinel_III	= sentinel_II + 	INCREMENT
    sentinel_IV		= sentinel_III + 	INCREMENT
    sentinel_V		= sentinel_IV + 	INCREMENT
    vindicator_I	= sentinel_V + 		INCREMENT
    vindicator_II	= vindicator_I + 	INCREMENT
    vindicator_III	= vindicator_II + 	INCREMENT
    vindicator_IV	= vindicator_III + 	INCREMENT
    vindicator_V	= vindicator_IV + 	INCREMENT
    architect_I		= vindicator_V + 	INCREMENT
    architect_II	= architect_I + 	INCREMENT
    architect_III	= architect_II + 	INCREMENT
    architect_IV	= architect_III + 	INCREMENT
    architect_V		= architect_IV + 	INCREMENT
    
    
    def __init__(self, rank_response):
        self.rank_tier = rank_response.ratings[0].rank_tier
        self.match_count = rank_response.ratings[0].match_count
        self.mmr_key = rank_response.ratings[0].mmr_key
        self.mode_key = rank_response.ratings[0].mode_key
        
    @property
    def mmr(self):
        return Rank.BASE_MMR + ((self.rank_tier - 1) * Rank.INCREMENT)
    
    @property
    def rank_string(self):
        if self.mmr > Rank.architect_V:
            return 'God'
        elif self.mmr >= Rank.architect_V:
            return 'Architect V' 
        elif self.mmr >= Rank.architect_IV:
            return 'Architect IV'
        elif self.mmr >= Rank.architect_III:
            return 'Architect III'
        elif self.mmr >= Rank.architect_II:
            return 'Architect II'
        elif self.mmr >= Rank.architect_I:
            return 'Architect I' 
        elif self.mmr >= Rank.vindicator_V:
            return 'Vindicator V'
        elif self.mmr >= Rank.vindicator_IV:
            return 'Vindicator IV'
        elif self.mmr >= Rank.vindicator_III:
            return 'Vindicator III'
        elif self.mmr >= Rank.vindicator_II:
            return 'Vindicator II'
        elif self.mmr >= Rank.vindicator_I:
            return 'Vindicator I'
        elif self.mmr >= Rank.sentinel_V:
            return 'Sentinel V' 
        elif self.mmr >= Rank.sentinel_IV:
            return 'Sentinel IV' 
        elif self.mmr >= Rank.sentinel_III:
            return 'Sentinel III'
        elif self.mmr >= Rank.sentinel_II:
            return 'Sentinel II' 
        elif self.mmr >= Rank.sentinel_I:
            return 'Sentinel I' 
        elif self.mmr >= Rank.tactician_V:
            return 'Tactician V' 
        elif self.mmr >= Rank.tactician_IV:
            return 'Tactician IV'
        elif self.mmr >= Rank.tactician_III:
            return 'Tactician III'
        elif self.mmr >= Rank.tactician_II:
            return 'Tactician II'
        elif self.mmr >= Rank.tactician_I:
            return 'Tactician I' 
        elif self.mmr >= Rank.hunter_V:
            return 'Hunter V' 
        elif self.mmr >= Rank.hunter_IV:
            return 'Hunter IV' 
        elif self.mmr >= Rank.hunter_III:
            return 'Hunter III' 
        elif self.mmr >= Rank.hunter_II:
            return 'Hunter II' 
        elif self.mmr >= Rank.hunter_I:
            return 'Hunter I' 
        elif self.mmr >= Rank.scout_V:
            return 'Scout V' 	
        elif self.mmr >= Rank.scout_IV:
            return 'Scout IV' 
        elif self.mmr >= Rank.scout_III:
            return 'Scout III' 
        elif self.mmr >= Rank.scout_II:
            return 'Scout II' 
        elif self.mmr >= Rank.scout_I:
            return 'Scout I' 	
        elif self.mmr >= Rank.artisan_V:
            return 'Artisan V' 
        elif self.mmr >= Rank.artisan_IV:
            return 'Artisan IV' 
        elif self.mmr >= Rank.artisan_III:
            return 'Artisan III' 
        elif self.mmr >= Rank.artisan_II:
            return 'Artisan II' 
        elif self.mmr >= Rank.artisan_I:
            return 'Artisan I' 
        elif self.mmr >= Rank.explorer_V:
            return 'Explorer V' 
        elif self.mmr >= Rank.explorer_IV:
            return 'Explorer IV' 
        elif self.mmr >= Rank.explorer_III:
            return 'Explorer III'
        elif self.mmr >= Rank.explorer_II:
            return 'Explorer II' 
        else:
            return 'Explorer I'
        
    def get_output(self):
        return f'`{self.rank_string} ({int(self.mmr)})`'
    
    
# ELO     SCORE   EXPECTED_SCORE     
# 1000    10      10
# 300     2       3
# 500     7       5
# 200     1       2

# 2000    20      20


# EXPECTED_SCORE = (ELO / ELOt) * TOTAL
            