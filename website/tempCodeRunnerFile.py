
class Receptionist:
    def __init__(self, receptionist_id, name, contact_number, email,password):
        self.receptionist_id = receptionist_id  # Unique identifier for each receptionist
        self.name = name  # Full name of the receptionist
        self.contact_number = contact_number  # Contact number of the receptionist
        self.email = email  # Email address of the receptionist
        self.password = password # Password of the receptionist

    def __str__(self):
        return f"{self.name} (ID: {self.receptionist_id})"
