def codeblock(str):
    return f'```{str}```'

async def send_in_codeblock(command, str):
    await command.channel.send(codeblock(str))