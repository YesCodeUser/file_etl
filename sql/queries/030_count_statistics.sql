SELECT
    (SELECT COUNT(*) FROM staging_employees) as attempted,
    (SELECT COUNT(*) FROM employees) as total;

