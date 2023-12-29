
from datetime import datetime
import pickle 
import uuid
from abc import ABC, abstractmethod

#########################################################################################################

#ADMIN MODULE

class ClinicAdminSingleton:
    # Class variable to store the singleton instance
    _instance = None

    def __init__(self, username, password):
        # Check if the instance doesn't exist
        if not ClinicAdminSingleton._instance:
            # Set attributes for the instance
            self.username = username
            self.password = password
            # Set the class variable to the current instance
            ClinicAdminSingleton._instance = self

    @classmethod
    def get_instance(cls, username, password):
        # Check if the instance doesn't exist
        if not cls._instance:
            # Create a new instance if it doesn't exist
            cls._instance = cls(username, password)

        return cls._instance


#########################################################################################################

#DOCTOR MODULE 

# Abstract Doctor class
class Doctor(ABC):
    def __init__(self, doctor_id, name, specialization, contact_number, email, qualification, available_hours, password):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.contact_number = contact_number
        self.email = email
        self.qualification = qualification
        self.available_hours = available_hours
        self.password = password
        self.queue = []
        self.consultation_fee=100
    @abstractmethod
    def get_type(self):
        pass

    def add_appointment_to_queue(self, appointment):
        self.queue.append(appointment)

    def delete_appointment_from_queue(self):
        self.queue.pop(0)

    def __str__(self):
        return f"Doctor ID: {self.doctor_id}\nName: {self.name}\nSpecialization: {self.specialization}\n" \
            f"Contact Number: {self.contact_number}\nEmail: {self.email}\nQualification: {self.qualification}\n" \
            f"Consultation Fee: {self.consultation_fee}\n" \
            f"Password: {self.password}\n"

    
# Concrete Pediatrician class
class Pediatrician(Doctor):
    def __init__(self, doctor_id, name,specialization, contact_number, email, qualification, available_hours, password):
        super().__init__(doctor_id, name, "Pediatrician", contact_number, email, qualification, available_hours, password)
        self.consultation_fee=200

    def get_type(self):
        return "Pediatrician"

# Concrete General Physician class
class GeneralPhysician(Doctor):
    def __init__(self, doctor_id, name,specialization, contact_number, email, qualification, available_hours, password):
        super().__init__(doctor_id, name, "General Physician", contact_number, email, qualification, available_hours, password)
        self.consultation_fee=200
    def get_type(self):
        return "General Physician"

# Concrete Cardiologist class
class Cardiologist(Doctor):
    def __init__(self, doctor_id, name,specialization, contact_number, email, qualification, available_hours, password):
        super().__init__(doctor_id, name, "Cardiologist", contact_number, email, qualification, available_hours, password)
        self.consultation_fee=300
    def get_type(self):
        return "Cardiologist"

# Concrete Dermatologist class
class Dermatologist(Doctor):
    def __init__(self, doctor_id, name,specialization, contact_number, email, qualification, available_hours, password):
        super().__init__(doctor_id, name, "Dermatologist", contact_number, email, qualification, available_hours, password)
        self.consultation_fee=400
    def get_type(self):
        return "Dermatologist"

# Concrete Neurologist class
class Neurologist(Doctor):
    def __init__(self, doctor_id, name, specialization, contact_number, email, qualification, available_hours, password):
        super().__init__(doctor_id, name, "Neurologist", contact_number, email, qualification, available_hours, password)
        self.consultation_fee = 350  # Adjust the consultation fee as needed

    def get_type(self):
        return "Neurologist"

# DoctorFactory class
class DoctorFactory:
    @staticmethod
    def create_doctor(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password):
        if specialization == "Pediatrician":
            return Pediatrician(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password)
        elif specialization == "General Physician":
            return GeneralPhysician(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password)
        elif specialization == "Cardiologist":
            return Cardiologist(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password)
        elif specialization == "Dermatologist":
            return Dermatologist(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password)
        elif specialization == "Neurologist":
            return Neurologist(doctor_id, name, specialization, contact_number, email, qualification, available_hours, password)
        else:
            raise ValueError("Invalid doctor type")


#########################################################################################################

#RECEPTIONIST MODULE



