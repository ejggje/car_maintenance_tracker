-- Run this against your car_maintenance database BEFORE starting the app
-- Default admin login: admin@carmaintenance.com / admin123

-- 1. Add 'admin' to the role column
ALTER TABLE user MODIFY COLUMN role ENUM('owner', 'servicer', 'admin') NOT NULL DEFAULT 'owner';

-- 2. Insert the admin user (password: admin123)
INSERT INTO user (first_name, last_name, email, password_hash, role, is_active)
VALUES ('Admin', 'User', 'admin@carmaintenance.com', 'pbkdf2:sha256:1000000$ZDzqGJN7cSfaD15J$364b04c2624300d5eedde11c8f20ce3cf98085b419c6c6116950f5dd2ff82dc3', 'admin', 1);

-- 3. Run hash_existing_users.py next to re-hash all other users.