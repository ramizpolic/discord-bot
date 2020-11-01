import discord
import asyncio
import re
import time

# formats
from models.msg import msg
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich.prompt import Confirm

class DiscordClient(discord.Client):
    """Handles Discord client logic."""
    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, **kwargs)

    def work(self, *args, **kwargs):
        """[CLI] Wrapper for discord.run to avoid exception spamming."""
        try:
            self.run(*args, **kwargs)
        except Exception as e:
            msg.error(e)

    async def auth(self, token):
        """[CLI] Authenticates client agains Discord API using provided token"""
        await self.wait_until_ready()
        # save token
        with open(".token", "w") as text_file:
            text_file.write(token)
        msg.success("Successfully logged in!")
        await self.logout()

    async def list(self, filter, check_dm):
        """[CLI] Lists guild users matching provided filters"""
        await self.wait_until_ready()
        users = await self.list_users(filter, check_dm)
        msg.print(f"  [bold]Total: [orange3]{len(users)}")
        await self.logout()

    async def notify(self, filter, filepath, delay):
        """[CLI] Sends formatted message to guild users matching provided filters"""
        await self.wait_until_ready()
        try:
            # read file
            with open(filepath, 'r') as file:
                text = file.read()

            # filter
            users = await self.list_users(filter)

            # should send?
            msg.title("Message format")
            msg.print(Panel.fit(text))
            msg.print("")
            should_send = Confirm.ask(f"[bold orange3]?[/][bold white] Are you sure you want to send this message to [orange3]{len(users)}[/orange3] users?")

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

    async def list_users(self, filter, check_dm=False):
        """Prints users from all Discord guilds matching provided filters"""
        try:
            # filter
            msg.title(f"Finding users (Guild filter: '{filter}')")
            users = await self.get_users(filter, True)

            # all accessible users
            msg.title(f"Available users")
            table = Table()
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Name", style="magenta bold")
            table.add_column("Type", justify="right", style="orange3")
            if check_dm:
                table.add_column("DM?", justify="right", style="green")

            for user in track(users, transient=True, description="[bright_black]  Fetching users..."):
                # create row data
                row = [str(user.id), user.name, "[bright_black]Bot" if user.bot else "User"]
                if check_dm:
                    row.append("Yes" if await self.can_dm_user(user) else "[red]No")

                # append
                table.add_row(*row)

            msg.print(table)
            return users

        except Exception as e:
            msg.error(e)
            pass

        return set()

    async def get_users(self, filter, should_print=False):
        """Fetches users from all Discord guilds matching provided filters"""
        if should_print:
            msg.subtitle("Guilds")

        users = set()
        for guild in self.guilds:
            if re.match(filter, guild.name):
                if should_print:
                    msg.listitem(guild.name)
                for channel in guild.channels:
                    users |= await self.get_channel_users(channel)
        return users

    async def can_dm_user(self, user):
        """Checks if you can interact with the user."""
        try:
            message = await user.send("Hi")
            await message.delete()
            time.sleep(1)
        except Exception as e:
            return False
        return True

    async def get_channel_users(self, channel):
        """Returns a set of users that interacted inside a channel."""
        users = set()
        try:
            if channel.type == discord.ChannelType.text:
                async for message in channel.history():
                    users.add(message.author)
                    users.update(message.mentions)
        except Exception as e:
            pass

        return users
