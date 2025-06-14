from core.base import AbstractRole
from enum import Enum

class Role(Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

# #####################################################
# USER CLASS
# #####################################################

class User(AbstractRole):
    def __init__(self, full_name, email, password, role: Role):
        super().__init__(full_name, email, password)
        self.role = role
        self._notifications = []

    def get_profile(self):
        return {
            "id": self._id,
            "full_name": self._full_name,
            "email": self._email,
            "role": self.role.value,
            "created_at": self._created_at
        }

    def update_profile(self, **kwargs):
        if "full_name" in kwargs:
            self._full_name = kwargs["full_name"]
        if "email" in kwargs:
            self._email = kwargs["email"]
        if "password" in kwargs:
            self._password_hash = self._hash_password(kwargs["password"])

    def add_notification(self, message):
        notification_id = len(self._notifications) + 1
        self._notifications.append({
            "id": notification_id,
            "message": message,
            "read": False
        })

    def view_notifications(self):
        return self._notifications

    def delete_notification(self, notification_id):
        self._notifications = [n for n in self._notifications if n["id"] != notification_id]


# #####################################################
# STUDENT CLASS
# #####################################################

from data.storage import assignments

class Student(User):
    def __init__(self, full_name, email, password, grade, subjects):
        super().__init__(full_name, email, password, Role.STUDENT)
        self.grade = grade
        self.subjects = subjects  # {subject_name: teacher_id}
        self.assignments = {}     # {assignment_id: 'submitted' or 'pending'}
        self.grades = {}          # {subject_name: [grade1, grade2, ...]}

    def submit_assignment(self, assignment_id, content):
        if assignment_id in self.assignments and self.assignments[assignment_id] == 'submitted':
            print(f"[⚠️] Assignment {assignment_id} already submitted.")
            return

        self.assignments[assignment_id] = 'submitted'
        print(f"[✅] Assignment {assignment_id} submitted with content: {content}")

        # 🔽 Real Assignment obyektga ham submission qo‘shamiz
        assignment = next((a for a in assignments if a.id == assignment_id), None)
        if assignment:
            assignment.add_submission(self._id, content)
        else:
            print(f"[❌] Assignment {assignment_id} not found in system.")

    def view_grades(self, subject=None):
        if subject:
            return self.grades.get(subject, [])
        return self.grades

    def calculate_average_grade(self):
        total = 0
        count = 0
        for subject_grades in self.grades.values():
            total += sum(subject_grades)
            count += len(subject_grades)
        if count == 0:
            return 0
        return round(total / count, 2)


# #####################################################
# TEACHER CLASS
# #####################################################

from core.assignment import Assignment  # assignment.py faylidan olib ishlatamiz
from data.storage import assignments, students  # global saqlovchilarni chaqiramiz

class Teacher(User):
    def __init__(self, full_name, email, password, subjects, classes):
        super().__init__(full_name, email, password, Role.TEACHER)
        self.subjects = subjects    # list of subject names
        self.classes = classes      # list of class IDs (e.g., ["9-A", "10-B"])
        self.assignments = {}       # {assignment_id: Assignment}

    def create_assignment(self, title, description, deadline, subject, class_id):
        new_assignment = Assignment(
            title=title,
            description=description,
            deadline=deadline,
            subject=subject,
            teacher_id=self._id,
            class_id=class_id
        )
        self.assignments[new_assignment.id] = new_assignment
        assignments.append(new_assignment)
        print(f"[✅] Assignment '{title}' created for class {class_id} - subject: {subject}")

    def grade_assignment(self, assignment_id, student_id, grade):
        if assignment_id in self.assignments:
            assignment = self.assignments[assignment_id]
            assignment.set_grade(student_id, grade)
            print(f"[✅] Student {student_id} graded {grade} for assignment {assignment_id}")
        else:
            print("[❌] Assignment not found")

    def view_student_progress(self, student_id):
        student = next((s for s in students if s._id == student_id), None)
        if student:
            print(f"Progress for {student._full_name}:")
            print("Assignments:", student.assignments)
            print("Grades:", student.grades)
        else:
            print("[❌] Student not found")


# #####################################################
# PARENT CLASS
# #####################################################

class Parent(User):
    def __init__(self, full_name, email, password, children_ids):
        super().__init__(full_name, email, password, Role.PARENT)
        self.children = children_ids  # list of student IDs

    def view_child_grades(self, child_id):
        student = next((s for s in students if s._id == child_id), None)
        if student:
            print(f"Grades for {student._full_name}: {student.grades}")
        else:
            print("[❌] Child not found")

    def view_child_assignments(self, child_id):
        student = next((s for s in students if s._id == child_id), None)
        if student:
            print(f"Assignments for {student._full_name}: {student.assignments}")
        else:
            print("[❌] Child not found")

    def receive_child_notification(self, child_id):
        student = next((s for s in students if s._id == child_id), None)
        if student:
            print(f"Notifications for {student._full_name}: {student.view_notifications()}")
        else:
            print("[❌] Child not found")


# #####################################################
# ADMIN CLASS
# #####################################################

from data.storage import users  # Global userlar ro‘yxati

class Admin(User):
    def __init__(self, full_name, email, password, permissions=None):
        super().__init__(full_name, email, password, Role.ADMIN)
        self.permissions = permissions if permissions else []

    def add_user(self, user):
        users.append(user)
        print(f"[✅] User '{user._full_name}' added with role {user.role.value}")

    def remove_user(self, user_id):
        global users
        users = [u for u in users if u._id != user_id]
        print(f"[🗑️] User with ID {user_id} removed.")

    def generate_report(self):
        print("[📊] System Report:")
        print(f"Total Users: {len(users)}")
        roles = {}
        for u in users:
            r = u.role.value
            roles[r] = roles.get(r, 0) + 1
        for role, count in roles.items():
            print(f" - {role}: {count}")
