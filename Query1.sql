#Numero de empleados por cada trabajo contratados por trimestre en el 2021
SELECT d.department,
		j.job,
        CONCAT('Q', QUARTER(he.datetime)) AS Q,
		COUNT(he.id) AS Hired_Employees
FROM
    hired_employees he
INNER JOIN departments d ON he.department_id = d.id
INNER JOIN jobs j ON he.job_id = j.id
WHERE
    YEAR(he.datetime)= 2021
GROUP BY
    d.department, j.job, Q
ORDER BY
    d.department ASC, j.job ASC, Q ASC;
