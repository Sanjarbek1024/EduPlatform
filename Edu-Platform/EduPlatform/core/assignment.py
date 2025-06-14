from datetime import datetime
from data.storage import students  # Global ro‘yxatdan studentni topish uchun

class Assignment:
    _id_counter = 1  # Global ID generator (avtoinkrement)

    def __init__(self, title, description, deadline, subject, teacher_id, class_id):
        self.id = Assignment._id_counter
        Assignment._id_counter += 1

        self.title = title
        self.description = description
        self.deadline = deadline  # str: ISO format, e.g. "2025-06-15T23:59"
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id

        self.submissions = {}  # {student_id: content}
        self.grades = {}       # {student_id: grade}

    def add_submission(self, student_id, content):
        now = datetime.now()
        deadline_time = datetime.fromisoformat(self.deadline)

        if student_id in self.submissions:
            print(f"[⚠️] Student {student_id} already submitted.")
        elif now > deadline_time:
            print(f"[⏰] Deadline passed. Submission by Student {student_id} is late.")
        else:
            self.submissions[student_id] = content
            print(f"[✅] Submission received from Student {student_id}")

    def set_grade(self, student_id, grade):
        if student_id in self.submissions:
            if not isinstance(grade, int) or not (1 <= grade <= 5):
                print(f"[❌] Invalid grade: {grade}. Must be integer 1–5.")
                return

            self.grades[student_id] = grade
            print(f"[🎓] Grade {grade} set for Student {student_id}")

            # 🔽 Student obyektini topib, bahoni unga ham qo‘shamiz
            student = next((s for s in students if s._id == student_id), None)
            if student:
                if self.subject not in student.grades:
                    student.grades[self.subject] = []
                student.grades[self.subject].append(grade)
        else:
            print(f"[❌] Cannot grade — no submission from Student {student_id}")

    def get_status(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "class_id": self.class_id,
            "deadline": self.deadline,
            "submissions_count": len(self.submissions),
            "graded_count": len(self.grades),
        }
