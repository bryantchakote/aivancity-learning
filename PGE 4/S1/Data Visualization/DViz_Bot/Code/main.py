from os.path import exists

import discord
from discord.ext import commands

# Our external files
import shotrecap
import compareplayers
import teamsefficiency

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def shot_recap(ctx, first_name, last_name, match_day):
    shotrecap.get_shot_recap(first_name, last_name, match_day)
    path = f'shotrecap_{first_name}_{last_name}_{match_day}.png'
    if exists(path):
        await ctx.channel.send(file=discord.File(path))

@bot.command()
async def compare_players(ctx, first_name_1, last_name_1, first_name_2, last_name_2):
    compareplayers.get_compare_players(first_name_1, last_name_1, first_name_2, last_name_2)
    path = f'compareplayers_{first_name_1}_{last_name_1}_{first_name_2}_{last_name_2}.png'
    if exists(path):
        await ctx.channel.send(file=discord.File(path))

@bot.command()
async def teams_efficiency(ctx):
    teamsefficiency.get_teams_efficiency()
    path = 'teamsefficiency.png'
    if exists(path):
        await ctx.channel.send(file=discord.File(path))

bot.run('MTAzOTgyNjY0MDg4NjMwMDY5Mg.GOeXwN.fzKdAsam5YI89anROR0UeJVcOv2WtMWA27rJOc')
