import discord
import os
from discord.ext import commands

import os
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.presences = True 
intents.members = True   
intents.guilds = True

bot = commands.Bot(command_prefix=lambda bot, msg: ["?", "??", f"<@{bot.user.id}> "], intents=intents)

ROLE_ID = 1432733039808614462  
CHANNEL_ID = 1433993299043156081 

STATUS_TRADUZIDO = {
    "online": "🟢 Online",
    "idle": "🌙 Ausente",
    "dnd": "⛔ Ocupado",
    "offline": "⚫ Offline"
}

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# @bot.command()
# async def sexo(ctx:commands.Context):
#     nome = ctx.author.name
#     await ctx.reply(f"O {nome} é um viadinho gay KKKKKKKKKKKKKKKKKKKKKKK")

@bot.event
async def on_presence_update(before, after):
    if not after.guild:
        return

    role = after.guild.get_role(ROLE_ID)
    if role in after.roles:
        # Detectar entrada (ficou online, idle ou dnd)
        if before.status == discord.Status.offline and after.status in (
            discord.Status.online,
            discord.Status.idle,
            discord.Status.dnd
        ):
            status = STATUS_TRADUZIDO.get(after.status.name, after.status.name)

            # Mensagem no canal
            channel = after.guild.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"@everyone ► {after.display_name} acabou de ficar **{status}**!")

            # Mensagem privada para o usuário
            try:
                await after.send(f"Olá {after.display_name}! Você acabou de ficar **{status}** e foi notificado sobre isso.")
            except discord.Forbidden:
                # Usuário bloqueou DMs do servidor ou do bot
                print(f"❌ Não foi possível enviar DM para {after.display_name}")

        # Detectar saída (ficou offline)
        elif before.status in (
            discord.Status.online,
            discord.Status.idle,
            discord.Status.dnd
        ) and after.status == discord.Status.offline:
            status = STATUS_TRADUZIDO.get(after.status.name, after.status.name)

            # Mensagem no canal
            channel = after.guild.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"@everyone ► {after.display_name} acabou de ficar **{status}**!")

bot.run(token)