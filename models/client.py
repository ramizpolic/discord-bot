import discord
import asyncio
import re
import time
from datetime import datetime

# formats
from models.msg import msg
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich import print

class DiscordClient(discord.Client):
    """Handles Discord client logic."""
    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, **kwargs)

    def work(self, *args, **kwargs):
        """[CLI] Wrapper for discord.run to avoid exception spamming."""
        start = datetime.now()
        
        try:
            self.run(*args, **kwargs)
        except Exception as e:
            msg.error(e)

        end = datetime.now()
        msg.info(f"\nTime to execute: {end - start}\n")

    async def auth(self, token):
        """[CLI] Authenticates client agains Discord API using provided token"""
        await self.wait_until_ready()
        # save token
        with open(".token", "w") as text_file:
            text_file.write(token)
        msg.success("Successfully logged in!")
        await self.logout()

    async def profile(self):
        await self.wait_until_ready()
        try:
            user = self.user
            msg.title("My profile")
            msg.item(f"Username", user.name)
            msg.item(f"Email", user.email)
        except Exception as e:
            pass
        await self.logout()

    async def list(self, server, depth, check_dm, delay):
        """[CLI] Lists server users matching provided filters"""
        await self.wait_until_ready()
        users = await self.list_users(server, depth, check_dm, delay)
        msg.print(f"  [bold]Total: [orange3]{len(users)}")
        await self.logout()

    async def befriend(self, server, depth, delay):
        """[CLI] Sends friend requests to users matching provided filters"""
        await self.wait_until_ready()
        try:
            # filter
            users = await self.list_users(server, depth)

            print(f"[bold orange3]?[/][bold white] Are you sure you want to send friend requests to [orange3]{len(users)}[/orange3] users (y/n)?", end=" ")
            should_send = input().upper() == "Y"

            # send requests
            if should_send:
                success = await self.friend_requests(users, delay)
                msg.print("")
                msg.success(f"Successfully sent friend requests to [orange3]{success}/{len(users)}[/orange3] users.")
            else:
                msg.warn("Skipping notify. Bye...")

        except Exception as e:
            msg.error(e)
            pass

        await self.logout()

    async def notify(self, server, filepath, delay, depth):
        """[CLI] Sends formatted message to server users matching provided filters"""
        await self.wait_until_ready()
        try:
            # read file
            with open(filepath, 'r') as file:
                text = file.read()

            # filter
            users = await self.list_users(server, depth)

            # should send?
            msg.title("Message format")
            msg.print(Panel.fit(text))
            msg.print("")

            print(f"[bold orange3]?[/][bold white] Are you sure you want to send this message to [orange3]{len(users)}[/orange3] users (y/n)?", end=" ")
            should_send = input().upper() == "Y"

            # send messages
            if should_send:
                success = await self.notify_users(users, text, delay)
                msg.print("")
                msg.success(f"Successfully sent messages to [orange3]{success}/{len(users)}[/orange3] users.")
            else:
                msg.warn("Skipping notify. Bye...")

        except Exception as e:
            msg.error(e)
            pass

        await self.logout()

    async def notify_users(self, users, text, delay):
        """Sends private message to all provided users"""
        success = 0
        for user in track(users, transient=True, description="[bright_black]  Sending private messages..."):
            try:
                message = text.replace("__USERNAME__", user.mention)
                await user.send(message)
                time.sleep(delay)
                success += 1
            except Exception:
                pass
        return success

    async def friend_requests(self, users, delay):
        """Sends friend requests to all provided users"""
        success = 0
        for user in track(users, transient=True, description="[bright_black]  Sending friend requests..."):
            try:
                if not user.is_friend():
                    await user.send_friend_request()
                    time.sleep(delay)
                success += 1
            except Exception as e:
                pass
        return success

    async def list_users(self, server, depth, check_dm=False, delay=1.0):
        """Prints users from all Discord servers matching provided filters"""
        try:
            # filter
            msg.title(f"Finding users (Guild filter: '{server}')")
            users = await self.get_users(server, depth, True)

            # all accessible users
            msg.title(f"Available users")
            table = Table()
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Name", style="magenta bold")
            table.add_column("Type", justify="right", style="orange3")
            table.add_column("Friend?", justify="right", style="green")

            if check_dm:
                table.add_column("DM?", justify="right", style="green")

            for user in track(users, transient=True, description="[bright_black]  Fetching users..."):
                # create row data
                row = [str(user.id), user.name, "[bright_black]Bot" if user.bot else "User"]

                # friend?
                try:
                    row.append("Yes" if user.is_friend() else "[red]No")
                except Exception:
                    row.append("[red]No")

                # dm?
                if check_dm:
                    row.append("Yes" if await self.can_dm_user(user, delay) else "[red]No")

                # append
                table.add_row(*row)

            msg.print(table)
            return users

        except Exception as e:
            msg.error(e)
            pass

        return set()

    async def get_users(self, server, depth, print_guild=False):
        """Fetches users from all Discord servers matching provided filters"""
        if print_guild:
            msg.subtitle("Guilds")

        users = set()
        for guild in self.guilds:
            if re.match(server, guild.name):
                if print_guild:
                    msg.listitem(guild.name)

                try:
                    for channel in guild.channels:
                        users |= await self.get_channel_users(channel, depth)
                except Exception as e:
                    pass
        return users

    async def can_dm_user(self, user, delay):
        """Checks if you can interact with the user."""
        try:
            message = await user.send(content=".")
            await message.delete()
            time.sleep(delay)
        except Exception as e:
            return False
        return True

    async def get_channel_users(self, channel, depth):
        """Returns a set of users that interacted inside a channel."""
        users = set()
        try:
            if channel.type == discord.ChannelType.text:
                async for message in channel.history(limit=depth):
                    users.add(message.author)
                    users.update(message.mentions)
        except Exception as e:
            pass

        return users
