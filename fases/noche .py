import asyncio

acciones_noche = {}

async def fase_de_noche(bot, jugadores_vivos, roles_asignados):
    acciones_noche.clear()

    canal = None
    for guild in bot.guilds:
        if guild.system_channel:
            canal = guild.system_channel
            break

    if canal:
        await canal.send("🌙 Comienza la fase de noche. Mafioso, Doctor: revisen sus DMs. Tienen 15 segundos...")

    # Enviar mensajes privados para que actúen
    for jugador in jugadores_vivos:
        rol = roles_asignados.get(jugador)
        if rol == "mafioso":
            try:
                await jugador.send("🔪 Eres el mafioso. Usa `!matar @jugador` en el servidor para elegir a tu víctima.")
            except:
                pass
        elif rol == "doctor":
            try:
                await jugador.send("💉 Eres el doctor. Usa `!curar @jugador` en el servidor para intentar salvar a alguien.")
            except:
                pass

    await asyncio.sleep(15)

    victima = acciones_noche.get("matar")
    salvado = acciones_noche.get("curar")

    canal_info = None
    for guild in bot.guilds:
        if guild.system_channel:
            canal_info = guild.system_channel
            break

    if victima and victima != salvado:
        jugadores_vivos.remove(victima)
        if victima in roles_asignados:
            del roles_asignados[victima]
        if canal_info:
            await canal_info.send(f"💀 Durante la noche, {victima.display_name} fue eliminado.")
    else:
        if canal_info:
            await canal_info.send("✨ Nadie murió esta noche.")

    from fases.dia import fase_de_dia
    await fase_de_dia(bot, jugadores_vivos, roles_asignados)
