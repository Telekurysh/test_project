CREATE
DATABASE IF NOT EXISTS test_project;

DO
$do$
BEGIN
    IF
EXISTS (SELECT FROM pg_user
        WHERE  usename = 'admin'
        ) THEN

        RAISE NOTICE 'SKIP ROLE MAKER!';
ELSE
CREATE ROLE admin LOGIN PASSWORD 'admin';
END IF;
END
$do$;

ALTER
ROLE admin SET client_encoding TO 'utf8';
ALTER
ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER
ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE
postgres TO admin;