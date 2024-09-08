# 100% chatgpt generated, use at your own risk (including readme)


# Discord Role Token Bot

Ein Discord-Bot, der es Admins ermöglicht, Tokens zu erstellen, die Benutzer einlösen können, um bestimmte Rollen auf einem Discord-Server zu erhalten. Der Bot unterstützt auch die Verwendung von SQLite für die Token-Verwaltung und ist so konfiguriert, dass er in einem Docker-Container ausgeführt werden kann.

## Features

- **Admin-Funktionen**:
  - Tokens für Rollen erstellen
  - Aktive Tokens anzeigen
  - Tokens löschen
  
- **Benutzerfunktionen**:
  - Tokens einlösen, um Rollen auf einem Server zu erhalten
  - Unterstützung für direkte Nachrichten (DM), um Tokens privat einzulösen
  
## Voraussetzungen

- Python 3.9 oder höher
- Discord-Bot-Token
- Docker (optional, für containerisierte Ausführung)

## Installation

### Lokale Ausführung

1. **Repository klonen**:

    ```bash
    git clone https://github.com/dein-repository/discord-role-token-bot.git
    cd discord-role-token-bot
    ```

2. **Abhängigkeiten installieren**:

    Stelle sicher, dass Python und `pip` installiert sind. Installiere dann die benötigten Python-Pakete:

    ```bash
    pip install -r requirements.txt
    ```

3. **Bot starten**:

    Erstelle eine Umgebungsvariable für den Bot-Token oder füge den Token direkt im Skript ein:

    ```bash
    export DISCORD_TOKEN=your_token_here
    python bot.py
    ```

### Docker-Ausführung

1. **Docker-Image bauen**:

    ```bash
    docker build -t discord-bot .
    ```

2. **Container starten**:

    ```bash
    docker run -d --name my-discord-bot -e DISCORD_TOKEN=your_token_here discord-bot
    ```

   Optional kannst du ein Volume für die persistente Speicherung der SQLite-Datenbank hinzufügen:

    ```bash
    docker run -d --name my-discord-bot -e DISCORD_TOKEN=your_token_here -v $(pwd)/data:/usr/src/app/data discord-bot
    ```

## Verwendung

### Admin-Befehle

1. **Token erstellen**:

    ```bash
    /add_role_token {role_name} {uses}
    ```

    - `role_name`: Der Name der Rolle, die mit dem Token verknüpft ist.
    - `uses`: Optional. Die Anzahl der Nutzungen, die für den Token zulässig sind (Standardwert: 1).

    Beispiel:
    
    ```bash
    /add_role_token Member 5
    ```

    Erstellt einen Token, der bis zu 5 Mal verwendet werden kann, um die Rolle "Member" zu erhalten.

2. **Aktive Tokens anzeigen**:

    ```bash
    /show_tokens
    ```

    Zeigt eine Liste der aktiven Tokens und ihrer verbleibenden Nutzungen an.

3. **Token löschen**:

    ```bash
    /delete_token {token}
    ```

    - `token`: Der zu löschende Token.

    Beispiel:

    ```bash
    /delete_token abc123xyz
    ```

    Löscht den Token `abc123xyz`, sodass er nicht mehr verwendet werden kann.

### Benutzer-Befehle

1. **Token einlösen**:

    ```bash
    /redeem {token}
    ```

    - `token`: Der von einem Admin bereitgestellte Token.

    Beispiel:

    ```bash
    /redeem abc123xyz
    ```

    Löst den Token ein und weist dem Benutzer die verknüpfte Rolle zu.