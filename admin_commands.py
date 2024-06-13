import sys
import os
import discord
import subprocess
from discord import app_commands
import database

def setup_admin_commands(client):
    @client.tree.command(name="restart", description="Перезапуск бота", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    async def restart(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Bot is restarting...")
            print(f"Restart command received. Restarting bot with PID {os.getpid()}...")
            subprocess.Popen([sys.executable, "restart_bot.py", str(os.getpid())])
            await client.close()
            os._exit(0)  # Завершаем процесс принудительно
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="channel_remove", description="Удаление канала из списка получаемого опыта", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(channel="Выберите канал для исключения")
    async def channel_remove(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        if interaction.user.guild_permissions.administrator:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                channel_id = channel.id
                client.channels_to_exclude.add(channel_id)
                database.add_excluded_channel(channel_id)
                await interaction.response.send_message(f"Channel {channel_id} removed from XP gain list.", ephemeral=True)
            else:
                await interaction.response.send_message("Вы можете исключать только текстовые или голосовые каналы.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="role_remove", description="Удаление роли из списка получаемого опыта", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(role="Выберите роль для исключения")
    async def role_remove(interaction: discord.Interaction, role: discord.Role):
        if interaction.user.guild_permissions.administrator:
            role_id = role.id
            client.roles_to_exclude.add(role_id)
            database.add_excluded_role(role_id)
            await interaction.response.send_message(f"Role {role_id} removed from XP gain list.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="adm_list", description="Проверка списка исключений", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    async def adm_list(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            excluded_channels = database.get_excluded_channels()
            excluded_roles = database.get_excluded_roles()

            channels = [interaction.guild.get_channel(channel_id) for channel_id in excluded_channels]
            roles = [interaction.guild.get_role(role_id) for role_id in excluded_roles]

            channel_list = "\n".join([channel.name for channel in channels if channel is not None])
            role_list = "\n".join([role.name for role in roles if role is not None])

            response = f"**Роли:**\n{role_list}\n\n**Каналы:**\n{channel_list}"

            await interaction.response.send_message(response, ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="exit", description="Полное выключение бота", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    async def exit(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Bot is shutting down...")
            print(f"Exit command received. Shutting down bot with PID {os.getpid()}...")
            subprocess.Popen([sys.executable, "stop_bot.py", str(os.getpid())])
            await client.close()
            os._exit(0)  # Завершаем процесс принудительно
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="ball", description="Управление специальными баллами", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(type="Выберите действие: add, remove, set", user="Выберите участника", amount="Количество специальных баллов")
    @app_commands.choices(type=[
        app_commands.Choice(name="add", value="add"),
        app_commands.Choice(name="remove", value="remove"),
        app_commands.Choice(name="set", value="set")
    ])
    async def ball(interaction: discord.Interaction, type: str, user: discord.Member, amount: int):
        if interaction.user.guild_permissions.administrator:
            user_id = user.id
            current_points = database.get_special_points(user_id)

            if type == "add":
                new_points = current_points + amount
                database.update_special_points(user_id, new_points)
                await interaction.response.send_message(f"Added {amount} special points to {user.mention}. They now have {new_points} special points.", ephemeral=True)
            elif type == "remove":
                new_points = max(0, current_points - amount)
                database.update_special_points(user_id, new_points)
                await interaction.response.send_message(f"Removed {amount} special points from {user.mention}. They now have {new_points} special points.", ephemeral=True)
            elif type == "set":
                database.update_special_points(user_id, amount)
                await interaction.response.send_message(f"Set {user.mention}'s special points to {amount}.", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid type. Please use 'add', 'remove', or 'set'.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="star", description="Установка картинки для пользователя", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(user="Выберите участника", star="Номер картинки (от 1 до 12)")
    async def star(interaction: discord.Interaction, user: discord.Member, star: int):
        if interaction.user.guild_permissions.administrator:
            if 1 <= star <= 12:
                database.update_star(user.id, star)
                await interaction.response.send_message(f"Updated star for {user.mention} to {star}.", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid star number. Please choose a number between 1 and 12.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="xp", description="Изменение опыта или уровня пользователя", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(type="op для опыта или level для уровня", action="add, remove, set", user="Выберите участника", amount="Количество")
    @app_commands.choices(type=[
        app_commands.Choice(name="op", value="op"),
        app_commands.Choice(name="level", value="level")
    ])
    @app_commands.choices(action=[
        app_commands.Choice(name="add", value="add"),
        app_commands.Choice(name="remove", value="remove"),
        app_commands.Choice(name="set", value="set")
    ])
    async def xp(interaction: discord.Interaction, type: str, action: str, user: discord.Member, amount: int):
        if interaction.user.guild_permissions.administrator:
            user_id = user.id
            if type == "op":
                current_exp = database.get_user_exp(user_id)
                if action == "add":
                    new_exp = current_exp + amount
                    database.update_user_exp(user_id, new_exp)
                    client.exp[user_id] = new_exp
                    client.check_level_up(user_id)
                    await interaction.response.send_message(f"Added {amount} experience points to {user.mention}. They now have {new_exp} experience points.", ephemeral=True)
                elif action == "remove":
                    new_exp = max(0, current_exp - amount)
                    database.update_user_exp(user_id, new_exp)
                    client.exp[user_id] = new_exp
                    client.check_level_up(user_id)
                    await interaction.response.send_message(f"Removed {amount} experience points from {user.mention}. They now have {new_exp} experience points.", ephemeral=True)
                elif action == "set":
                    database.update_user_exp(user_id, amount)
                    client.exp[user_id] = amount
                    client.check_level_up(user_id)
                    await interaction.response.send_message(f"Set {user.mention}'s experience points to {amount}.", ephemeral=True)
                else:
                    await interaction.response.send_message("Invalid action. Please use 'add', 'remove', or 'set'.", ephemeral=True)
            elif type == "level":
                current_level = database.get_user_level(user_id)
                if action == "add":
                    new_level = current_level + amount
                    database.update_user_level(user_id, new_level)
                    client.levels[user_id] = new_level
                    await interaction.response.send_message(f"Added {amount} levels to {user.mention}. They are now level {new_level}.", ephemeral=True)
                elif action == "remove":
                    new_level = max(0, current_level - amount)
                    database.update_user_level(user_id, new_level)
                    client.levels[user_id] = new_level
                    await interaction.response.send_message(f"Removed {amount} levels from {user.mention}. They are now level {new_level}.", ephemeral=True)
                elif action == "set":
                    database.update_user_level(user_id, amount)
                    client.levels[user_id] = amount
                    await interaction.response.send_message(f"Set {user.mention}'s level to {amount}.", ephemeral=True)
                else:
                    await interaction.response.send_message("Invalid action. Please use 'add', 'remove', or 'set'.", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid type. Please use 'op' or 'level'.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)

    @client.tree.command(name="pid", description="Получить PID процесса бота", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    async def pid(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"PID процесса бота: {os.getpid()}", ephemeral=True)
        else:
            await interaction.response.send_message("У вас нет прав на использование этой команды.", ephemeral=True)
