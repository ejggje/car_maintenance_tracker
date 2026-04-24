from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")

# ─── DB ─────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="car_maintenance"
    )

# ─── DECORATORS ─────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ─── AUTH ───────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE email = %s AND is_active = 1", (email,))
        user = cursor.fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['name'] = user['first_name']
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']
        if new != confirm:
            flash('New passwords do not match.')
            return render_template('change_password.html')
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        if not check_password_hash(user['password_hash'], current):
            db.close()
            flash('Current password is incorrect.')
            return render_template('change_password.html')
        cursor2 = db.cursor()
        cursor2.execute(
            "UPDATE user SET password_hash = %s WHERE user_id = %s",
            (generate_password_hash(new, method='pbkdf2:sha256'), session['user_id'])
        )
        db.commit()
        db.close()
        flash('Password updated successfully.')
        return redirect(url_for('dashboard'))
    return render_template('change_password.html')

# ─── DASHBOARD ROUTER ───────────────────────────────
@app.route('/')
@login_required
def dashboard():
    role = session.get('role')
    if role == 'admin':
        return render_template('index.html')
    elif role == 'owner':
        return redirect(url_for('owner_dashboard'))
    elif role == 'servicer':
        return redirect(url_for('servicer_dashboard'))
    return redirect(url_for('login'))

# ─── OWNER DASHBOARD ────────────────────────────────
@app.route('/owner/dashboard')
@role_required('owner')
def owner_dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    uid = session['user_id']
    cursor.execute("SELECT * FROM vehicle WHERE user_id = %s", (uid,))
    vehicles = cursor.fetchall()
    cursor.execute("""
        SELECT mr.*, v.make, v.model, mt.name as type_name, sf.name as facility_name
        FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        JOIN maintenance_type mt ON mr.maintenance_type_id = mt.maintenance_type_id
        LEFT JOIN service_facility sf ON mr.facility_id = sf.facility_id
        WHERE v.user_id = %s
        ORDER BY mr.service_date DESC
    """, (uid,))
    records = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility ORDER BY name")
    facilities = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type ORDER BY name")
    types = cursor.fetchall()
    db.close()
    return render_template('owner_dashboard.html',
                           vehicles=vehicles, records=records,
                           facilities=facilities, types=types)

