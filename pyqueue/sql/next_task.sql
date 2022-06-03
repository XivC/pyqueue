SELECT
       task
FROM $name$ AS t_name
WHERE id IN (
    SELECT MIN(id) FROM $name$
    )