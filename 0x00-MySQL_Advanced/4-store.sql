-- trigger that decreases quantity of an item after placing order.
DELIMITER //

CREATE TRIGGER decrease_quantity_after_placing_order
AFTER INSERT
ON orders
FOR EACH ROW
BEGIN
  UPDATE items
  SET quantity = quantity - NEW.Number
  WHERE name = NEW.item_name;
END;
//
DELIMITER ;
