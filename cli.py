#!/usr/bin/env python3

VERSION = "v1.0.0"
AUTHOR = "Ramiz Polic (fhivemind)"

import click
import discord
import os
from models.client import DiscordClient
from models.msg import msg

# Initialize environment
dc = DiscordClient(loop=None)

# Load token
TOKEN = ""
try:
    with open('.token', 'r') as file:
        TOKEN = file.read().replace('\n', '')
except:
    pass

@click.group()
def cli():
    '''
Discord CLI bot that programmatically controls user events.
It allows advanced control of Discord APIs for provided user.
Initially, you will have to authenticate user by providing a valid token via

$ ./cli.py auth

\b
Usages:
- Sending messages to users of a specific guild
- Sending formatted messages to all visible users

\b
Notes:
- This tool is against Discord policies and can result in account suspension.
- To obtain user token, follow https://bit.ly/31Vcno0'''
    pass

@cli.command()
def info():
    """Displays info information"""
    msg.title("Environment information")
    msg.item(f"Version", VERSION)
    msg.item(f"Author", AUTHOR)
    msg.item(f"Token", TOKEN)

@cli.command(short_help='Authenticate user agains Discord API')
@click.option('--token', prompt='🔑 Token', help='Discord user authentication token')
def login(token):
    """Ensures that you are logged in to Discord API and that you are able to run other commands. 
If you haven't authenticated yourself with this command, you will not be able to proceed. 
To obtain the login token, follow this [guide](https://bit.ly/31Vcno0).

\b
Example:
```
$ cli.py login
$ cli.py login --token="YOUR TOKEN"
```
"""
    dc.loop.create_task(dc.auth(token))
    dc.work(token, bot=None)

@cli.command(short_help="Lists guild users matching provided filters")
@click.option('--name', default=".*", help='Regex guild name filter (default: .*)')
def list(name):
    """Shows which users you can interact with based on the guilds your user account is part of. You can filter which
users to show based on the guild they are part of.

\b
Example:
```bash
### Shows all users you can interact with across all guilds.
$ cli.exe list
\b
### Shows all users you can interact with across all guilds whose
### name regex matches "Example.*".
$ cli.exe list --name "Example.*"
```
"""
    dc.loop.create_task(dc.list(name))
    dc.work(TOKEN, bot=None)

@cli.command(short_help="Sends formatted message to guild users matching provided filters")
@click.option('--name', default=".*", help='Regex guild name filter (default: .*)')
@click.option('--file', default="MESSAGE.md", type=click.Path(exists=True), help='File containing message that will be sent to users (default: MESSAGE.md)')
def notify(name, file):
    """Sends private messages to users you can interact with. You can filter which
users it should send the message to based on the guild they are part of. 
Before it starts sending private messages, it will for your confirmation.

\b
Notes:
- You can format the message you want to send to users by adding providing the file.
- All attributes formatted as (__ATTR__) will be replaced by user parameters. 
Supported attributes: __USERNAME__

\b
For example:
```bash
### Sends private message formatted as MESSAGES.md to
### all users you can interact with across all guilds.
$ cli.py notify

\b
### Sends private message formatted as MESSAGES.md to all users
### you can interact with across all guilds whose name matches
### provided regex.
$ cli.py notify --name "Example.*"
```
"""
    dc.loop.create_task(dc.notify(name, file))
    dc.work(TOKEN, bot=None)

if __name__ == '__main__':
    cli()