class Receptionist:
    def __init__(self, receptionist_id, name, contact_number, email,password):
        self.receptionist_id = receptionist_id  # Unique identifier for each receptionist
        self.name = name  # Full name of the receptionist
        self.contact_number = contact_number  # Contact number of the receptionist
        self.email = email  # Email address of the receptionist
        self.password = password # Password of the receptionist

    def __str__(self):
        return f"Receptionist ID: {self.receptionist_id}\nName: {self.name}\n" \
               f"Contact Number: {self.contact_number}\nEmail: {self.email}\n" \
               f"Password: {self.password}\n"


class ReceptionistBuilder:
    def set_receptionist_id(self, receptionist_id):
        pass

    def set_name(self, name):
        pass

    def set_contact_number(self, contact_number):
        pass

    def set_email(self, email):
        pass

    def set_password(self, password):
        pass

    def get_receptionist(self):
        pass


class ReceptionistBuilderImpl(ReceptionistBuilder):
    def __init__(self):
        self.receptionist = Receptionist(receptionist_id=None, name=None, contact_number=None, email=None, password=None)

    def set_receptionist_id(self, receptionist_id):
        self.receptionist.receptionist_id = receptionist_id
        return self

    def set_name(self, name):
        self.receptionist.name = name
        return self

    def set_contact_number(self, contact_number):
        self.receptionist.contact_number = contact_number
        return self

    def set_email(self, email):
        self.receptionist.email = email
        return self

    def set_password(self, password):
        self.receptionist.password = password
        return self

    def get_receptionist(self):
        return self.receptionist


class ReceptionistDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct_receptionist(self, receptionist_id, name, contact_number, email, password):
        self.builder.set_receptionist_id(receptionist_id)
        self.builder.set_name(name)
        self.builder.set_contact_number(contact_number)
        self.builder.set_email(email)
        self.builder.set_password(password)
        return self.builder.get_receptionist()


#########################################################################################################

#PATIENT MODULE

# Command interface
class PatientCommand(ABC):
    @abstractmethod
    def execute(self, patient):
        pass

# ConcreteCommand for adding a visit
class AddVisitCommand(PatientCommand):
    def __init__(self, visit):
        self.visit = visit

    def execute(self, patient):
        patient.add_visit(self.visit)

# ConcreteCommand for adding an invoice
class AddInvoiceCommand(PatientCommand):
    def __init__(self, invoice):
        self.invoice = invoice

    def execute(self, patient):
        patient.add_invoice(self.invoice)


# Receiver class (Patient)
class Patient:
    def __init__(self, patient_id, name, contact_number, email, password):
        self.patient_id = patient_id
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.password = password
        self.visits = []  # List to store patient's visits
        self.invoices = []  # List to store invoices
        

    def add_visit(self, visit):
        self.visits.append(visit)

    def add_invoice(self, invoice):
        self.invoices.append(invoice)
        print(invoice)

    def __str__(self):
        return f"Patient ID: {self.patient_id}\nName: {self.name}\n" \
               f"Contact Number: {self.contact_number}\nEmail: {self.email}\n" \
               f"Password: {self.password}\n"
    
    @classmethod
    def create_patient(cls, patient_id, name, contact_number, email, password):
        return Patient(patient_id, name, contact_number, email, password)

# Invoker class
class PatientInvoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def execute_command(self, patient):
        self.command.execute(patient)


#########################################################################################################

#APPOINTMENT MODULE


class Appointment:
    def __init__(self, patient_id, specialization, doctor_id, time_slot,description):
        self.patient_id = patient_id
        self.specialization = specialization
        self.doctor_id = doctor_id
        self.time_slot = time_slot
        self.description=description

    def __str__(self):
        return f"Appointment - Patient ID: {self.patient_id}, Specialization: {self.specialization}, Doctor ID: {self.doctor_id}, Time Slot: {self.time_slot}"

    @classmethod
    def create_appointment(cls,patient_id, specialization, doctor_id, time_slot,description):
            return Appointment(patient_id, specialization, doctor_id, time_slot,description)




class Visit:
    def __init__(self, patient_id, doctor_id, diagnosis, prescription, visit_date):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.visit_date = visit_date 

    def __str__(self):
        return f"Visit - Patient ID: {self.patient_id}, Doctor ID: {self.doctor_id}\nDate: {self.visit_date}\nDiagnosis: {self.diagnosis}\nPrescription: {self.prescription}"

    @classmethod
    def create_visit(cls, patient_id, doctor_id, diagnosis, prescription, visit_date):
        return Visit(patient_id, doctor_id, diagnosis, prescription, visit_date)




