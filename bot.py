import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from roles.asignacion import asignar_roles
from fases.noche import fase_de_noche
from fases.dia import fase_de_dia, votar
from fases.noche import acciones_noche

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

partida = {
    "jugadores": [],
    "roles": {},
    "max_jugadores": 0,
    "estado": "esperando"
}

@bot.event
async def on_ready():
    print(f"✅ Conectado correctamente como {bot.user.name}")

@bot.command()
async def mafia(ctx, accion: str, nro: int = None):
    if accion == "crear" and nro:
        partida["jugadores"].clear()
        partida["roles"].clear()
        partida["max_jugadores"] = nro
        partida["estado"] = "esperando"
        await ctx.send(f"🎲 Se ha creado la partida con {nro} jugadores. Únete con `!mafia unirme`.")
    elif accion == "unirme":
        if partida["estado"] != "esperando":
            await ctx.send("No hay una partida disponible para unirse. Usa `!mafia crear <nro>` primero.")
            return
        if ctx.author in partida["jugadores"]:
            await ctx.send("Ya estás en la partida.")
        elif len(partida["jugadores"]) >= partida["max_jugadores"]:
            await ctx.send("La partida ya está completa.")
        else:
            partida["jugadores"].append(ctx.author)
            await ctx.send(f"{ctx.author.mention} se unió a la partida. ({len(partida['jugadores'])}/{partida['max_jugadores']})")
            if len(partida["jugadores"]) == partida["max_jugadores"]:
                partida["estado"] = "jugando"
                await asignar_roles(partida["jugadores"], bot, partida["roles"])
                await fase_de_noche(bot, partida)

@bot.command()
async def matar(ctx, objetivo: discord.Member):
    if roles_asignados.get(ctx.author) != "mafioso":
        await ctx.send("❌ Solo el mafioso puede usar este comando.")
        return
    if objetivo not in jugadores:
        await ctx.send("❌ Ese jugador no está en la partida.")
        return

    acciones_noche["matar"] = objetivo
    await ctx.send(f"🔪 Has elegido matar a {objetivo.display_name}.")


@bot.command()
async def curar(ctx, objetivo: discord.Member):
    if roles_asignados.get(ctx.author) != "doctor":
        await ctx.send("❌ Solo el doctor puede usar este comando.")
        return
    if objetivo not in jugadores:
        await ctx.send("❌ Ese jugador no está en la partida.")
        return

    acciones_noche["curar"] = objetivo
    await ctx.send(f"💉 Has intentado curar a {objetivo.display_name}.")


@bot.command()
async def votar(ctx, jugador: discord.Member):
    await realizar_votacion(ctx, jugador, partida, bot)

bot.run(TOKEN)
