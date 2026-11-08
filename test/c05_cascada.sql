-- C-05: después de DELETE /turnos/1 la base borra en cascada sus prácticas.
-- Ejecutar con: psql -U postgres -d veterinaria -f test/c05_cascada.sql
-- Resultado esperado: practicas_del_turno_1 = 0
SELECT count(*) AS practicas_del_turno_1
FROM turno_practica
WHERE turno_id = 1;
