class Schedule:
    _id_counter = 1  # Avtoinkrement ID

    def __init__(self, class_id, day):
        self.id = Schedule._id_counter
        Schedule._id_counter += 1

        self.class_id = class_id     # Masalan: "9-A"
        self.day = day               # Masalan: "Monday"
        self.lessons = {}           # {time: {"subject": ..., "teacher_id": ...}}

    def add_lesson(self, time, subject, teacher_id):
        if time in self.lessons:
            print(f"[⚠️] Dars {time} da allaqachon mavjud.")
        else:
            self.lessons[time] = {
                "subject": subject,
                "teacher_id": teacher_id
            }
            print(f"[➕] Dars qo‘shildi: {time} - {subject} (teacher {teacher_id})")

    def view_schedule(self):
        print(f"\n📅 Dars jadvali - {self.class_id} ({self.day}):")
        if not self.lessons:
            print("🚫 Hech qanday dars mavjud emas.")
        else:
            for time in sorted(self.lessons):
                lesson = self.lessons[time]
                print(f"  ⏰ {time} → {lesson['subject']} (Teacher ID: {lesson['teacher_id']})")

    def remove_lesson(self, time):
        if time in self.lessons:
            removed = self.lessons.pop(time)
            print(f"[🗑️] Dars o‘chirildi: {time} - {removed['subject']}")
        else:
            print(f"[❌] {time} da dars topilmadi.")

    def get_info(self):
        return {
            "id": self.id,
            "class_id": self.class_id,
            "day": self.day,
            "lessons": str(self.lessons)
        }
