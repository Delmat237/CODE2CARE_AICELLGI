
psql -U postgres -h localhost -d feedback_db


-- Connect to the database
\c feedback_db

-- Disable foreign key checks to avoid dependency issues
SET session_replication_role = replica;

-- Drop all tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS feedbacks CASCADE;
DROP TABLE IF EXISTS reminders CASCADE;
DROP TABLE IF EXISTS alembic_version CASCADE; -- Drop migration tracking table

-- Re-enable foreign key checks
SET session_replication_role = DEFAULT;

-- Verify tables are dropped
\dt


rm migrations/versions/*
alembic revision -m "Initial migration"
alembic upgrade head

alembic revision --autogenerate -m "Recreate initial migration with all tables"
alembic upgrade head


alembic init migrations

