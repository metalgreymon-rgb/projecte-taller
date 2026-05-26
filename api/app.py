from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="example",
        database="taller"
    )

# GET /vehicles - Llistar tots els vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.id, v.matricula, v.model, v.any_fabricacio, v.quilometres,
               c.nom AS client_nom, c.telefon, c.correu
        FROM vehicles v
        JOIN clients c ON v.client_id = c.id
    """)
    vehicles = cursor.fetchall()
    db.close()
    return jsonify(vehicles)

# GET /clients - Llistar tots els clients
@app.route('/clients', methods=['GET'])
def get_clients():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    db.close()
    return jsonify(clients)

# POST /appointments - Crear una nova cita
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not data or not all(k in data for k in ['client_id', 'vehicle_id', 'data_cita', 'servei_sollicitat']):
        return jsonify({'error': 'Falten dades obligatòries'}), 400
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO cites (client_id, vehicle_id, data_cita, servei_sollicitat) VALUES (%s, %s, %s, %s)",
        (data['client_id'], data['vehicle_id'], data['data_cita'], data['servei_sollicitat'])
    )
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    return jsonify({'message': 'Cita creada correctament', 'id': new_id}), 201

# GET /appointments - Llistar totes les cites
@app.route('/appointments', methods=['GET'])
def get_appointments():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT ci.id, ci.data_cita, ci.servei_sollicitat,
               v.matricula, v.model,
               cl.nom AS client_nom, cl.telefon
        FROM cites ci
        JOIN vehicles v ON ci.vehicle_id = v.id
        JOIN clients cl ON v.client_id = cl.id
        ORDER BY ci.data_cita DESC
    """)
    cites = cursor.fetchall()
    # Convertir dates a string per JSON
    for cita in cites:
        if cita['data_cita']:
            cita['data_cita'] = str(cita['data_cita'])
    db.close()
    return jsonify(cites)

# DELETE /appointments/<id> - Eliminar una cita
@app.route('/appointments/<int:cita_id>', methods=['DELETE'])
def delete_appointment(cita_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cites WHERE id = %s", (cita_id,))
    db.commit()
    affected = cursor.rowcount
    db.close()
    if affected == 0:
        return jsonify({'error': 'Cita no trobada'}), 404
    return jsonify({'message': 'Cita eliminada correctament'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
