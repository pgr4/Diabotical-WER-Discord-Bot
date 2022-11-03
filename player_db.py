file_name = 'players.csv'

def get_line_output(author, id):
    return f'{get_username(author)},{id}'

def get_username(author):
    return f'{author.name}#{author.discriminator}'

def try_get_player_id(author):
    for line in open(file_name, 'r').readlines():
        split_lines = line.split(',')
        
        if split_lines[0] == get_username(author):
            return split_lines[1]
        
    return None
        
def try_remove_player_id(author):
    ret = False
    
    with open(file_name, 'r') as f:
        lines = f.readlines()
    with open(file_name, 'w') as f:
        for line in lines:
            if line.startswith(get_username(author)) == True:
                ret = True
            else:
                f.write(line)
                
    return ret
                
                

def try_add_player(author, id):
    if try_get_player_id(id) is not None:
        return False
    
    with open(file_name, 'a') as f:
        f.write(get_line_output(author, id))
        
    return True