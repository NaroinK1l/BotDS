import os
import sys
import discord
import asyncio
from discord.ext import tasks
from discord import app_commands
from dotenv import load_dotenv
from database import database
from database import exp
from database import special_points
from database import stars
from database import birthday
from database import settings
from commands import admin_commands, user_commands
import autosave

# Загрузка токена и ID сервера из файла .env
load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

# Инициализация базы данных
database.initialize_db()
exp.initialize_exp_db()
special_points.initialize_bot_db()
stars.initialize_bot_db()
birthday.initialize_birthday_db()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.exp = {user_id: exp.get_user_exp(user_id) for user_id in exp.get_all_user_ids()}
        self.levels = {user_id: exp.get_user_level(user_id) for user_id in exp.get_all_user_ids()}
        self.birthday = {user_id: birthday.get_birthday(user_id) for user_id in exp.get_all_user_ids()}
        self.channels_to_exclude = database.get_excluded_channels()
        self.roles_to_exclude = database.get_excluded_roles()

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))
        self.add_exp_voice.start()
        print(f'{self.user} has connected to Discord!')
        print(f'Bot PID: {os.getpid()}')

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id in self.channels_to_exclude or any(role.id in self.roles_to_exclude for role in message.author.roles):
            return

        user_id = message.author.id
        self.exp[user_id] = self.exp.get(user_id, 0) + 10
        self.check_level_up(user_id)

    @tasks.loop(minutes=1)
    async def add_exp_voice(self):
        for guild in self.guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.bot:
                        continue
                    if channel.id in self.channels_to_exclude or any(role.id in self.roles_to_exclude for role in member.roles):
                        continue

                    user_id = member.id
                    self.exp[user_id] = self.exp.get(user_id, 0) + 5
                    self.check_level_up(user_id)

    def check_level_up(self, user_id):
        while self.exp[user_id] >= 300:
            self.exp[user_id] -= 300
            self.levels[user_id] = self.levels.get(user_id, 0) + 1
            current_points = special_points.get_special_points(user_id)
            special_points.update_special_points(user_id, current_points + 40)
        exp.update_user_exp(user_id, self.exp[user_id])
        exp.update_user_level(user_id, self.levels[user_id])

    async def close(self):
        print("Bot is shutting down...")
        for user_id in self.exp.keys():
            exp.update_user_exp(user_id, self.exp[user_id])
            exp.update_user_level(user_id, self.levels[user_id])
            if self.birthday.get(user_id):
                birthday.update_birthday(user_id, self.birthday[user_id])
        await super().close()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True

client = MyClient(intents=intents)

admin_commands.setup_admin_commands(client)
user_commands.setup_user_commands(client)

async def main():
    admin_commands.setup_birthday_notification(client)
    await client.start(TOKEN)
    asyncio.create_task(autosave.main(client))
    print("Bot has started.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is stopping.")
