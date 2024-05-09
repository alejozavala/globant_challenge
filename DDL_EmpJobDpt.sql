CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(255)
);

CREATE TABLE Jobs (
    job_id INT PRIMARY KEY,
    job_name VARCHAR(255)
);

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(255),
    hire_date DATETIME,
    department_id INT,
    job_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id)
);