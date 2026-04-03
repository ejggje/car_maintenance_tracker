# car_maintenance_tracker

## Setup Instructions

### 1. Install dependencies
```pip3 install flask mysql-connector-python python-dotenv```

### 2. Set up the database
- Install MySQL
- Open MySQL Workbench
- Run the ```database_dump.sql``` file to create and populate the database
 - Do this by pasting into text editor in the app, highlighting all text, then hitting lightening icon 

### 3. Create a .env file
Create a file called ```.env``` in the project root with:
DB_PASSWORD=*password_you_created*

### 4. Run the app
python3 app.py

### 5. Open in browser
Go to http://127.0.0.1:5000