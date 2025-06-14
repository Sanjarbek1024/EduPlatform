from data.storage import users, students, teachers, parents, admins, assignments, grades, notifications, schedules
from export.to_csv import export_to_csv
from export.to_xlsx import export_to_xlsx
from export.to_sql import export_to_sql
from core.user import Admin, Teacher, Student, Parent, Role
from core.assignment import Assignment
from core.grade import Grade
from core.notification import Notification
from core.schedule import Schedule

import hashlib
import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    print("\nYangi foydalanuvchi qo'shish (faqat Admin uchun)")
    role_input = input("Rolni kiriting (admin/teacher/student/parent): ").lower()
    full_name = input("Ism va familiya: ")
    email = input("Email: ")
    password = input("Parol: ")

    if role_input == "admin":
        user = Admin(full_name, email, password)
        admins.append(user)
    elif role_input == "teacher":
        subjects = input("Fanlar (vergul bilan): ").split(",")
        classes = input("Sinf(lar) (vergul bilan): ").split(",")
        user = Teacher(full_name, email, password, subjects, classes)
        teachers.append(user)
    elif role_input == "student":
        grade = input("Sinf (masalan: 9-A): ")
        while True:
            subject_map = input("Fan va o'qituvchi ID (Math:2,English:3): ")
            try:
                subjects = dict(item.split(":") for item in subject_map.split(","))
                break
            except ValueError:
                print("Format noto'g'ri! Masalan: Math:2,English:3")
        user = Student(full_name, email, password, grade, subjects)
        students.append(user)
    elif role_input == "parent":
        child_ids = list(map(int, input("Farzand IDlari (vergul bilan): ").split(",")))
        user = Parent(full_name, email, password, child_ids)
        parents.append(user)
    else:
        print("Noto'g'ri rol tanlandi.")
        return

    users.append(user)
    print(f"{role_input.capitalize()} foydalanuvchi yaratildi: {full_name}")

def login():
    print("\nTizimga kirish")
    email = input("Email: ")
    password = input("Parol: ")
    hashed = hash_password(password)

    for u in users:
        if u._email == email and u._password_hash == hashed:
            print(f"Xush kelibsiz, {u._full_name}!")
            return u

    print("Email yoki parol noto'g'ri.")
    return None

def admin_panel(admin):
    while True:
        print("\n[Admin Panel]")
        print("1. Foydalanuvchi qo'shish")
        print("2. Hisobot yaratish")
        print("3. Chiqish")
        choice = input("Tanlov: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            admin.generate_report()
        elif choice == "3":
            break
        else:
            print("Noto'g'ri tanlov")

def teacher_panel(teacher):
    while True:
        print("\n[O'qituvchi Paneli]")
        print("1. Vazifa yaratish")
        print("2. Baho qo'yish")
        print("3. O'quvchini kuzatish")
        print("4. Chiqish")
        choice = input("Tanlov: ")
        if choice == "1":
            title = input("Vazifa nomi: ")
            desc = input("Tavsif: ")
            deadline = input("Deadline (YYYY-MM-DDTHH:MM): ")
            subject = input("Fan: ")
            class_id = input("Sinf: ")
            task = Assignment(title, desc, deadline, subject, teacher._id, class_id)
            assignments.append(task)
            teacher.assignments[task.id] = task
            print("Vazifa yaratildi")
        elif choice == "2":
            aid = int(input("Vazifa ID: "))
            sid = int(input("O'quvchi ID: "))
            grade = int(input("Baho (1-5): "))
            teacher.grade_assignment(aid, sid, grade)
        elif choice == "3":
            sid = int(input("O'quvchi ID: "))
            teacher.view_student_progress(sid)
        elif choice == "4":
            break
        else:
            print("Noto'g'ri tanlov")

def student_panel(student):
    while True:
        print("\n[O'quvchi Paneli]")
        print("1. Vazifa topshirish")
        print("2. Baholarni ko'rish")
        print("3. O'rtacha bahoni ko'rish")
        print("4. Chiqish")
        choice = input("Tanlov: ")
        if choice == "1":
            aid = int(input("Vazifa ID: "))
            content = input("Javob matni: ")
            if len(content) > 500:
                print("Javob matni 500 belgidan oshmasligi kerak.")
                continue
            deadline_check = next((a for a in assignments if a.id == aid), None)
            if deadline_check and datetime.datetime.now() > datetime.datetime.fromisoformat(deadline_check.deadline):
                print("Diqqat: bu vazifaning muddati tugagan.")
            student.submit_assignment(aid, content)
        elif choice == "2":
            subj = input("Fan nomi (yoki bo'sh): ")
            print(student.view_grades(subj if subj else None))
        elif choice == "3":
            print("O'rtacha baho:", student.calculate_average_grade())
        elif choice == "4":
            break

def parent_panel(parent):
    while True:
        print("\n[Ota-ona Paneli]")
        print("1. Farzand baholari")
        print("2. Farzand topshiriqlari")
        print("3. Farzand xabarlari")
        print("4. Chiqish")
        choice = input("Tanlov: ")
        if choice == "1":
            cid = int(input("Farzand ID: "))
            parent.view_child_grades(cid)
        elif choice == "2":
            cid = int(input("Farzand ID: "))
            parent.view_child_assignments(cid)
        elif choice == "3":
            cid = int(input("Farzand ID: "))
            parent.receive_child_notification(cid)
        elif choice == "4":
            break

def export_all():
    export_to_csv([u.get_profile() for u in users], "users.csv", ["id", "full_name", "email", "role", "created_at"])
    export_to_csv([a.get_status() for a in assignments], "assignments.csv", ["id", "title", "subject", "class_id", "deadline", "submissions_count", "graded_count"])
    export_to_csv([g.get_grade_info() for g in grades], "grades.csv", ["id", "student_id", "subject", "value", "date", "teacher_id", "comment"])
    export_to_csv([n.get_info() for n in notifications], "notifications.csv", ["id", "message", "recipient_id", "created_at", "is_read", "priority"])
    export_to_csv([s.get_info() for s in schedules], "schedules.csv", ["id", "class_id", "day", "lessons"])

    export_to_xlsx({
        "Users": [u.get_profile() for u in users],
        "Assignments": [a.get_status() for a in assignments],
        "Grades": [g.get_grade_info() for g in grades],
        "Notifications": [n.get_info() for n in notifications],
        "Schedules": [s.get_info() for s in schedules],
    })

    export_to_sql({
        "Users": [u.get_profile() for u in users],
        "Assignments": [a.get_status() for a in assignments],
        "Grades": [g.get_grade_info() for g in grades],
        "Notifications": [n.get_info() for n in notifications],
        "Schedules": [s.get_info() for s in schedules],
    })
    print("Ma'lumotlar eksport qilindi.")

def main():
    print("\nEDU PLATFORM TERMINAL TIZIMI")
    while True:
        print("\n1. Ro'yxatdan o'tish (faqat admin)")
        print("2. Login qilish")
        print("3. Ma'lumotlarni eksport qilish")
        print("4. Chiqish")
        choice = input("Tanlovni kiriting: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            user = login()
            if user:
                if user.role == Role.ADMIN:
                    admin_panel(user)
                elif user.role == Role.TEACHER:
                    teacher_panel(user)
                elif user.role == Role.STUDENT:
                    student_panel(user)
                elif user.role == Role.PARENT:
                    parent_panel(user)
        elif choice == "3":
            export_all()
        elif choice == "4":
            print("Chiqildi. Xayr!")
            break
        else:
            print("Noto'g'ri tanlov. 1-4 ni tanlang.")


if __name__ == "__main__":
    main()
