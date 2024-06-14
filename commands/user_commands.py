import discord
from discord import app_commands
from database import exp, special_points, stars, birthday
import os

def setup_user_commands(client):
    @client.tree.command(name="user", description="Проверка статуса пользователя", guild=discord.Object(id=int(os.getenv('GUILD_ID'))))
    @app_commands.describe(member="Выберите пользователя")
    async def user(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_id = member.id
        user_exp = exp.get_user_exp(user_id)
        user_level = exp.get_user_level(user_id)
        user_special_points = special_points.get_special_points(user_id)
        user_star = stars.get_star(user_id)
        user_birthday = birthday.get_birthday(user_id)
        
        exp_to_next_level = 300 - user_exp
        
        embed = discord.Embed(title=f"Статус пользователя {member.display_name}", color=discord.Color.blue())
        embed.add_field(name="Уровень", value=f"{user_level}", inline=False)
        embed.add_field(name="Опыт", value=f"{user_exp} / 300", inline=False)
        embed.add_field(name="До следующего уровня", value=f"{exp_to_next_level}", inline=False)
        embed.add_field(name="Специальные баллы", value=f"{user_special_points}", inline=False)
        if user_birthday:
            embed.add_field(name="Дата рождения", value=user_birthday, inline=False)
        
        if user_star >= 1 and user_star <= 12:
            file_path = f"stars/{user_star}.png"
            file = discord.File(file_path, filename=f"{user_star}.png")
            embed.set_image(url=f"attachment://{user_star}.png")
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)
