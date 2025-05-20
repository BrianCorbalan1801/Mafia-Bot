import random
import discord

async def asignar_roles(jugadores, bot, roles_asignados):
    roles = ["mafioso", "doctor", "detective"] + ["ciudadano"] * (len(jugadores) - 3)
    random.shuffle(roles)

    for jugador, rol in zip(jugadores, roles):
        roles_asignados[jugador] = rol
        try:
            await jugador.send(f"Tu rol es: **{rol}**")
        except discord.Forbidden:
            print(f"No se pudo enviar el rol a {jugador.display_name}.")