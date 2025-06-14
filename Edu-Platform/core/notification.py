from datetime import datetime

class Notification:
    _id_counter = 1  # Unikal ID generator

    def __init__(self, message, recipient_id, priority="normal"):
        self.id = Notification._id_counter
        Notification._id_counter += 1

        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.now().isoformat()
        self.is_read = False
        self.priority = priority # "normal", "high", "low"

    def send(self):
        print(f"\n Notification sent to user {self.recipient_id}: {self.message}")

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            print(f"\n Notification {self.id} marked as read")
        else:
            print(f"\n Notification {self.id} already read")

    def get_info(self):
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "is_read": self.is_read,
            "priority": self.priority  
        }

