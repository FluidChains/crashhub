SELECT count(*) FROM logentry
WHERE sender_ip = %(sender_ip)s
AND sent_at BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW();