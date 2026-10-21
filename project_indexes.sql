-- Встановлюємо схему за замовчуванням
SET search_path TO project;

-- 4. Індекси на зовнішні ключі та перевірка через EXPLAIN ANALYZE

-- Створення індексів на зовнішніх ключах
CREATE INDEX idx_orders_client_id ON project.orders (client_id);
CREATE INDEX idx_order_items_order_id ON project.order_items (order_id);
CREATE INDEX idx_order_items_service_id ON project.order_items (service_id);
CREATE INDEX idx_appointments_client_id ON project.appointments (client_id);
CREATE INDEX idx_appointments_service_id ON project.appointments (service_id);

-- Перевірка запиту через EXPLAIN ANALYZE
-- Без індексу (пошук за client_id):
EXPLAIN ANALYZE
SELECT * FROM project.orders WHERE client_id = 1;

-- Після створення індексу результат повинен бути швидшим (Index Scan замість Seq Scan)

-- Перегляд індексів таблиці orders
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'orders' AND schemaname = 'project';