from datetime import datetime

class Grade:
    _id_counter = 1  # Unikal ID generator

    def __init__(self, student_id, subject, value, teacher_id, comment=""):
        self.id = Grade._id_counter
        Grade._id_counter += 1

        self.student_id = student_id       # Talaba IDsi
        self.subject = subject             # Fan nomi
        self.value = self._validate_value(value)  # Baho (1-5)
        self.date = datetime.now().isoformat()    # Sana (ISO format)
        self.teacher_id = teacher_id       # O‘qituvchi IDsi
        self.comment = comment             # Ixtiyoriy izoh

    def _validate_value(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Grade must be an integer between 1 and 5.")
        return value

    def update_grade(self, new_value, new_comment=None):
        self.value = self._validate_value(new_value)
        self.date = datetime.now().isoformat()
        if new_comment is not None:
            self.comment = new_comment
        print(f"\n Grade updated: {self.value}, comment: {self.comment}")

    def get_grade_info(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }
