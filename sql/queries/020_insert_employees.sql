INSERT INTO employees (id, name, salary)
SELECT id, name, salary
FROM staging_employees
ON CONFLICT (id) DO NOTHING;
