# car_maintenance_tracker

## Setup Instructions

### 1. Install dependencies
````pip3 install flask mysql-connector-python python-dotenv werkzeug```

### 2. Set up the database
- Install MySQL
- Open MySQL Workbench
- Run the `database_dump.sql` file to create and populate the database
  - Do this by pasting into the text editor in the app, highlighting all text, then hitting the lightning icon
- Then run `add_admin.sql` the same way to add the admin role and admin user

### 3. Re-hash existing user passwords
Run the following script once to set up passwords for all existing users:
```python3 hash_existing_users.py```

This sets all existing user passwords to `changeme123`. Users can change their password after logging in.

### 4. Create a .env file
Create a file called `.env` in the project root with:
```
DB_PASSWORD=password_you_created
SECRET_KEY=any_random_string
````

### 5. Run the app
````python3 app.py```

### 6. Open in browser
Go to http://127.0.0.1:5000

## Default Accounts
| Email | Password | Role |
|---|---|---|
| admin@carmaintenance.com | admin123 | Admin |
| (any existing user email) | changeme123 | Owner or Servicer |
````