def get_patient_by_id(patient_id):
    # Replace this with your actual implementation to retrieve a patient by ID
    patients = load_patient_data()  # You need to implement a function like load_patient_data() to load patient data
    return next((patient for patient in patients if patient.patient_id == patient_id), None)


def load_patient_data():
    try:
        with open("patients_data.pkl", "rb") as pickle_file:
            loaded_patient_list = pickle.load(pickle_file)
        return loaded_patient_list
    except :
        return []


# Function to load doctor data from a pickle file
def load_doctor_data():
    try:
        with open("doctors_data.pkl", "rb") as pickle_file:
            loaded_doctor_list = pickle.load(pickle_file)
        return loaded_doctor_list
    except :
        return []


#FACADE
class AppointmentHandler:
    @staticmethod
    def handle_end_appointment(doctor, appointment, diagnosis, prescription, doctors):
        visit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Save visit details to the patient's visits
        visit = Visit.create_visit(appointment.patient_id, doctor.doctor_id, diagnosis, prescription, visit_date)
        add_visit_command = AddVisitCommand(visit)
        patient_invoker = PatientInvoker()
        # Update patient data
        patient_list = load_patient_data()
        for patient in patient_list:
            if patient.patient_id == appointment.patient_id:
                patient_invoker.set_command(add_visit_command)
                patient_invoker.execute_command(patient)
                add_invoice_command = AddInvoiceCommand(Invoice(patient.patient_id,patient.name, doctor.doctor_id,doctor.name,doctor.consultation_fee))
                patient_invoker.set_command(add_invoice_command)
                patient_invoker.execute_command(patient)
                
        with open("patients_data.pkl", "wb") as pickle_file:
            pickle.dump(patient_list, pickle_file)

        # Remove the appointment from the queue
        doctor.delete_appointment_from_queue()

        # Update doctor data
        for i, doc in enumerate(doctors):
            if doc.doctor_id == doctor.doctor_id:
                doctors[i] = doctor  # Update the doctor object in the list

        with open("doctors_data.pkl", "wb") as pickle_file:
            pickle.dump(doctors, pickle_file)


#########################################################################################################

#INVOICE MODULE

# Abstract base class representing the state of an invoice
class InvoiceState:
    def display_state(self):
        """
        Abstract method to be implemented by concrete state classes.
        Returns a string representation of the current state.
        """
        pass


# Concrete class representing the Pending state of an invoice
class PendingState(InvoiceState):
    def display_state(self):
        """Return a string indicating that the invoice is in the 'Pending' state."""
        return "Pending"


# Concrete class representing the Paid state of an invoice
class PaidState(InvoiceState):
    def display_state(self):
        """Return a string indicating that the invoice is in the 'Paid' state."""
        return "Paid"


# Class representing an invoice with different states
class Invoice:
    def __init__(self, patient_id, patient_name, doctor_id, doctor_name, total_amount):
        """
        Initialize an Invoice object with default values and the Pending state.

        Parameters:
        - patient_id (str): ID of the patient.
        - patient_name (str): Name of the patient.
        - doctor_id (str): ID of the doctor.
        - doctor_name (str): Name of the doctor.
        - total_amount (float): Total amount of the invoice.
        """
        self.invoice_number = self.generate_invoice_id()  # Generate a unique invoice number
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.total_amount = total_amount
        self.payment_details = None  # Payment details initially set to None
        self.state = PendingState()  # Initial state is set to Pending

    def generate_invoice_id(self):
        """
        Generate a unique 6-digit invoice ID based on a UUID.

        Returns:
        str: A 6-digit invoice ID.
        """
        # Generate a UUID and take the last 6 digits to get a 6-digit invoice ID
        return str(uuid.uuid4().int)[-6:]

    def mark_as_paid(self):
        """Change the state of the invoice to 'Paid' when the payment is completed."""
        self.state = PaidState()
        print("State changed to Paid")

    def get_invoice_details(self):
        """
        Return a formatted string with key details of the invoice.

        Returns:
        str: Invoice details including number, patient name, total amount, and payment status.
        """
        return f"Invoice Number: {self.invoice_number}\nPatient Name: {self.patient_name}\n" \
               f"Total Amount: ${self.total_amount}\nPayment Status: {self.state.display_state()}"

