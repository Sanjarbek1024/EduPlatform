from data.storage import users, students, teachers, parents, admins, assignments, grades, notifications, schedules
from export.to_csv import export_to_csv
from export.to_xlsx import export_to_xlsx
from export.to_sql import export_to_sql
from core.user import Admin, Teacher, Student, Parent
from core.assignment import Assignment
from core.grade import Grade
from core.notification import Notification
from core.schedule import Schedule

# 1️⃣ Admin yaratadi
admin = Admin("Ali Admin", "ali@edu.uz", "admin123")
users.append(admin)
admins.append(admin)

# 2️⃣ O'qituvchi va o'quvchi yaratamiz
teacher = Teacher("Zarina Xon", "zarina@school.com", "abc123", ["Math"], ["9-A"])
student = Student("Aziz Karimov", "aziz@school.com", "qwerty", "9-A", {"Math": teacher._id})
parent = Parent("Karim aka", "karim@family.com", "12345", children_ids=[student._id])

users.extend([teacher, student, parent])
teachers.append(teacher)
students.append(student)
parents.append(parent)

# 3️⃣ Dars jadvali yaratamiz
schedule = Schedule(class_id="9-A", day="Monday")
schedule.add_lesson("08:00", "Matematika", teacher._id)
schedules.append(schedule)

# 4️⃣ Assignment yaratiladi
task = Assignment("Algebra uy vazifasi", "x=5 ni toping", "2025-06-20T23:59", "Math", teacher._id, "9-A")
assignments.append(task)
teacher.assignments[task.id] = task

# 5️⃣ Student topshiriqni topshiradi
student.submit_assignment(task.id, "x = 5 yechim")

# 6️⃣ O'qituvchi baho qo'yadi
teacher.grade_assignment(task.id, student._id, 5)

# 7️⃣ Xabarnoma yuboriladi
notif = Notification("Yangi vazifa yuklandi!", recipient_id=student._id, priority="high")
notif.send()
notifications.append(notif)
student.add_notification(notif.message)

# 8️⃣ Bahoni alohida obyekt sifatida saqlaymiz
grade = Grade(student_id=student._id, subject="Math", value=5, teacher_id=teacher._id, comment="Ajoyib")
grades.append(grade)

# 9️⃣ Eksport CSV
export_to_csv([u.get_profile() for u in users], "users.csv", ["id", "full_name", "email", "role", "created_at"])
export_to_csv([a.get_status() for a in assignments], "assignments.csv", ["id", "title", "subject", "class_id", "deadline", "submissions_count", "graded_count"])
export_to_csv([g.get_grade_info() for g in grades], "grades.csv", ["id", "student_id", "subject", "value", "date", "teacher_id", "comment"])
export_to_csv([n.get_info() for n in notifications], "notifications.csv", ["id", "message", "recipient_id", "created_at", "is_read", "priority"])
export_to_csv([s.get_info() for s in schedules], "schedules.csv", ["id", "class_id", "day", "lessons"])

# Export to XLSX
export_to_xlsx({
    "Users": [u.get_profile() for u in users],
    "Assignments": [a.get_status() for a in assignments],
    "Grades": [g.get_grade_info() for g in grades],
    "Notifications": [n.get_info() for n in notifications],
    "Schedules": [s.get_info() for s in schedules],
})

# Export to SQL
export_to_sql({
    "Users": [u.get_profile() for u in users],
    "Assignments": [a.get_status() for a in assignments],
    "Grades": [g.get_grade_info() for g in grades],
    "Notifications": [n.get_info() for n in notifications],
    "Schedules": [s.get_info() for s in schedules],
})
