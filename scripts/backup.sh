#!/bin/bash
# ============================================
# Script de còpia de seguretat de la BDs
# S'executa cada 24h via cron
# ============================================

BACKUP_DIR="./backups"
DATA=$(date +%Y-%m-%d_%H-%M-%S)
FITXER="$BACKUP_DIR/backup_$DATA.sql"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Iniciant backup..."

docker exec taller-db sh -c 'exec mysqldump --all-databases -uroot -pexample' > "$FITXER"

if [ $? -eq 0 ]; then
    echo "[$(date)] Backup guardat a: $FITXER"
else
    echo "[$(date)] ERROR: El backup ha fallat." >&2
    exit 1
fi

# Eliminar backups de més de 7 dies
find "$BACKUP_DIR" -name "backup_*.sql" -mtime +7 -delete
echo "[$(date)] Backups antics eliminats."

# Per programar execució automàtica cada 24h, afegir al cron:
# 0 2 * * * /ruta/al/projecte/scripts/backup.sh >> /var/log/taller_backup.log 2>&1
