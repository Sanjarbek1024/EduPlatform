CREATE TABLE Users (
  id INT,
  full_name VARCHAR(255),
  email VARCHAR(255),
  role VARCHAR(255),
  created_at VARCHAR(255)
);

INSERT INTO Users (id, full_name, email, role, created_at) VALUES (1, 'Ali Admin', 'ali@edu.uz', 'Admin', '2025-06-14T11:26:22.375176');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (2, 'Zarina Xon', 'zarina@school.com', 'Teacher', '2025-06-14T11:26:22.375176');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (3, 'Aziz Karimov', 'aziz@school.com', 'Student', '2025-06-14T11:26:22.375176');
INSERT INTO Users (id, full_name, email, role, created_at) VALUES (4, 'Karim aka', 'karim@family.com', 'Parent', '2025-06-14T11:26:22.376555');

CREATE TABLE Assignments (
  id INT,
  title VARCHAR(255),
  subject VARCHAR(255),
  class_id VARCHAR(255),
  deadline VARCHAR(255),
  submissions_count VARCHAR(255),
  graded_count VARCHAR(255)
);

INSERT INTO Assignments (id, title, subject, class_id, deadline, submissions_count, graded_count) VALUES (1, 'Algebra uy vazifasi', 'Math', '9-A', '2025-06-20T23:59', 1, 1);

CREATE TABLE Grades (
  id INT,
  student_id INT,
  subject VARCHAR(255),
  value VARCHAR(255),
  date VARCHAR(255),
  teacher_id INT,
  comment VARCHAR(255)
);

INSERT INTO Grades (id, student_id, subject, value, date, teacher_id, comment) VALUES (1, 3, 'Math', 5, '2025-06-14T11:26:22.378553', 2, 'Ajoyib');

CREATE TABLE Notifications (
  id INT,
  message VARCHAR(255),
  recipient_id INT,
  created_at VARCHAR(255),
  is_read VARCHAR(255),
  priority VARCHAR(255)
);

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority) VALUES (1, 'Yangi vazifa yuklandi!', 3, '2025-06-14T11:26:22.378553', False, 'high');

CREATE TABLE Schedules (
  id INT,
  class_id VARCHAR(255),
  day VARCHAR(255),
  lessons VARCHAR(255)
);

INSERT INTO Schedules (id, class_id, day, lessons) VALUES (1, '9-A', 'Monday', '{''08:00'': {''subject'': ''Matematika'', ''teacher_id'': 2}}');

