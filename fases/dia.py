import asyncio
from discord.ext import commands

fase_dia_activa = False
votos = {}

async def fase_de_dia(bot, jugadores_vivos, roles_asignados):
    global fase_dia_activa, votos
    fase_dia_activa = True
    votos = {}

    # Buscar un canal para enviar los mensajes
    canal = None
    for guild in bot.guilds:
        if guild.system_channel:
            canal = guild.system_channel
            break

    if canal:
        await canal.send("☀️ Ha amanecido. ¡Comienza la fase de día!")
        await canal.send("Usen `!votar @jugador` para votar por quién eliminar.")
        await canal.send("⏳ Tienen 30 segundos para votar.")

    await asyncio.sleep(30)

    # Conteo de votos
    if votos:
        conteo = {}
        for jugador in votos.values():
            conteo[jugador] = conteo.get(jugador, 0) + 1

        eliminado = max(conteo, key=conteo.get)
        if canal:
            await canal.send(f"🔨 {eliminado.mention} ha sido eliminado por mayoría de votos.")

        jugadores_vivos.remove(eliminado)
        if eliminado in roles_asignados:
            del roles_asignados[eliminado]

    else:
        if canal:
            await canal.send("😶 Nadie fue eliminado hoy.")

    fase_dia_activa = False

    # Reiniciar con la siguiente noche
    from fases.noche import fase_de_noche
    await fase_de_noche(bot, jugadores_vivos, roles_asignados)

@commands.command()
async def votar(ctx, jugador: commands.MemberConverter):
    global votos, fase_dia_activa

    if not fase_dia_activa:
        await ctx.send("❌ No es la fase de día o las votaciones aún no están activas.")
        return

    votos[ctx.author] = jugador
    await ctx.send(f"✅ {ctx.author.display_name} ha votado por {jugador.display_name}.")
