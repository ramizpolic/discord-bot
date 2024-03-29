#!/usr/bin/env python3

VERSION = "v1.2.2"
AUTHOR = "Ramiz Polic (hivemindf@gmail.com)"
DONATION = "Make sure to support the future development by donating to PayPal at <hivemindf@gmail.com>"
DEFAULT_TEXT = f"""Howdy __USERNAME__,

This is a testing message generated by automated Discord spam bot.
{DONATION}
"""

import click
import discord
import os
from models.client import DiscordClient
from models.msg import msg
from pathlib import Path

# Initialized environment
dc = DiscordClient(loop=None)

# Load token
TOKEN = ""
try:
    with open('.token', 'r') as file:
        TOKEN = file.read().replace('\n', '')
except:
    pass

def fail_for_token():
    if TOKEN == "":
        msg.error("You are not logged in. Please provide valid token to continue.")
        exit(1)


@click.group()
def cli():
    '''
Discord CLI bot that programmatically controls user events.
It allows advanced control of Discord APIs for provided user.
Initially, you will have to authenticate user by providing a valid token via

$ ./discord-bot auth

\b
Usages:
- Sending formatted messages to users of servers based on searched parameters
- Inspect users you can interact with


\b
Notes:
- Users are gathered from public server text channels message history. 
  The larger the depth of messages, more users will be notified. 
  The cost of this is slower performance.
  This is the only way to obtain list of users from servers.
- This tool is against Discord policies and can result in account suspension.
- To obtain user authentication token, follow https://bit.ly/31Vcno0'''
    pass


@cli.command()
def info():
    """Displays application information"""
    msg.title("Application information")
    msg.item(f"Version", VERSION)
    msg.item(f"Author", AUTHOR)
    msg.item(f"Support", DONATION)



@cli.command()
def init():
    """Initializes the environment with example configs."""
    msg.title("Initializing environment")

    msg_file = Path("FORMAT.md")
    if not msg_file.is_file():
        msg.listitem("Adding FORMAT.md")
        msg_file.write_text(DEFAULT_TEXT)
        msg.listitem("Added!")
    else:
        msg.listitem("File FORMAT.md exists, skipping...")



@cli.command(short_help='Authenticate user against Discord API')
@click.option('--token', prompt='🔑 Token', help='Discord user authentication token')
def login(token):
    """Ensures that you are logged in to Discord API and that you are able to run other commands. 
If you haven't authenticated yourself with this command, you will not be able to proceed. 
To obtain the login token, follow this [guide](https://bit.ly/31Vcno0).

\b
Example usage:
> discord-bot login
> discord-bot login --token="YOUR TOKEN"
"""
    dc.loop.create_task(dc.auth(token))
    dc.work(token, bot=None)




@cli.command(short_help='Displays public information of currently logged user')
def profile():
    dc.loop.create_task(dc.profile())
    dc.work(TOKEN, bot=None)



@cli.command(short_help="Sends friend requests to users on servers matching provided filters")
@click.option('--server', default=".*", help='Regex server name filter (default: .*)')
@click.option('--depth', default=500, help='Depth of message history per channel to inspect (default: 500)')
@click.option('--delay', type=float, default=1.5, help='Wait for this long before sending a new friend request (in seconds, default: 1.5)')
def frequest(server, depth, delay):
    """Sends friend requests to users you can interact with based on the servers your user account is part of. You can filter which
users to send requests to based on the server they are part of.

\b
Example usage:
### Sends friend requests to all users you can see across all servers.
> discord-bot frequest
\b
### Sends friend requests to all users you can see across servers that match "Server.*" filter
> discord-bot frequest --server "Server.*"
"""
    dc.loop.create_task(dc.befriend(server, depth, delay))
    dc.work(TOKEN, bot=None)



@cli.command(short_help="Lists server users matching provided filters")
@click.option('--server', default=".*", help='Regex server name filter (default: .*)')
@click.option('--depth', default=500, help='Depth of message history per channel to inspect (default: 500)')
@click.option('--check-dm', is_flag=True, default=False, help='Checks if you can send direct messages to users (default: False)')
@click.option('--delay', type=float, default=1.5, help='Wait for this long before sending a new message, only valid if --check-dm active (in seconds, default: 1.5)')
def list(server, depth, check_dm, delay):
    """Shows which users you can interact with based on the servers your user account is part of. You can filter which
users to show based on the server they are part of.

\b
Example usage:
### Shows all users you can see with across all servers.
> discord-bot list
\b
### Shows all users you can send a direct message to.
> discord-bot list --check-dm
\b
### Shows all users you can see with across servers that match "Server.*" filter
> discord-bot list --server "Server.*"
"""
    dc.loop.create_task(dc.list(server, depth, check_dm, delay))
    dc.work(TOKEN, bot=None)



@cli.command(short_help="Sends formatted message to server users matching provided filters")
@click.option('--server', default=".*", help='Regex server name filter (default: .*)')
@click.option('--file', default="FORMAT.md", type=click.Path(exists=True), help='Formatted file defining custom message that will be sent to users (default: FORMAT.md)')
@click.option('--delay', type=float, default=1.5, help='Wait for this long before sending a new message (in seconds, default: 1.5)')
@click.option('--depth', default=500, help='Depth of message history per channel to inspect (default: 500)')
def notify(server, file, delay, depth):
    """Sends private messages to users you can interact with. You can filter which
users it should send the message to based on the server they are part of. 
Before it starts sending private messages, it will ask for your confirmation.
If you send too many messages in a row, Discord might disable your access for some time.

\b
Notes:
- You can format the message you want to send to users by providing custom file.
- All attributes formatted as (__ATTR__) will be replaced by user parameters. 
Supported attributes: __USERNAME__

\b
Example usage:
### Sends formatted message from "CUSTOM_MESSAGE.md" file to all users you can interact with across all servers.
> discord-bot notify --file="CUSTOM_MESSAGE.md"

\b
### Sends private message to all users you can interact with across all servers,
### waiting for 1.5 second between sending messages.
> discord-bot notify --delay=1.5

\b
### Sends private message to all users you can interact with across all servers whose name matches
### provided regex.
> discord-bot notify --server "Server"
"""
    dc.loop.create_task(dc.notify(server, file, delay, depth))
    dc.work(TOKEN, bot=None)




if __name__ == '__main__':
    cli()
