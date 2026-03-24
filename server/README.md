# Kabootar DNS Guide

This file is only about the server side.
The server has no frontend and no desktop build. Its main job is to run the DNS bridge and serve channel data to clients.

## Requirements

- Python 3.13
- Network access for running the DNS bridge
- Optional proxy access if the server needs help reaching Telegram

## Setup

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If you are on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
py manage.py dns-bridge-server
```

Or on Linux:

```bash
.venv/bin/python manage.py dns-bridge-server
```

## Important Settings

Sample configuration is in `.env.example`. The main settings are:

- `DNS_DOMAIN` for the domain the server answers on
- `DNS_PORT` for the bind port of the bridge
- `DNS_ACCESS_MODE` for `free` or `fixed`
- `DNS_PASSWORD` for optional domain password protection
- `TELEGRAM_CHANNELS` for forced channels in `fixed` mode
- `TELEGRAM_PROXIES` for Telegram proxy access

## Notes

- The server is only for DNS mode. Direct mode belongs to the client.
- The server does not produce EXE or APK outputs.
- If you want it to stay up permanently, run it under `systemd` or another service manager.
- Server state and database live under `data/` unless you override the path.
