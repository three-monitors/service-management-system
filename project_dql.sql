-- Встановлюємо схему за замовчуванням
SET search_path TO project, public;

-- Рівень 4. Власний проєкт

-- 1. Без JOIN: Виведіть усі клієнти, відсортовані за прізвищем
-- Питання бізнесу: Список клієнтів в алфавітному порядку
-- Очікувана кількість рядків: ~3
SELECT c.id, c.name, c.phone, c.email
FROM project.clients AS c
ORDER BY c.name;

-- 2. Без JOIN: Виведіть послуги з ціною більше 400
-- Питання бізнесу: Преміум послуги
-- Очікувана кількість рядків: ~2
SELECT s.id, s.name, s.price, s.duration
FROM project.services AS s
WHERE s.price > 400
ORDER BY s.price DESC;

-- 3. Без JOIN: Виведіть замовлення зі статусом completed
-- Питання бізнесу: Завершені замовлення
-- Очікувана кількість рядків: ~1
SELECT o.id, o.status, o.created_at
FROM project.orders AS o
WHERE o.status = 'completed'
ORDER BY o.created_at DESC;

-- 4. Без JOIN: Виведіть продукти з кількістю менше 30
-- Питання бізнесу: Товари, які треба докупити
-- Очікувана кількість рядків: ~2
SELECT i.id, i.name, i.quantity, i.price
FROM project.inventory AS i
WHERE i.quantity < 30
ORDER BY i.quantity ASC;

-- 5. INNER JOIN: Виведіть замовлення з іменем клієнта
-- Питання бізнесу: Замовлення з інформацією про клієнта
-- Очікувана кількість рядків: ~3
SELECT o.id, c.name AS client_name, o.status, o.created_at
FROM project.orders AS o
JOIN project.clients AS c ON c.id = o.client_id
ORDER BY o.created_at DESC;

-- 6. INNER JOIN: Виведіть замовлення з послугами
-- Питання бізнесу: Що саме замовив клієнт
-- Очікувана кількість рядків: ~4
SELECT o.id, s.name AS service_name, s.price
FROM project.orders AS o
JOIN project.order_items AS oi ON oi.order_id = o.id
JOIN project.services AS s ON s.id = oi.service_id
ORDER BY o.id;

-- 7. LEFT JOIN: Виведіть усі послуги з кількістю замовлень
-- Питання бізнесу: Популярність послуг
-- Очікувана кількість рядків: ~3
SELECT s.name, COUNT(oi.order_id) AS order_count
FROM project.services AS s
LEFT JOIN project.order_items AS oi ON oi.service_id = s.id
GROUP BY s.id, s.name
ORDER BY order_count DESC;

-- 8. LEFT JOIN: Виведіть клієнтів з їхніми призначеннями
-- Питання бізнесу: Запис клієнтів на процедури
-- Очікувана кількість рядків: ~3
SELECT c.name AS client_name, a.appointment_time, a.status
FROM project.clients AS c
LEFT JOIN project.appointments AS a ON a.client_id = c.id
ORDER BY c.name, a.appointment_time;

-- 9. Пошук «записів без пари»: Послуги без жодного замовлення
-- Питання бізнесу: Нереалізовані послуги
-- Очікувана кількість рядків: ~1
SELECT s.id, s.name, s.price
FROM project.services AS s
LEFT JOIN project.order_items AS oi ON oi.service_id = s.id
WHERE oi.service_id IS NULL;

-- 10. Пошук «записів без пари»: Клієнти без жодного замовлення
-- Питання бізнесу: Нові клієнти без покупок
-- Очікувана кількість рядків: ~0
SELECT c.id, c.name, c.phone, c.email
FROM project.clients AS c
LEFT JOIN project.orders AS o ON o.client_id = c.id
WHERE o.id IS NULL;