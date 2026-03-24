#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
INTERVAL="${CRON_INTERVAL_MINUTES:-15}"
if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]] || [ "$INTERVAL" -lt 1 ] || [ "$INTERVAL" -gt 59 ]; then
  INTERVAL=15
fi
CMD="cd $(pwd) && ./.venv/bin/python manage.py sync >> ./sync.log 2>&1"
LINE="*/${INTERVAL} * * * * ${CMD}"
( { crontab -l 2>/dev/null || true; } | grep -Fv "manage.py sync"; echo "$LINE" ) | crontab -
echo "Installed cron: $LINE"