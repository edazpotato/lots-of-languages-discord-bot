import discord
from dotenv import load_dotenv
import os
import aiohttp

client = discord.Client()
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
KSOFT_TOKEN = os.getenv("KSOFT_TOKEN")
PREFIX = "."

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await client.change_presence(activity=discord.Game(name="In Python"))

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author.bot:
        return
    if not message.content.startswith(PREFIX):
        return
    args = message.content[len(PREFIX):].split(" ")
    cmd = args[0]
    args = args[1:]


    if cmd == "help":
        help_txt = f"""
My command prefix here is: `{PREFIX}`
List of my commands:
```fix
help  - displays this message
info  - information about me
ban   - ban a memeber
kick  - kick a member
purge - clear messages
meme  - get a random meme (powered by Ksoft.si)
```
        """
        await message.channel.send(help_txt)
    elif cmd == "info":
        info_txt = """
Description of me:
```fix
I'm a discord bot written in 9 different programing languages. You can see which language this version of me is written in below.
I was created by Edaz#5671 in order to try out different programing languages so they can decide which language to re-write their main discord bot in.
```
Technical information about this version of me:
```fix
Programing language:         Python 3
Discord API wrapper library: discord.py
```
        """
        await message.channel.send(info_txt)
    elif cmd == "ban":
        if message.author.guild_permissions.ban_members:
            if message.guild.me.guild_permissions.ban_members:
                try:
                    member = args[0][2:len(args[0])-1]
                    if member.startswith("!"):
                        member = member[1:]
                    member = message.guild.get_member(int(member))
                    await member.ban()
                    await message.channel.send("Successfully banned that member yay!")
                except:
                    await message.channel.send("Something went wrong...\nThe things that might have gone wrong include: ```fix\n- You didn't mention a member\n- I don't have the ban members permission\n- I don't have permission to ban that specific member```")
            else:
                await message.channel.send("I don't have permission to do that :(")
        else:
            await message.channel.send("You aren't allowed to do that :(")
    elif cmd == "kick":
        if message.author.guild_permissions.kick_members:
            if message.guild.me.guild_permissions.kick_members:
                try:
                    member = args[0][2:len(args[0])-1]
                    if member.startswith("!"):
                        member = member[1:]
                    member = message.guild.get_member(int(member))
                    await member.kick()
                    await message.channel.send("Successfully kickeded that member yay!")
                except:
                    await message.channel.send("Something went wrong...\nThe things that might have gone wrong include: ```fix\n- You didn't mention a member\n- I don't have the kick members permission\n- I don't have permission to kick that specific member```")
            else:
                await message.channel.send("I don't have permission to do that :(")
        else:
            await message.channel.send("You aren't allowed to do that :(")
    elif cmd == "purge" or cmd == "clear":
        if message.author.guild_permissions.manage_messages:
            if message.guild.me.guild_permissions.manage_messages:
                try:
                    num = 2
                    if args and args[0]:
                        num = int(args[0]) + 1
                    deleted = await message.channel.purge(limit=num)
                    await message.channel.send(f"Deleted {len(deleted)-1} message(s)", delete_after=3)
                except:
                    await message.channel.send("An error occurred...\nThe things that could have gone wrong include: ```fix\n- You didn't provide a number\n- I can't delete those spcific messages\n- Something else???```")
            else:
                await message.channel.send("I don't have permission to do that :(")
        else:
            await message.channel.send("You aren't allowed to do that :(")
    elif cmd == "meme":
        headers = {"Authorization": f"Bearer {KSOFT_TOKEN}"}
        session = aiohttp.ClientSession()
        resp = await session.get("https://api.ksoft.si/images/random-meme", headers=headers)
        json = await resp.json()
        await session.close()
        embed = discord.Embed()
        embed.set_image(url=json["image_url"])
        embed.color = message.author.color
        embed.title = json["title"]
        embed.url = json["source"]
        await message.channel.send(embed=embed)

client.run(TOKEN)