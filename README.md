# Digitalització d'un Taller Mecànic Connectat

Projecte del mòdul 1665 Digitalització. Sistema de gestió de clients, vehicles i cites per a un taller mecànic, amb base de dades, API REST i interfície web.

**Autors:** Jan Bote i Joan Molina  
**Curs:** 2025-2026

---

## Què fa aquest projecte

- Gestió de clients i els seus vehicles
- Creació i consulta de cites des d'una web
- API REST per accedir a les dades
- Scripts d'automatització (còpia de seguretat i comprovació d'estat)

## Estructura

```
projecte-taller/
├── api/
│   ├── app.py              # API Flask (backend amb MariaDB)
│   ├── requirements.txt
│   └── Dockerfile
├── web/
│   ├── index.html          # Interfície web
│   ├── css/style.css
│   ├── js/script.js
│   └── Dockerfile
├── scripts/
│   ├── backup.sh           # Còpia de seguretat de la BD
│   └── check_services.sh   # Comprovació d'estat dels serveis
├── app_local.py            # Versió local amb SQLite (sense Docker)
├── docker-compose.yml
├── db_schema.sql           # Esquema i dades de prova
└── taller.db               # Base de dades SQLite (versió local)
```

## Com executar-ho (versió local)

Requisits: Python 3 instal·lat.

```bash
pip install flask
python app_local.py
```

- Web: http://localhost:5000
- API clients: http://localhost:5000/clients
- API vehicles: http://localhost:5000/vehicles
- API cites: http://localhost:5000/appointments

## Com executar-ho (Docker)

Requisits: Docker i Docker Compose instal·lats.

```bash
docker-compose up --build
```

- Web: http://localhost:8080
- API: http://localhost:5000

> Nota: la versió Docker va estar en desenvolupament però es recomana usar la versió local per garantir el funcionament.

## API - Endpoints

| Mètode | Ruta | Descripció |
|--------|------|------------|
| GET | /clients | Llista tots els clients |
| GET | /vehicles | Llista tots els vehicles |
| GET | /appointments | Llista totes les cites |
| POST | /appointments | Crea una nova cita |
| DELETE | /appointments/\<id\> | Elimina una cita |

### Exemple POST /appointments

```json
{
  "client_id": 1,
  "vehicle_id": 1,
  "data_cita": "2026-06-10",
  "servei_sollicitat": "Canvi d'oli"
}
```

## Base de dades

Tres taules: `clients`, `vehicles` i `cites`. El fitxer `db_schema.sql` inclou l'esquema complet i dades de prova (5 clients, 6 vehicles, 7 cites).

## Scripts

```bash
# Còpia de seguretat
bash scripts/backup.sh

# Comprovació d'estat dels contenidors
bash scripts/check_services.sh
```
