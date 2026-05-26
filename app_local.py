from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "taller.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telefon TEXT,
            correu TEXT
        );
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            matricula TEXT NOT NULL,
            model TEXT,
            any_fabricacio INTEGER,
            quilometres INTEGER,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        CREATE TABLE IF NOT EXISTS cites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            vehicle_id INTEGER NOT NULL,
            data_cita TEXT NOT NULL,
            servei_sollicitat TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        );
    """)
    # Inserir dades de prova si la BD està buida
    c.execute("SELECT COUNT(*) FROM clients")
    if c.fetchone()[0] == 0:
        c.executescript("""
            INSERT INTO clients (nom, telefon, correu) VALUES
            ('Maria Garcia',  '612 345 678', 'maria.garcia@email.com'),
            ('Joan Puig',     '634 567 890', 'joan.puig@email.com'),
            ('Anna Martinez', '698 123 456', 'anna.martinez@email.com'),
            ('Pere Soler',    '611 987 654', 'pere.soler@email.com'),
            ('Laura Ferrer',  '677 234 567', 'laura.ferrer@email.com');

            INSERT INTO vehicles (client_id, matricula, model, any_fabricacio, quilometres) VALUES
            (1, '1234 ABC', 'Seat Ibiza',      2018, 85000),
            (1, '5678 DEF', 'Toyota Yaris',    2020, 32000),
            (2, '9012 GHI', 'Ford Focus',      2016, 120000),
            (3, '3456 JKL', 'Volkswagen Golf', 2019, 67000),
            (4, '7890 MNO', 'Renault Clio',    2021, 18000),
            (5, '2345 PQR', 'Peugeot 208',     2017, 95000);

            INSERT INTO cites (client_id, vehicle_id, data_cita, servei_sollicitat) VALUES
            (1, 1, '2025-05-26', 'Canvi d oli i filtre'),
            (1, 2, '2025-05-27', 'Revisio frens'),
            (2, 3, '2025-05-28', 'Canvi de pneumatics'),
            (3, 4, '2025-05-29', 'Revisio general ITV'),
            (4, 5, '2025-06-02', 'Reparacio aire condicionat'),
            (5, 6, '2025-06-03', 'Diagnosi electronica'),
            (1, 1, '2025-06-05', 'Canvi bateria');
        """)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    return response

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    conn = get_db()
    vehicles = conn.execute("""
        SELECT v.id, v.matricula, v.model, v.any_fabricacio, v.quilometres,
               c.nom AS client_nom, c.telefon, c.correu
        FROM vehicles v JOIN clients c ON v.client_id = c.id
    """).fetchall()
    conn.close()
    return jsonify([dict(v) for v in vehicles])

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = get_db()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return jsonify([dict(c) for c in clients])

@app.route('/appointments', methods=['GET'])
def get_appointments():
    conn = get_db()
    cites = conn.execute("""
        SELECT ci.id, ci.data_cita, ci.servei_sollicitat,
               v.matricula, v.model,
               cl.nom AS client_nom, cl.telefon
        FROM cites ci
        JOIN vehicles v ON ci.vehicle_id = v.id
        JOIN clients cl ON ci.client_id = cl.id
        ORDER BY ci.data_cita DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(c) for c in cites])

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not data or not all(k in data for k in ['client_id', 'vehicle_id', 'data_cita', 'servei_sollicitat']):
        return jsonify({'error': 'Falten dades obligatories'}), 400
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO cites (client_id, vehicle_id, data_cita, servei_sollicitat) VALUES (?, ?, ?, ?)",
        (data['client_id'], data['vehicle_id'], data['data_cita'], data['servei_sollicitat'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Cita creada correctament', 'id': new_id}), 201

@app.route('/appointments/<int:cita_id>', methods=['DELETE'])
def delete_appointment(cita_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM cites WHERE id = ?", (cita_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Cita no trobada'}), 404
    return jsonify({'message': 'Cita eliminada correctament'})

@app.route('/appointments', methods=['OPTIONS'])
@app.route('/vehicles', methods=['OPTIONS'])
def options():
    return '', 204

if __name__ == '__main__':
    init_db()
    print("\n✅ API arrancada correctament!")
    print("📋 Vehicles:     http://localhost:5000/vehicles")
    print("📅 Cites:        http://localhost:5000/appointments")
    print("👥 Clients:      http://localhost:5000/clients")
    print("\nPrem Ctrl+C per aturar.\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
