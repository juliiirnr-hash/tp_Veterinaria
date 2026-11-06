-- C-08: la base debe rechazar precio = 0 por ck_practica_precio_positivo.
BEGIN;
UPDATE practica SET precio = 0 WHERE id = 1;
ROLLBACK;
