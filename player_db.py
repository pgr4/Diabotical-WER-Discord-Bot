players_file_name = 'players.csv'
all_players_file_name = 'all_players.csv'

def get_line_output(name, id) -> str:
    return f'{name},{id}\n'

def get_username(author) -> str:
    return f'{author.name}#{author.discriminator}'

def try_get_player_id(author) -> str:
    for line in open(players_file_name, 'r').readlines():
        split_lines = line.split(',')
        
        if split_lines[0] == get_username(author):
            return split_lines[1].replace('\n', '')
        
    return None
        
def try_remove_player_id(author) -> bool:
    try:
        ret = False
        
        with open(players_file_name, 'r') as f:
            lines = f.readlines()
        with open(players_file_name, 'w') as f:
            for line in lines:
                if line.startswith(get_username(author)) == True:
                    ret = True
                else:
                    f.writelines(line)
                    
        return ret
    except:
        return False

def try_add_player(author, id) -> bool:
    try:
        if try_get_player_id(author) is not None:
            return False
        
        with open(players_file_name, 'a') as f:
            f.writelines(get_line_output(get_username(author), id))
            
        return True
    except:
        return False

def try_get_all_player_id(player) -> str:
    f = open(all_players_file_name, 'r')
    while True:
        try:
            line = f.readline()
            
            if not line:
                return None
            
            split_lines = line.split(',')
            
            if split_lines[0].lower() == player.lower():
                    return split_lines[1].replace('\n', '')
        except:
            pass
    

def try_add_all_player(player, id) -> bool:
    try:
        if try_get_all_player_id(player) is not None:
            return False
        
        with open(all_players_file_name, 'a') as f:
            f.write()
            f.writelines(get_line_output(player, id))
            
        return True
    except:
        return False