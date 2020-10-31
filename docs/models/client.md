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

    `get_users(self, filter, print_guild=False)`
    :   Fetches users from all Discord guilds matching provided filters

    `list(self, filter)`
    :   [CLI] Lists guild users matching provided filters

    `list_users(self, filter)`
    :   Prints users from all Discord guilds matching provided filters

    `notify(self, filter, filepath)`
    :   [CLI] Sends formatted message to guild users matching provided filters

    `notify_users(self, users, text)`
    :   Sends private message to all provided users

    `work(self, *args, **kwargs)`
    :   [CLI] Wrapper for discord.run to avoid exception spamming.
