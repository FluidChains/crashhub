INSERT INTO crashkind(file, name, type)
VALUES (%(file)s, %(name)s, %(type)s)
RETURNING *;