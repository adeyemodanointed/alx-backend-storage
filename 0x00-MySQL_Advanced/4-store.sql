-- Write a SQL script that creates a trigger that decreases
-- the quantity of an item after adding a new order.

CREATE TRIGGER items_trigger
AFTER INSERT
ON orders FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
