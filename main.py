import discord
from discord import app_commands 
import cloudscraper
import requests

server_id = 'server id'
scraper = cloudscraper.create_scraper()

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync(guild = discord.Object(id=server_id)) 
            self.synced = True
        print(f"Logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name="player",description="Gets player stats",guild=discord.Object(id=server_id))
async def self(interaction: discord.Interaction, username: str):
    #get user id
    sent = False
    failed = False

    try:
        get_userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={username}").json()
        get_userid = str(get_userid["Id"])
        userID = get_userid
    except:
        failed = True
        sent = True
        em = discord.Embed(title="User has not played bloxflip", color=0xAE00FF)
        await interaction.response.send_message(embed=em)
        return 0

    #get bloxflip info
    try:
        general_bloxinfo = scraper.get(f"https://api.bloxflip.com/user/lookup/{userID}").json()
        rank = general_bloxinfo['rank']
        wagered = int(general_bloxinfo['wager'])
        games_played = general_bloxinfo['gamesPlayed']
        rain_winnings = int(general_bloxinfo['rainWinnings'])
        trivia_Winnings = int(general_bloxinfo['triviaWinnings'])
        failed = False
    except:
        if sent == False:
            failed = True
            sent = True
            em = discord.Embed(title="User has not played bloxflip", color=0xAE00FF)
            await interaction.response.send_message(embed=em)
            return 0
    if failed == True:
        if sent == False:
            em = discord.Embed(title="Something failed try again", color=0x7520FF)
            await interaction.response.send_message(embed=em)
            return 0
    em = discord.Embed(color=0xAE00FF)
    em.add_field(name="**UserID**", value=f"```{userID}```")
    em.add_field(name="**Rank**", value=f"```{rank}```")
    em.add_field(name="**Total Wagered**", value=f"```{wagered}```" + "\n")
    em.add_field(name="**Games Played**", value=f"```{games_played}```")
    em.add_field(name="**Rain Winnings**",value=f"```{str(rain_winnings)}```")
    em.add_field(name="**Trivia Winnings**",value=f"```{str(trivia_Winnings)}```")
    await interaction.response.send_message(embed=em)

client.run('discord bot token')
