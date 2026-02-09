# c.speed-tools

Production-grade Discord operations bot for moderation, tickets, staff workflows, levels, economy, anti-abuse, analytics, and owner global actions.

## Features
- Moderation + case auditing
- 4-layer permission model (Discord perms, staff ranks, overrides, owner gate)
- Tickets with atomic claim flow
- Levels/economy scaffolding
- Owner global moderation (global bans + sync)
- Misc operational tools

## Setup
1. Create Discord application + bot in the Discord Developer Portal.
2. Enable intents: **Guilds**, **Guild Members** (for global join enforcement), **Guild Messages** (logging), and **Message Content** if your moderation policies require content scanning.
3. Copy `.env.example` to `.env`.
4. Paste your token into `.env`:
   ```env
   BOT_TOKEN=your_bot_token_here
   DATABASE_URL=sqlite+aiosqlite:///local.db
   OWNER_USER_ID=1275585606688444438
   ```

## Invite scopes
Use `bot` and `applications.commands` scopes with required permissions for moderation and management.

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m cspeed_tools.main
```

## Command sync behavior
- If `DEV_GUILD_ID` is set, commands sync only to that guild.
- Otherwise commands sync globally.

## Deploy (systemd example)
Create `/etc/systemd/system/cspeed-tools.service`:
```ini
[Unit]
Description=c.speed-tools
After=network.target

[Service]
WorkingDirectory=/opt/c.speed-tools
EnvironmentFile=/opt/c.speed-tools/.env
ExecStart=/opt/c.speed-tools/.venv/bin/python -m cspeed_tools.main
Restart=always
User=bot

[Install]
WantedBy=multi-user.target
```

## Global moderation safety model
- Only `OWNER_USER_ID` can run `/owner` commands.
- Global actions require reason and are case/audit logged.
- Per-guild success/failure is reported with partial-failure transparency.
