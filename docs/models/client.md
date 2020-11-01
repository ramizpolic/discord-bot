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

    `can_dm_user(self, user)`
    :   Checks if you can interact with the user.

    `get_channel_users(self, channel)`
    :   Returns a set of users that interacted inside a channel.

    `get_users(self, filter, should_print=False)`
    :   Fetches users from all Discord guilds matching provided filters

    `list(self, filter, check_dm)`
    :   [CLI] Lists guild users matching provided filters

    `list_users(self, filter, check_dm=False)`
    :   Prints users from all Discord guilds matching provided filters

    `notify(self, filter, filepath, delay)`
    :   [CLI] Sends formatted message to guild users matching provided filters

    `notify_users(self, users, text, delay)`
    :   Sends private message to all provided users

    `work(self, *args, **kwargs)`
    :   [CLI] Wrapper for discord.run to avoid exception spamming.
