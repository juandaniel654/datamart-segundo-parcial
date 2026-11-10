#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
    python3 - <<'PY'
from pathlib import Path
import secrets

Path(".env").write_text(
    "MYSQL_ROOT_PASSWORD=" + secrets.token_urlsafe(20) + "\n"
    "MYSQL_DATABASE=datamart\n"
    "MYSQL_USER=datamart\n"
    "MYSQL_PASSWORD=" + secrets.token_urlsafe(20) + "\n"
)
PY
    chmod 600 .env
fi

mkdir -p ssh
chmod 700 ssh

if [ ! -f ssh/id_ed25519 ]; then
    ssh-keygen -q -t ed25519 \
      -f ssh/id_ed25519 \
      -N "" \
      -C "examen-hadoop"
fi

cp ssh/id_ed25519.pub ssh/authorized_keys
chmod 600 ssh/id_ed25519 ssh/authorized_keys

echo "Entorno preparado correctamente."
