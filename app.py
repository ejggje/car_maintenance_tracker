from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="car_maintenance"
    )

# ─── HOME ───────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─── USERS ──────────────────────────────────────────
@app.route('/users')
def users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    db.close()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['POST'])
def add_user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO user (first_name, last_name, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s, %s)",
        (request.form['first_name'], request.form['last_name'], request.form['email'],
         request.form['password_hash'], request.form['role'], 1)
    )
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/users/edit/<int:user_id>')
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    db.close()
    return render_template('users.html', edit_user=user)

@app.route('/users/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE user SET first_name=%s, last_name=%s, email=%s, role=%s WHERE user_id=%s",
        (request.form['first_name'], request.form['last_name'],
         request.form['email'], request.form['role'], user_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('users'))

# ─── VEHICLES ───────────────────────────────────────
@app.route('/vehicles')
def vehicles():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, u.first_name, u.last_name 
        FROM vehicle v 
        JOIN user u ON v.user_id = u.user_id
    """)
    vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    db.close()
    return render_template('vehicles.html', vehicles=vehicles, users=users)

@app.route('/vehicles/add', methods=['POST'])
def add_vehicle():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO vehicle (user_id, vin, make, model, year, current_mileage) VALUES (%s, %s, %s, %s, %s, %s)",
        (request.form['user_id'], request.form['vin'], request.form['make'],
         request.form['model'], request.form['year'], request.form['current_mileage'])
    )
    db.commit()
    db.close()
    return redirect(url_for('vehicles'))

@app.route('/vehicles/delete/<int:vehicle_id>')
def delete_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
    db.commit()
    db.close()
    return redirect(url_for('vehicles'))

@app.route('/vehicles/edit/<int:vehicle_id>')
def edit_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM vehicle v JOIN user u ON v.user_id = u.user_id")
    vehicles = cursor.fetchall()
    db.close()
    return render_template('vehicles.html', edit_vehicle=vehicle, users=users, vehicles=vehicles)

@app.route('/vehicles/update/<int:vehicle_id>', methods=['POST'])
def update_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE vehicle SET user_id=%s, make=%s, model=%s, year=%s, current_mileage=%s WHERE vehicle_id=%s",
        (request.form['user_id'], request.form['make'], request.form['model'],
         request.form['year'], request.form['current_mileage'], vehicle_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('vehicles'))

# ─── MAINTENANCE RECORDS ────────────────────────────
@app.route('/records')
def records():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT mr.*, v.make, v.model, mt.name as type_name, sf.name as facility_name
        FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        JOIN maintenance_type mt ON mr.maintenance_type_id = mt.maintenance_type_id
        LEFT JOIN service_facility sf ON mr.facility_id = sf.facility_id
    """)
    records = cursor.fetchall()
    cursor.execute("SELECT * FROM vehicle")
    vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type")
    types = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility")
    facilities = cursor.fetchall()
    db.close()
    return render_template('maintenance_records.html', records=records,
                           vehicles=vehicles, types=types, facilities=facilities)

@app.route('/records/add', methods=['POST'])
def add_record():
    db = get_db()
    cursor = db.cursor()
    facility_id = request.form['facility_id'] if request.form['facility_id'] else None
    cost = request.form['cost'] if request.form['cost'] else None
    cursor.execute(
        """INSERT INTO maintenance_record 
        (vehicle_id, maintenance_type_id, facility_id, service_date, mileage_at_service, cost, notes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (request.form['vehicle_id'], request.form['maintenance_type_id'],
         facility_id, request.form['service_date'],
         request.form['mileage_at_service'], cost, request.form['notes'])
    )
    db.commit()
    db.close()
    return redirect(url_for('records'))

@app.route('/records/delete/<int:record_id>')
def delete_record(record_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM maintenance_record WHERE maintenance_record_id = %s", (record_id,))
    db.commit()
    db.close()
    return redirect(url_for('records'))

@app.route('/records/edit/<int:record_id>')
def edit_record(record_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_record WHERE maintenance_record_id = %s", (record_id,))
    record = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle")
    vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type")
    types = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility")
    facilities = cursor.fetchall()
    cursor.execute("""
        SELECT mr.*, v.make, v.model, mt.name as type_name, sf.name as facility_name
        FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        JOIN maintenance_type mt ON mr.maintenance_type_id = mt.maintenance_type_id
        LEFT JOIN service_facility sf ON mr.facility_id = sf.facility_id
    """)
    records = cursor.fetchall()
    db.close()
    return render_template('maintenance_records.html', edit_record=record,
                           vehicles=vehicles, types=types, facilities=facilities, records=records)

@app.route('/records/update/<int:record_id>', methods=['POST'])
def update_record(record_id):
    db = get_db()
    cursor = db.cursor()
    facility_id = request.form['facility_id'] if request.form['facility_id'] else None
    cost = request.form['cost'] if request.form['cost'] else None
    cursor.execute(
        """UPDATE maintenance_record SET vehicle_id=%s, maintenance_type_id=%s,
        facility_id=%s, service_date=%s, mileage_at_service=%s, cost=%s, notes=%s
        WHERE maintenance_record_id=%s""",
        (request.form['vehicle_id'], request.form['maintenance_type_id'],
         facility_id, request.form['service_date'],
         request.form['mileage_at_service'], cost, request.form['notes'], record_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('records'))

# ─── MAINTENANCE TYPES ──────────────────────────────
@app.route('/types')
def types():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_type")
    types = cursor.fetchall()
    db.close()
    return render_template('maintenance_types.html', types=types)

@app.route('/types/add', methods=['POST'])
def add_type():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO maintenance_type (name, description, default_interval_miles, default_interval_days) VALUES (%s, %s, %s, %s)",
        (request.form['name'], request.form['description'],
         request.form['default_interval_miles'], request.form['default_interval_days'])
    )
    db.commit()
    db.close()
    return redirect(url_for('types'))

@app.route('/types/delete/<int:type_id>')
def delete_type(type_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM maintenance_type WHERE maintenance_type_id = %s", (type_id,))
    db.commit()
    db.close()
    return redirect(url_for('types'))

@app.route('/types/edit/<int:type_id>')
def edit_type(type_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_type WHERE maintenance_type_id = %s", (type_id,))
    type_ = cursor.fetchone()
    cursor.execute("SELECT * FROM maintenance_type")
    types = cursor.fetchall()
    db.close()
    return render_template('maintenance_types.html', edit_type=type_, types=types)

@app.route('/types/update/<int:type_id>', methods=['POST'])
def update_type(type_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE maintenance_type SET name=%s, description=%s, default_interval_miles=%s, default_interval_days=%s WHERE maintenance_type_id=%s",
        (request.form['name'], request.form['description'],
         request.form['default_interval_miles'], request.form['default_interval_days'], type_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('types'))

if __name__ == '__main__':
    app.run(debug=True)