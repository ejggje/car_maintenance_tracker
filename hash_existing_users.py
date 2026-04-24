"""
Default password assigned to all existing non-admin users: changeme123
"""

import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="car_maintenance"
)

cursor = db.cursor(dictionary=True)
cursor.execute("SELECT user_id, email FROM user WHERE role != 'admin'")
users = cursor.fetchall()

update_cursor = db.cursor()
default_password = "changeme123"

for user in users:
    new_hash = generate_password_hash(default_password, method='pbkdf2:sha256')
    update_cursor.execute(
        "UPDATE user SET password_hash = %s WHERE user_id = %s",
        (new_hash, user['user_id'])
    )
    print(f"Re-hashed: {user['email']}")

db.commit()
db.close()
print(f"\nDone. All existing users now have password: {default_password}")
print("log in and use /change-password to set new password.")