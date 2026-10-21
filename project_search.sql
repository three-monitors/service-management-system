-- Встановлюємо схему за замовчуванням
SET search_path TO project;

-- 2. 5 запитів SELECT з LIKE, ORDER BY і LIMIT

-- 1. Пошук клієнтів за іменем (LIKE)
SELECT id, name, phone, email
FROM project.clients
WHERE name LIKE '%Олена%'
ORDER BY name
LIMIT 10;

-- 2. Пошук послуг за назвою (ILIKE — без урахування регістру)
SELECT id, name, price, duration
FROM project.services
WHERE name ILIKE '%масаж%'
ORDER BY price DESC
LIMIT 5;

-- 3. Замовлення зі статусом in_progress (ORDER BY по даті)
SELECT id, client_id, status, created_at
FROM project.orders
WHERE status = 'in_progress'
ORDER BY created_at DESC
LIMIT 10;

-- 4. Призначення на майбутнє (BETWEEN для дати)
SELECT id, client_id, service_id, appointment_time
FROM project.appointments
WHERE appointment_time BETWEEN '2026-10-15' AND '2026-10-31'
ORDER BY appointment_time
LIMIT 10;

-- 5. Товари з інвентаризації з кількістю менше 50
SELECT id, name, quantity, price
FROM project.inventory
WHERE quantity < 50
ORDER BY quantity ASC
LIMIT 10;