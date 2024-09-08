import os

import discord
from discord.ext import commands
import random
import string
import sqlite3

# SQLite Datenbankverbindung einrichten
conn = sqlite3.connect('data/roles.db')
c = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
c.execute('''
    CREATE TABLE IF NOT EXISTS role_tokens (
        token TEXT PRIMARY KEY,
        role_name TEXT,
        uses_left INTEGER
    )
''')
conn.commit()

# Discord Bot Setup
intents = discord.Intents.default()
intents.members = True  # Um Rollen zuzuweisen, benötigen wir die Berechtigung für Mitglieder
bot = commands.Bot(command_prefix="/", intents=intents)


# Hilfsfunktion zum Erzeugen eines zufälligen Tokens
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


# Funktion, um den Server und die Rolle basierend auf der DM zu finden
async def find_guild_and_role(ctx, role_name):
    if not ctx.author.mutual_guilds:
        await ctx.send("Ich konnte keinen gemeinsamen Server finden, auf dem du bist.")
        return None, None

    # Den ersten gemeinsamen Server nehmen
    guild = ctx.author.mutual_guilds[0]  # Falls der Benutzer auf mehreren Servern ist, nimm den ersten
    role = discord.utils.get(guild.roles, name=role_name)

    if role is None and role_name is not None:
        await ctx.send(f"Die Rolle '{role_name}' existiert nicht auf dem Server '{guild.name}'.")
        return None, None

    return guild, role


# Funktion zur Überprüfung der Administrator-Berechtigung
async def check_admin_permissions(ctx):
    guild, _ = await find_guild_and_role(ctx, None)
    if guild is None:
        return False

    member = guild.get_member(ctx.author.id)
    if member is None:
        await ctx.send("Du bist kein Mitglied auf dem Server.")
        return False
    print(member.guild_permissions)
    print(guild)
    if member.guild_permissions.administrator:
        return True
    else:
        await ctx.send("Du benötigst Administrator-Berechtigungen, um diesen Befehl auszuführen.")
        return False


# Befehl zum Hinzufügen eines Tokens und Verknüpfen mit einer Rolle (nur Admins)
@bot.command()
async def add_role_token(ctx, role_name: str, uses: int = 1):
    if not await check_admin_permissions(ctx):
        return

    token = generate_token()

    # Token und Rolle in die Datenbank einfügen
    c.execute('INSERT INTO role_tokens (token, role_name, uses_left) VALUES (?, ?, ?)', (token, role_name, uses))
    conn.commit()

    await ctx.send(f"Ein Token für die Rolle '{role_name}' wurde erstellt: {token} (verbleibende Nutzungen: {uses})")


# Befehl zum Einlösen eines Tokens und Rolle zuweisen (kann in einer DM genutzt werden)
@bot.command(name="redeem", help="Löse einen Token ein, um eine Rolle zu erhalten")
async def redeem(ctx, token: str):
    # Token in der Datenbank suchen
    c.execute('SELECT role_name, uses_left FROM role_tokens WHERE token = ?', (token,))
    result = c.fetchone()

    if result is None:
        await ctx.send("Ungültiger Token.")
    else:
        role_name, uses_left = result

        if uses_left <= 0:
            await ctx.send("Dieser Token wurde bereits vollständig eingelöst.")
        else:
            guild, role = await find_guild_and_role(ctx, role_name)
            if guild is None or role is None:
                return

            # Dem Benutzer die Rolle auf dem entsprechenden Server zuweisen
            member = guild.get_member(ctx.author.id)
            if member:
                await member.add_roles(role)
                await ctx.send(f"Du hast erfolgreich die Rolle '{role_name}' auf dem Server '{guild.name}' erhalten!")

                # Nutzungen des Tokens verringern
                uses_left -= 1
                if uses_left <= 0:
                    c.execute('DELETE FROM role_tokens WHERE token = ?', (token,))
                else:
                    c.execute('UPDATE role_tokens SET uses_left = ? WHERE token = ?', (uses_left, token))
                conn.commit()
            else:
                await ctx.send(f"Du bist kein Mitglied auf dem Server '{guild.name}'.")


# Befehl zum Anzeigen der aktuellen Tokens (nur Admins)
@bot.command()
async def show_tokens(ctx):
    if not await check_admin_permissions(ctx):
        return

    c.execute('SELECT token, role_name, uses_left FROM role_tokens')
    tokens = c.fetchall()

    if len(tokens) == 0:
        await ctx.send("Es gibt derzeit keine aktiven Tokens.")
    else:
        response = "Aktive Tokens:\n"
        for token, role_name, uses_left in tokens:
            response += f"Token: {token} | Rolle: {role_name} | Verbleibende Nutzungen: {uses_left}\n"
        await ctx.send(response)


# Befehl zum Löschen eines Tokens (nur Admins)
@bot.command()
async def delete_token(ctx, token: str):
    if not await check_admin_permissions(ctx):
        return

    c.execute('DELETE FROM role_tokens WHERE token = ?', (token,))
    conn.commit()

    if c.rowcount == 0:
        await ctx.send("Kein solcher Token gefunden.")
    else:
        await ctx.send(f"Token '{token}' wurde erfolgreich gelöscht.")


# Bot starten (füge hier deinen eigenen Token ein)

bot.run(os.environ.get("DISCORD_TOKEN"))
