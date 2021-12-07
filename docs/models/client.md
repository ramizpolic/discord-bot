Module client
=============

Classes
-------

`DiscordClient(*args, **kwargs)`
:   Handles Discord client logic.

    ### Ancestors (in MRO)

    * discord.client.Client

    ### Methods

    `auth(self, token)`
    :   [CLI] Authenticates client agains Discord API using provided token

    `befriend(self, server, depth, delay)`
    :   [CLI] Sends friend requests to users matching provided filters

    `can_dm_user(self, user, delay)`
    :   Checks if you can interact with the user.

    `friend_requests(self, users, delay)`
    :   Sends friend requests to all provided users

    `get_channel_users(self, channel, depth)`
    :   Returns a set of users that interacted inside a channel.

    `get_users(self, server, depth, print_guild=False)`
    :   Fetches users from all Discord servers matching provided filters

    `list(self, server, depth, check_dm, delay)`
    :   [CLI] Lists server users matching provided filters

    `list_users(self, server, depth, check_dm=False, delay=1.0)`
    :   Prints users from all Discord servers matching provided filters

    `notify(self, server, filepath, delay, depth)`
    :   [CLI] Sends formatted message to server users matching provided filters

    `notify_users(self, users, text, delay)`
    :   Sends private message to all provided users

    `profile(self)`
    :

    `work(self, *args, **kwargs)`
    :   [CLI] Wrapper for discord.run to avoid exception spamming.
