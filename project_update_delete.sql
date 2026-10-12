-- Встановлюємо схему за замовчуванням
SET search_path TO project, public;

-- 3. Безпечний UPDATE і DELETE (спочатку SELECT, потім транзакція)

-- UPDATE: Оновлення ціни послуги
-- Спочатку SELECT:
SELECT id, name, price
FROM project.services
WHERE id = 1;

-- Потім UPDATE в транзакції:
BEGIN;

UPDATE project.services
SET price = 550.00
WHERE id = 1
RETURNING id, name, price;

-- Перевіряємо результат
SELECT id, name, price FROM project.services WHERE id = 1;

-- Якщо все правильно, то COMMIT, інакше ROLLBACK
-- COMMIT;
ROLLBACK;

-- DELETE: Видалення завершеного замовлення
-- Спочатку SELECT:
SELECT id, client_id, status
FROM project.orders
WHERE id = 1 AND status = 'completed';

-- Потім DELETE в транзакції:
BEGIN;

DELETE FROM project.order_items
WHERE order_id = 1;

DELETE FROM project.orders
WHERE id = 1 AND status = 'completed'
RETURNING id, client_id, status;

-- Перевіряємо результат
SELECT id, client_id, status FROM project.orders WHERE id = 1;

-- Якщо все правильно, то COMMIT, інакше ROLLBACK
-- COMMIT;
ROLLBACK;