-- Створення окремої схеми для проєкту
CREATE SCHEMA IF NOT EXISTS project;

-- Встановлюємо схему за замовчуванням
SET search_path TO project;

-- Створення таблиць проєкту
DROP TABLE IF EXISTS project.order_items;
DROP TABLE IF EXISTS project.appointments;
DROP TABLE IF EXISTS project.orders;
DROP TABLE IF EXISTS project.services;
DROP TABLE IF EXISTS project.clients;
DROP TABLE IF EXISTS project.inventory;

CREATE TABLE IF NOT EXISTS project.clients (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project.services (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    duration INTEGER NOT NULL CHECK (duration > 0),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project.orders (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES project.clients(id)
);

CREATE TABLE IF NOT EXISTS project.order_items (
    order_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (order_id, service_id),
    FOREIGN KEY (order_id) REFERENCES project.orders(id),
    FOREIGN KEY (service_id) REFERENCES project.services(id)
);

CREATE TABLE IF NOT EXISTS project.appointments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_time TIMESTAMP NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES project.clients(id),
    FOREIGN KEY (service_id) REFERENCES project.services(id)
);

CREATE TABLE IF NOT EXISTS project.inventory (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 1. Тестові дані (мінімум 3 рядки на таблицю)
INSERT INTO project.clients (name, phone, email)
VALUES
    ('Олена Коваленко', '+380-67-123-45-67', 'olena@example.com'),
    ('Іван Петренко', '+380-50-987-65-43', 'ivan@example.com'),
    ('Марія Сидоренко', '+380-63-456-78-90', 'maria@example.com');

INSERT INTO project.services (name, price, duration, description)
VALUES
    ('Масаж обличчя', 500.00, 60, 'Розслабляючий масаж обличчя'),
    ('Манікюр', 300.00, 45, 'Класичний манікюр'),
    ('Педикюр', 400.00, 60, 'СПА-педикюр');

INSERT INTO project.orders (client_id, status)
VALUES
    (1, 'completed'),
    (2, 'in_progress'),
    (3, 'scheduled');

INSERT INTO project.order_items (order_id, service_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 3);

INSERT INTO project.appointments (client_id, service_id, appointment_time, status)
VALUES
    (1, 1, '2026-10-15 10:00:00', 'completed'),
    (2, 2, '2026-10-16 14:00:00', 'scheduled'),
    (3, 3, '2026-10-17 11:00:00', 'scheduled');

INSERT INTO project.inventory (name, quantity, price)
VALUES
    ('Лак для нігтів', 50, 150.00),
    ('Крем для обличчя', 30, 200.00),
    ('Масло для масажу', 20, 300.00);