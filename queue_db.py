from datetime import datetime, timedelta

queue_file_name = 'queue.csv'

class QueueStatus:
    def __init__(self, hours):
        self.players = []
        self.hours = hours

    def add(self, player):
        self.players.append(player)

    def count(self) -> int:
        return len(self.players)
    
    def __str__(self):
        return f"{self.count()} Players in Queue for next {self.hours} hours {', '.join(self.players)}"

def try_remove_player_id(author) -> bool:
    try:
        ret = False
        
        with open(queue_file_name, 'r') as f:
            lines = f.readlines()
        with open(queue_file_name, 'w') as f:
            for line in lines:
                if line.startswith(get_username(author)) == True:
                    ret = True
                else:
                    f.writelines(line)
                    
        return ret
    except:
        return False
    
def get_line_output(name, hours) -> str:
    current = datetime.now()
    future = current + timedelta(hours=hours)
    return f'{name},{current},{future}\n'

def get_username(author) -> str:
    return f'{author.name}#{author.discriminator}'

def add_to_queue(author, hours) -> bool:
    try_remove_player_id(author)
    with open(queue_file_name, 'a') as f:
        f.writelines(get_line_output(get_username(author), hours))
        return True

def remove_from_queue(author) -> bool:
    try_remove_player_id(author)
    return True

def get_queue_status(hours) -> QueueStatus:
    ret = QueueStatus(hours)
    current = datetime.now()
    # future = current + timedelta(hours=hours)
    for line in open(queue_file_name, 'r').readlines():
        # 0: player
        # 1: init time
        # 2: end time
        split_lines = line.split(',')
        if current >= datetime.strptime(split_lines[1], '%Y-%m-%d %H:%M:%S.%f'):
        # Guess we do not care about the future time for right now 
        # if current >= datetime.strptime(split_lines[1], '%Y-%m-%d %H:%M:%S.%f') and datetime.strptime(split_lines[2].strip('\n'), '%Y-%m-%d %H:%M:%S.%f') >= future:
            ret.add(split_lines[0])
    return ret