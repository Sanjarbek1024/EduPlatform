CREATE TABLE IF NOT EXISTS Users (
  id INT,
  full_name VARCHAR(255),
  email VARCHAR(255),
  role VARCHAR(255),
  created_at VARCHAR(255)
);

INSERT INTO Users (id, full_name, email, role, created_at) VALUES (1, 'Sanjarbek Gulomjonov', 'gsanjarbek1024@gmail.com', 'Admin', '2025-06-14T14:42:44.585534');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (2, 'Sardor Mamadaliyev', 'sardor@gmail.com', 'Teacher', '2025-06-14T14:46:05.553614');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (3, 'Sarvar Odilov', 'sarvar@gmail.com', 'Student', '2025-06-14T14:50:05.375592');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (4, 'Jasur Hamdamov', 'jasur@gmail.com', 'Parent', '2025-06-14T14:51:10.702217');

CREATE TABLE IF NOT EXISTS Assignments (
  id INT,
  title VARCHAR(255),
  subject VARCHAR(255),
  class_id VARCHAR(255),
  deadline VARCHAR(255),
  submissions_count VARCHAR(255),
  graded_count VARCHAR(255)
);

INSERT INTO Assignments (id, title, subject, class_id, deadline, submissions_count, graded_count) VALUES (1, 'Sayyoralar', 'Matematika', '10', '2025-11-12T12:00', 0, 0);

