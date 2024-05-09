 #Lista de IDs, nombres y el número de empleados contratados de cada departamento que contrató más empleados que el promedio de empleados contratados en 2021 para todos los departamentos, 
 #ordenados por el número de empleados contratados en orden descendente
SELECT d.id AS Department_ID,
    d.department AS Department_Name,
    COUNT(he.id) AS Number_of_Employees_Hired
FROM hired_employees he
INNER JOIN departments d ON he.department_id = d.id
WHERE YEAR(he.datetime) = 2021
GROUP BY Department_ID, Department_Name
HAVING
    COUNT(he.id) > (
        SELECT AVG(num_employees_hired)
        FROM
            (SELECT COUNT(id) AS num_employees_hired
            FROM hired_employees
            WHERE YEAR(datetime) = 2021
            GROUP BY department_id) AS subquery
    )
ORDER BY Number_of_Employees_Hired DESC;