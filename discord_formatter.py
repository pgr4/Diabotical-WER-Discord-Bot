def format_vertical_lines(str) -> str:
    return str.replace('|', '│')

def format(str) -> str:
    return format_vertical_lines(str)

def codeblock(str) -> str:
    return f'```{format(str)}```'

async def send_in_codeblock(command, str):
    await command.channel.send(codeblock(str))
    
def clean_command(command) -> str:
    return command.message.content.replace(command.prefix + command.invoked_with, '').strip()

def get_match_from_command(command) -> int:
    try:
        cleaned_command = clean_command(command)
        return int(cleaned_command)
    except:
        return 0
    
def get_player_from_command(command) -> int:
    try:
        return clean_command(command)
    except:
        return None