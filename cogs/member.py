import discord
import random
from discord.ext import commands

# welcome message formats
welcome_msgs = [
    "{} just joined the server - glhf!",
    "{} just joined. Everyone, look busy!",
    "{} just joined. Can I get a heal?",
    "{} joined your party.",
    "{} joined. You must construct additional pylons.",
    "Ermagherd. {} is here.",
    "Welcome, {}. Stay awhile and listen.",
    "Welcome, {}. We were expecting you ( ͡° ͜ʖ ͡°)",
    "Welcome, {}. We hope you brought pizza.",
    "Welcome {}. Leave your weapons by the door.",
    "A wild {} appeared.",
    "Swoooosh. {} just landed.",
    "Brace yourselves. {} just joined the server.",
    "{} just joined. Hide your bananas.",
    "{} just arrived. Seems OP - please nerf.",
    "{} just slid into the server.",
    "A {} has spawned in the server.",
    "Big {} showed up!",
    "Where’s {}? In the server!",
    "{} hopped into the server. Kangaroo!!",
    "{} just showed up. Hold my beer."
]

class member(commands.Cog):
    """Member class controls discord member events and configs."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handles logic for when a new member joins server."""

        # get random welcome msg
        msg_sent = False
        msg = random.choice(welcome_msgs).format(member.mention)
        print(f"New member '{member.name}' joined server.")
        for channel in member.guild.channels:
            if channel.name == "general":
                await channel.send(msg)
                msg_sent = True
                break

        # default channel
        if not msg_sent:
            await member.guild.default_channel.send(msg)

        # set member role
        # role = discord.utils.get(member.server.roles, name="name-of-your-role")
        # try: 
        #     await client.add_roles(member, role)
        #     print(f"[role] Added role '{role.name}' to '{member.name}'.")
        # except:
        #     print(f"[role] Failed adding role '{role.name}' to '{member.name}'.")

def setup(bot):
    bot.add_cog(member(bot))