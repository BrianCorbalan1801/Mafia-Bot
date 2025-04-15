import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
 
partida_activa = False
jugadores_objetivo = 0
jugadores = []
roles = ["Mafioso", "Ciudadano", "Ciudadano", "Doctor", "Detective"]
fase_noche = False
mafia_objetivo = None

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.group()
async def mafia(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Comando inválido. Usá `!mafia crear <n>` o `!mafia unirme`.")

@mafia.command()
async def crear(ctx, n: int):
    global partida_activa, jugadores_objetivo, jugadores

    if partida_activa:
        await ctx.send("Ya hay una partida en curso.")
        return

    if n < 4:
        await ctx.send("La partida necesita al menos 4 jugadores.")
        return

    partida_activa = True
    jugadores_objetivo = n
    jugadores = []

    await ctx.send(f"🎲 Se ha creado una partida de Mafia para {n} jugadores. Usá `!mafia unirme` para participar.")

@mafia.command()
async def unirme(ctx):
    global jugadores

    if not partida_activa:
        await ctx.send("No hay ninguna partida creada. Usá `!mafia crear <n>` primero.")
        return

    if ctx.author in jugadores:
        await ctx.send("Ya estás en la partida.")
        return

    jugadores.append(ctx.author)
    await ctx.send(f"{ctx.author.name} se ha unido. Jugadores actuales: {len(jugadores)}/{jugadores_objetivo}")

    if len(jugadores) == jugadores_objetivo:
        await asignar_roles()

async def asignar_roles():
    global partida_activa, jugadores

    roles_disponibles = generar_roles(len(jugadores))
    random.shuffle(jugadores)
    random.shuffle(roles_disponibles)

    for jugador, rol in zip(jugadores, roles_disponibles):
        try:
            await jugador.send(f"🎭 Tu rol es **{rol}**.")
        except discord.Forbidden:
            print(f"No pude enviar DM a {jugador.name}.")

    canal = jugadores[0].guild.system_channel
    if canal:
        await canal.send("🔒 Todos los jugadores recibieron su rol por privado. ¡La partida comienza!")
    
    await fase_de_noche()

    partida_activa = False
    jugadores = []

def generar_roles(n):
    base = ["Mafioso", "Doctor", "Detective"]
    ciudadanos = n - len(base)
    return base + ["Ciudadano"] * ciudadanos


async def fase_de_noche():
    global fase_noche, mafia_objetivo

    fase_noche = True
    mafiosos = [jugador for jugador in jugadores if "Mafioso" in await obtener_rol(jugador)]
    await notificar_fase_noche(mafiosos)


    while fase_noche:
        await asyncio.sleep(10) 

    if mafia_objetivo:
        await procesar_muerte(mafia_objetivo)

async def obtener_rol(jugador):

    return "Mafioso" if "Mafioso" in jugadores else "Ciudadano"

async def notificar_fase_noche(mafiosos):

    for mafioso in mafiosos:
        try:
            await mafioso.send("🌙 Es la fase de Noche. Usen `!matar <jugador>` para eliminar a alguien.")
        except discord.Forbidden:
            print(f"No pude enviar DM a {mafioso.name}.")
            
    print("Fase de Noche iniciada. Los mafiosos pueden elegir a quién eliminar.")

@bot.command()
async def matar(ctx, objetivo: discord.Member):
    global mafia_objetivo, fase_noche

    if not fase_noche:
        await ctx.send("No es la fase de Noche. Espera a que los mafiosos elijan.")
        return

    if "Mafioso" not in await obtener_rol(ctx.author):
        await ctx.send("¡Solo los mafiosos pueden usar este comando!")
        return

    mafia_objetivo = objetivo
    await ctx.send(f"Los mafiosos han elegido a {objetivo.name}. Se procesará al amanecer.")
    fase_noche = False  

async def procesar_muerte(jugador):
    canal = jugador.guild.system_channel
    if canal:
        await canal.send(f"{jugador.name} ha sido eliminado por los mafiosos durante la Noche.")

bot.run("MTM1ODgxNzcyMTY1OTQyNDkzOQ.Gm6LeZ.Iihd9MHpW1qQ1-_jMcw06PIZ7f0k1TWI0c7HWE")
