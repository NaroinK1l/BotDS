import discord
from discord import app_commands
import database
import os

def setup_user_commands(client):
    @client.tree.command(name="user", description="Проверка статуса пользователя", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(member="Выберите пользователя")
    async def user(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_id = member.id
        exp = database.get_user_exp(user_id)
        level = database.get_user_level(user_id)
        special_points = database.get_special_points(user_id)
        star = database.get_star(user_id)
        birthday = database.get_birthday(user_id)
        
        exp_to_next_level = 300 - exp
        
        embed = discord.Embed(title=f"Статус пользователя {member.display_name}", color=discord.Color.blue())
        embed.add_field(name="Уровень", value=f"{level}", inline=False)
        embed.add_field(name="Опыт", value=f"{exp} / 300", inline=False)
        embed.add_field(name="До следующего уровня", value=f"{exp_to_next_level}", inline=False)
        embed.add_field(name="Специальные баллы", value=f"{special_points}", inline=False)
        if birthday:
            embed.add_field(name="Дата рождения", value=birthday, inline=False)
        
        if star >= 1 and star <= 12:
            file_path = f"stars/{star}.png"
            file = discord.File(file_path, filename=f"{star}.png")
            embed.set_image(url=f"attachment://{star}.png")
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)
