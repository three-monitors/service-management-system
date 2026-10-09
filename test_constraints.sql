-- ✅ Коректні дані
INSERT INTO clients (name, phone, email)
VALUES ('Олена Коваленко', '+380-67-123-45-67', 'olena@example.com');

INSERT INTO services (name, price, duration, description)
VALUES ('Масаж обличчя', 500.00, 60, 'Розслабляючий масаж обличчя');

INSERT INTO orders (client_id, status)
VALUES (1, 'scheduled');

INSERT INTO order_items (order_id, service_id)
VALUES (1, 1);

-- ❌ Дубль телефону → порушення UNIQUE
INSERT INTO clients (name, phone, email)
VALUES ('Інший клієнт', '+380-67-123-45-67', 'other@example.com');

-- ❌ Негативна ціна → порушення CHECK
INSERT INTO services (name, price, duration, description)
VALUES ('Масаж тіла', -100.00, 90, 'Антистрес масаж');

-- ❌ Клієнта 999 не існує → порушення FOREIGN KEY
INSERT INTO orders (client_id, status)
VALUES (999, 'scheduled');