@app.route('/owner/vehicles/add', methods=['POST'])
@role_required('owner')
def owner_add_vehicle():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO vehicle (user_id, vin, make, model, year, current_mileage) VALUES (%s, %s, %s, %s, %s, %s)",
        (session['user_id'], request.form['vin'], request.form['make'],
         request.form['model'], request.form['year'], request.form['current_mileage'])
    )
    db.commit()
    db.close()
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/vehicles/delete/<int:vehicle_id>')
@role_required('owner')
def owner_delete_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
    v = cursor.fetchone()
    if v and v['user_id'] == session['user_id']:
        cursor2 = db.cursor()
        cursor2.execute("DELETE FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
        db.commit()
    db.close()
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/records/add', methods=['POST'])
@role_required('owner')
def owner_add_record():
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
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/records/delete/<int:record_id>')
@role_required('owner')
def owner_delete_record(record_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.user_id FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        WHERE mr.maintenance_record_id = %s
    """, (record_id,))
    row = cursor.fetchone()
    if row and row['user_id'] == session['user_id']:
        cursor2 = db.cursor()
        cursor2.execute("DELETE FROM maintenance_record WHERE maintenance_record_id = %s", (record_id,))
        db.commit()
    db.close()
    return redirect(url_for('owner_dashboard'))

# ─── SERVICER DASHBOARD ─────────────────────────────
@app.route('/servicer/dashboard')
@role_required('servicer')
def servicer_dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT mr.*, v.make, v.model, v.year, mt.name as type_name,
               sf.name as facility_name, sf.address as facility_address
        FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        JOIN maintenance_type mt ON mr.maintenance_type_id = mt.maintenance_type_id
        JOIN service_facility sf ON mr.facility_id = sf.facility_id
        ORDER BY mr.service_date DESC
    """)
    records = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility ORDER BY name")
    facilities = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type ORDER BY name")
    types = cursor.fetchall()
    db.close()
    return render_template('servicer_dashboard.html',
                           records=records, facilities=facilities, types=types)

@app.route('/servicer/records/add', methods=['POST'])
@role_required('servicer')
def servicer_add_record():
    db = get_db()
    cursor = db.cursor()
    cost = request.form['cost'] if request.form['cost'] else None
    cursor.execute(
        """INSERT INTO maintenance_record
        (vehicle_id, maintenance_type_id, facility_id, service_date, mileage_at_service, cost, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (request.form['vehicle_id'], request.form['maintenance_type_id'],
         request.form['facility_id'], request.form['service_date'],
         request.form['mileage_at_service'], cost, request.form['notes'])
    )
    db.commit()
    db.close()
    return redirect(url_for('servicer_dashboard'))

# ─── REPORTS (all roles) ─────────────────────────────
@app.route('/reports')
@login_required
def reports():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.make, v.model, v.year,
               COUNT(mr.maintenance_record_id) AS total_services,
               SUM(mr.cost) AS total_spent
        FROM vehicle v
        JOIN maintenance_record mr ON v.vehicle_id = mr.vehicle_id
        GROUP BY v.vehicle_id, v.make, v.model, v.year
        ORDER BY total_spent DESC
    """)
    cost_report = cursor.fetchall()
    cursor.execute("""
        SELECT mt.name AS service_type,
               COUNT(mr.maintenance_record_id) AS times_performed,
               AVG(mr.cost) AS average_cost
        FROM maintenance_type mt
        JOIN maintenance_record mr ON mt.maintenance_type_id = mr.maintenance_type_id
        GROUP BY mt.maintenance_type_id, mt.name
        ORDER BY times_performed DESC
    """)
    frequency_report = cursor.fetchall()
    db.close()
    return render_template('reports.html',
                           cost_report=cost_report,
                           frequency_report=frequency_report)

# ─── ADMIN: USERS ───────────────────────────────────
@app.route('/users')
@admin_required
def users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    all_users = cursor.fetchall()
    db.close()
    return render_template('users.html', users=all_users)

@app.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    db = get_db()
    cursor = db.cursor()
    hashed = generate_password_hash(request.form['password_hash'], method='pbkdf2:sha256')
    cursor.execute(
        "INSERT INTO user (first_name, last_name, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s, %s)",
        (request.form['first_name'], request.form['last_name'], request.form['email'],
         hashed, request.form['role'], 1)
    )
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/users/delete/<int:user_id>')
@admin_required
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
    db.commit()
    db.close()
    return redirect(url_for('users'))

@app.route('/users/edit/<int:user_id>')
@admin_required
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM user")
    all_users = cursor.fetchall()
    db.close()
    return render_template('users.html', edit_user=user, users=all_users)

@app.route('/users/update/<int:user_id>', methods=['POST'])
@admin_required
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

# ─── ADMIN: VEHICLES ────────────────────────────────
@app.route('/vehicles')
@admin_required
def vehicles():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, u.first_name, u.last_name
        FROM vehicle v JOIN user u ON v.user_id = u.user_id
    """)
    all_vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM user")
    all_users = cursor.fetchall()
    db.close()
    return render_template('vehicles.html', vehicles=all_vehicles, users=all_users)

@app.route('/vehicles/add', methods=['POST'])
@admin_required
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
@admin_required
def delete_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
    db.commit()
    db.close()
    return redirect(url_for('vehicles'))

@app.route('/vehicles/edit/<int:vehicle_id>')
@admin_required
def edit_vehicle(vehicle_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle WHERE vehicle_id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    cursor.execute("SELECT * FROM user")
    all_users = cursor.fetchall()
    cursor.execute("SELECT v.*, u.first_name, u.last_name FROM vehicle v JOIN user u ON v.user_id = u.user_id")
    all_vehicles = cursor.fetchall()
    db.close()
    return render_template('vehicles.html', edit_vehicle=vehicle, users=all_users, vehicles=all_vehicles)

@app.route('/vehicles/update/<int:vehicle_id>', methods=['POST'])
@admin_required
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

# ─── ADMIN: RECORDS ─────────────────────────────────
@app.route('/records')
@admin_required
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
    all_records = cursor.fetchall()
    cursor.execute("SELECT * FROM vehicle")
    all_vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type")
    all_types = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility")
    all_facilities = cursor.fetchall()
    db.close()
    return render_template('maintenance_records.html', records=all_records,
                           vehicles=all_vehicles, types=all_types, facilities=all_facilities)

@app.route('/records/add', methods=['POST'])
@admin_required
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
@admin_required
def delete_record(record_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM maintenance_record WHERE maintenance_record_id = %s", (record_id,))
    db.commit()
    db.close()
    return redirect(url_for('records'))

@app.route('/records/edit/<int:record_id>')
@admin_required
def edit_record(record_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_record WHERE maintenance_record_id = %s", (record_id,))
    record = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle")
    all_vehicles = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_type")
    all_types = cursor.fetchall()
    cursor.execute("SELECT * FROM service_facility")
    all_facilities = cursor.fetchall()
    cursor.execute("""
        SELECT mr.*, v.make, v.model, mt.name as type_name, sf.name as facility_name
        FROM maintenance_record mr
        JOIN vehicle v ON mr.vehicle_id = v.vehicle_id
        JOIN maintenance_type mt ON mr.maintenance_type_id = mt.maintenance_type_id
        LEFT JOIN service_facility sf ON mr.facility_id = sf.facility_id
    """)
    all_records = cursor.fetchall()
    db.close()
    return render_template('maintenance_records.html', edit_record=record,
                           vehicles=all_vehicles, types=all_types, facilities=all_facilities, records=all_records)

@app.route('/records/update/<int:record_id>', methods=['POST'])
@admin_required
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

# ─── ADMIN: TYPES ────────────────────────────────────
@app.route('/types')
@admin_required
def types():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_type")
    all_types = cursor.fetchall()
    db.close()
    return render_template('maintenance_types.html', types=all_types)

@app.route('/types/add', methods=['POST'])
@admin_required
def add_type():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO maintenance_type (name, description, default_interval_miles, default_interval_days) VALUES (%s, %s, %s, %s)",
        (request.form['name'], request.form['description'],
         request.form['default_interval_miles'] or None,
         request.form['default_interval_days'] or None)
    )
    db.commit()
    db.close()
    return redirect(url_for('types'))

@app.route('/types/delete/<int:type_id>')
@admin_required
def delete_type(type_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM maintenance_type WHERE maintenance_type_id = %s", (type_id,))
    db.commit()
    db.close()
    return redirect(url_for('types'))

@app.route('/types/edit/<int:type_id>')
@admin_required
def edit_type(type_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM maintenance_type WHERE maintenance_type_id = %s", (type_id,))
    type_ = cursor.fetchone()
    cursor.execute("SELECT * FROM maintenance_type")
    all_types = cursor.fetchall()
    db.close()
    return render_template('maintenance_types.html', edit_type=type_, types=all_types)

@app.route('/types/update/<int:type_id>', methods=['POST'])
@admin_required
def update_type(type_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE maintenance_type SET name=%s, description=%s, default_interval_miles=%s, default_interval_days=%s WHERE maintenance_type_id=%s",
        (request.form['name'], request.form['description'],
         request.form['default_interval_miles'] or None,
         request.form['default_interval_days'] or None, type_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('types'))

if __name__ == '__main__':
    app.run(debug=True)