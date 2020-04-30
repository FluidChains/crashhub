SELECT * FROM crashkind
WHERE file = %(file)s
AND name = %(name)s
AND type = %(type)s;