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

# CLI Handler
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

@cli.command()
@click.option('--token', prompt='🔑 Token', help='Discord user authentication token')
def login(token):
    """Authenticate user agains Discord API"""
    dc.loop.create_task(dc.auth(token))
    dc.work(token, bot=None)

@cli.command()
@click.option('--name', default=".*", help='Regex guild name filter (default: .*)')
def list(name):
    """Lists guild users matching provided filters"""
    dc.loop.create_task(dc.list(name))
    dc.work(TOKEN, bot=None)

@cli.command()
@click.option('--name', default=".*", help='Regex guild name filter (default: .*)')
@click.option('--file', default="MESSAGE.md", type=click.Path(exists=True), help='File containing message that will be sent to users (default: MESSAGE.md)')
def notify(name, file):
    """Sends formatted message to guild users matching provided filters"""
    dc.loop.create_task(dc.notify(name, file))
    dc.work(TOKEN, bot=None)

if __name__ == '__main__':
    cli()
