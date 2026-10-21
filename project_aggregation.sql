-- Встановлюємо схему за замовчуванням
SET search_path TO project;

-- Рівень 5. Власний проєкт (Beauty Clinic Service Management System)

-- Завдання 25: 3 запити з GROUP BY/HAVING, 2 з підзапитами (1 корельований), 
-- 1 з DISTINCT ON, 2 з віконними функціями

-- 1. GROUP BY/HAVING: Загальна вартість замовлень кожного клієнта.
-- Вивести тільки клієнтів, у яких загальна сума більше 5000.
SELECT
    c.id AS client_id,
    c.name AS client,
    SUM(s.price) AS total_spent
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN services s ON s.id = oi.service_id
GROUP BY c.id, c.name
HAVING SUM(s.price) > 5000
ORDER BY total_spent DESC;

-- 2. GROUP BY/HAVING: Кількість замовлень за кожним статусом.
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 3. GROUP BY/HAVING: Популярність послуг з кількістю замовлень.
SELECT
    s.name AS service_name,
    s.price,
    COUNT(*) AS order_count
FROM services s
LEFT JOIN order_items oi ON oi.service_id = s.id
GROUP BY s.id, s.name, s.price
ORDER BY order_count DESC;

-- 4. Підзапит: Клієнти, які зробили замовлення на суму більше за середню вартість замовлення.
-- Під середньою вартістю замовлення мається на увазі середня сума всіх замовлень.
WITH order_totals AS (
    SELECT o.id, SUM(s.price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    JOIN services s ON s.id = oi.service_id
    GROUP BY o.id
)
SELECT
    c.id,
    c.name AS client,
    ot.order_total
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_totals ot ON ot.id = o.id
WHERE ot.order_total > (SELECT AVG(order_total) FROM order_totals)
ORDER BY ot.order_total DESC;

-- 5. Корельований підзапит: Послуги, ціна яких вища за середню ціну послуг.
SELECT s.id, s.name, s.price
FROM services s
WHERE s.price > (SELECT AVG(price) FROM services)
ORDER BY s.price DESC;

-- 6. DISTINCT ON: Останнє замовлення кожного клієнта.
SELECT DISTINCT ON (client_id)
    client_id,
    id AS order_id,
    created_at,
    status
FROM orders
ORDER BY client_id, created_at DESC;

-- 7. Віконна функція: Накопичувальна сума витрат клієнта за часом.
WITH client_spending AS (
    SELECT
        c.id AS client_id,
        o.id AS order_id,
        o.created_at,
        s.price AS amount
    FROM clients c
    JOIN orders o ON o.client_id = c.id
    JOIN order_items oi ON oi.order_id = o.id
    JOIN services s ON s.id = oi.service_id
)
SELECT
    client_id,
    order_id,
    created_at,
    amount,
    SUM(amount) OVER (
        PARTITION BY client_id
        ORDER BY created_at
    ) AS running_total
FROM client_spending
ORDER BY client_id, created_at;

-- 8. Віконна функція: Рейтинг клієнтів за загальною сумою витрат.
WITH client_totals AS (
    SELECT
        c.id AS client_id,
        c.name AS client,
        SUM(s.price) AS total_spent
    FROM clients c
    JOIN orders o ON o.client_id = c.id
    JOIN order_items oi ON oi.order_id = o.id
    JOIN services s ON s.id = oi.service_id
    GROUP BY c.id, c.name
)
SELECT
    client,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS rank_place
FROM client_totals
ORDER BY rank_place;

-- Завдання 26: 2 представлення, які спрощують найчастіші запити

-- VIEW 1: v_client_orders — повна інформація про замовлення клієнтів
DROP VIEW IF EXISTS v_client_orders;
CREATE VIEW v_client_orders AS
SELECT
    o.id AS order_id,
    o.created_at,
    o.status,
    c.id AS client_id,
    c.name AS client_name,
    c.phone,
    c.email
FROM orders o
JOIN clients c ON c.id = o.client_id;

-- VIEW 2: v_service_popularity — популярність послуг з кількістю замовлень
DROP VIEW IF EXISTS v_service_popularity;
CREATE VIEW v_service_popularity AS
SELECT
    s.id AS service_id,
    s.name AS service_name,
    s.price,
    s.duration,
    COUNT(*) AS times_ordered,
    COALESCE(SUM(s.price), 0) AS total_revenue
FROM services s
LEFT JOIN order_items oi ON oi.service_id = s.id
GROUP BY s.id, s.name, s.price, s.duration
ORDER BY times_ordered DESC;