from flask import Blueprint,render_template,session
from .models import ClinicAdminSingleton,Doctor,Receptionist,Patient,Appointment,DoctorFactory,AppointmentHandler,ReceptionistDirector,ReceptionistBuilderImpl
import json,pickle
from flask import request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

views=Blueprint('views',__name__)



@views.route('/')
def home():
    return render_template('home.html')


@views.route('/admin_doc')
def admin_doc():
    doctorlist = load_doctor_data()  # Make sure to load the doctorlist here or from your database

    return render_template('admin_doc.html', doctorlist=doctorlist)

# Function to load doctor data from a pickle file
def load_doctor_data():
    try:
        with open("doctors_data.pkl", "rb") as pickle_file:
            loaded_doctor_list = pickle.load(pickle_file)
        return loaded_doctor_list
    except :
        return []

# Route for admin to manage doctors
@views.route('/add_doc', methods=['GET', 'POST'])
def add_doc():
    doctorlist = load_doctor_data()

    if request.method == 'POST':
        # Assuming you have a form with fields like 'name', 'specialization', etc.
        doctor_data = {
            'doctor_id': request.form.get("doctor_id"),
            'name': request.form.get("name"),
            'specialization': request.form.get("specialization"),
            'contact_number': request.form.get("contact_number"),
            'email': request.form.get("email"),
            'qualification': request.form.get("qualification"),
            'available_hours': request.form.getlist("available_hours"),# Assuming multiple hours can be selected
            'password': request.form.get("password") 
            # Add other relevant details as needed
        }

        # Create a new Doctor object from the form data using the factory method
        new_doctor = DoctorFactory.create_doctor(**doctor_data)
        print(new_doctor)

        # Add the new doctor to the list and update the pickle file
        doctorlist.append(new_doctor)

        with open("doctors_data.pkl", "wb") as pickle_file:
            pickle.dump(doctorlist, pickle_file)

        send_doctor_email(new_doctor)

        flash('Doctor added successfully.')
        return redirect(url_for('views.add_doc'))

    else:
        return render_template("add_doc.html", doctorlist=doctorlist)

def send_doctor_email(doctor):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'harisabapaty@gmail.com'
    smtp_password =os.environ.get('smtp_password')
    sender_email = 'harisabapaty@gmail.com'

    # Create a message with doctor details
    subject = 'Welcome to Apollo Clinic'
    body = f"Hello {doctor.name},\n\nYou have been successfully added as a doctor. Here are your details:\n\n{str(doctor)}"
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = doctor.email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [doctor.email], msg.as_string())


# Route to delete a doctor
@views.route('/delete_doc', methods=['GET', 'POST'])
def delete_doc():
    doctorlist = load_doctor_data()

    if request.method == 'POST':
        doctor_id_to_delete = request.form.get("doctor_id")

        # Find and remove the doctor from the list
        doctor_to_delete = next((doctor for doctor in doctorlist if doctor.doctor_id == doctor_id_to_delete), None)

        if doctor_to_delete:
            doctorlist.remove(doctor_to_delete)

            # Update the pickle file
            with open("doctors_data.pkl", "wb") as pickle_file:
                pickle.dump(doctorlist, pickle_file)

            flash(f'Doctor {doctor_id_to_delete} deleted successfully.')
        else:
            flash(f'Doctor {doctor_id_to_delete} not found.')

        return redirect(url_for('views.delete_doc'))

    else:
        return render_template("delete_doc.html", doctorlist=doctorlist)



# Import necessary modules and classes

@views.route('/admin_recep')
def admin_recep():
    receptionistlist = load_receptionist_data()  # Make sure to load the receptionistlist here or from your database

    return render_template('admin_recep.html', receptionistlist=receptionistlist)


# Function to load receptionist data from a pickle file
def load_receptionist_data():
    try:
        with open("receptionists_data.pkl", "rb") as pickle_file:
            loaded_receptionist_list = pickle.load(pickle_file)
        return loaded_receptionist_list
    except :
        return []


# Assume Receptionist, ReceptionistBuilder, ReceptionistBuilderImpl, and ReceptionistDirector are defined as before

# Route for admin to manage receptionists
@views.route('/add_recep', methods=['GET', 'POST'])
def add_recep():
    receptionistlist = load_receptionist_data()

    if request.method == 'POST':
        # Assuming you have a form with fields like 'name', 'role', etc.
        receptionist_director = ReceptionistDirector(ReceptionistBuilderImpl())

        # Construct a new Receptionist object using the director
        new_receptionist = receptionist_director.construct_receptionist(
            receptionist_id=request.form.get("receptionist_id"),
            name=request.form.get("name"),
            contact_number=request.form.get("contact_number"),
            email=request.form.get("email"),
            password=request.form.get("password")
        )

        # Add the new receptionist to the list and update the pickle file
        receptionistlist.append(new_receptionist)

        with open("receptionists_data.pkl", "wb") as pickle_file:
            pickle.dump(receptionistlist, pickle_file)

        send_recep_email(new_receptionist)

        flash('Receptionist added successfully.')
        return redirect(url_for('views.add_recep'))

    else:
        return render_template("add_recep.html", receptionistlist=receptionistlist)

def send_recep_email(receptionist):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'harisabapaty@gmail.com'
    smtp_password =os.environ.get('smtp_password')
    sender_email = 'harisabapaty@gmail.com'

    # Create a message with receptionist details
    subject = 'Welcome to Apollo Clinic'
    body = f"Hello {receptionist.name},\n\nYou have been successfully added as a receptionist. Here are your details:\n\n{str(receptionist)}"
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receptionist.email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [receptionist.email], msg.as_string())


@views.route('/delete_recep', methods=['GET', 'POST'])
def delete_recep():
    receptionistlist = load_receptionist_data()

    if request.method == 'POST':
        receptionist_id_to_delete = request.form.get("receptionist_id")

        # Find and remove the receptionist from the list
        receptionist_to_delete = next((receptionist for receptionist in receptionistlist if receptionist.receptionist_id == receptionist_id_to_delete), None)

        if receptionist_to_delete:
            receptionistlist.remove(receptionist_to_delete)

            # Update the pickle file
            with open("receptionists_data.pkl", "wb") as pickle_file:
                pickle.dump(receptionistlist, pickle_file)

            flash(f'Receptionist {receptionist_id_to_delete} deleted successfully.')
        else:
            flash(f'Receptionist {receptionist_id_to_delete} not found.')

        return redirect(url_for('views.delete_recep'))

    else:
        return render_template("delete_recep.html", receptionistlist=receptionistlist)




# Function to load patient data from a pickle file
def load_patient_data():
    try:
        with open("patients_data.pkl", "rb") as pickle_file:
            loaded_patient_list = pickle.load(pickle_file)
        return loaded_patient_list
    except Exception as e:
        print(f"Error loading patient data: {e}")
        return []

# Route for admin to manage patients
@views.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    patient_list = load_patient_data()

    if request.method == 'POST':
        # Assuming you have a form with fields like 'name', 'contact_number', etc.
        patient_data = {
            'patient_id': request.form.get("patient_id"),
            'name': request.form.get("name"),
            'contact_number': request.form.get("contact_number"),
            'email': request.form.get("email"),
            'password': request.form.get("password"),
            # Add other relevant details as needed
        }

        # Create a new Patient object from the form data using the factory method
        new_patient = Patient.create_patient(**patient_data)
        print(new_patient)

        # Add the new patient to the list and update the pickle file
        patient_list.append(new_patient)

        with open("patients_data.pkl", "wb") as pickle_file:
            pickle.dump(patient_list, pickle_file)
        
        send_patient_email(new_patient)

        flash('Patient added successfully.')
        return redirect(url_for('views.add_patient'))

    else:
        return render_template("add_patient.html", patient_list=patient_list)

def send_patient_email(patient):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'harisabapaty@gmail.com'
    smtp_password =os.environ.get('smtp_password')
    sender_email = 'harisabapaty@gmail.com'

    # Create a message with patient details
    subject = 'Welcome to Apollo Clinic'
    body = f"Hello {patient.name},\n\nYou have been successfully added as a patient. Here are your details:\n\n{str(patient)}"
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = patient.email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [patient.email], msg.as_string())


# Function to load appointment data from a pickle file
def load_appointment_data():
    try:
        with open("appointments_data.pkl", "rb") as pickle_file:
            loaded_appointment_list = pickle.load(pickle_file)
        return loaded_appointment_list
    except:
        return []
# Route for admin to manage appointments
@views.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    appointment_list = load_appointment_data()
    doctor_list = load_doctor_data()

    if request.method == 'POST':
        # Assuming you have a form with fields like 'patient_id', 'specialization', etc.
        appointment_data = {
            'patient_id': request.form.get("patient_id"),
            'specialization': request.form.get("specialization"),
            'doctor_id': request.form.get("doctor_id"),
            'time_slot': request.form.get("time_slot"),
            'description': request.form.get("description")
        }

        # Create a new Appointment object from the form data using the factory method
        new_appointment = Appointment.create_appointment(**appointment_data)

        # Add the new appointment to the list and update the pickle file
        appointment_list.append(new_appointment)

        # Enqueue the appointment into the corresponding doctor's queue
        doctor_id = request.form.get("doctor_id")
        doctor = next((doctor for doctor in doctor_list if doctor.doctor_id == doctor_id), None)
        
        if doctor:
            doctor.add_appointment_to_queue(new_appointment)
            # Update the pickle file for doctors
            with open("doctors_data.pkl", "wb") as pickle_file:
                pickle.dump(doctor_list, pickle_file)

        # Update the pickle file for appointments
        with open("appointments_data.pkl", "wb") as pickle_file:
            pickle.dump(appointment_list, pickle_file)

        flash('Appointment added successfully.')
        return redirect(url_for('views.add_appointment'))

    else:
        return render_template("add_appointment.html", appointment_list=appointment_list, patient_list=load_patient_data(), doctor_list=doctor_list)




@views.route('/admin_patients')
def admin_patients():
    return render_template('admin_patients.html', patients=load_patient_data())


# Flask route to display appointments in the HTML page
@views.route('/queue')
def queue():
    doctors_data = load_doctor_data()

    return render_template('queue.html', doctors_data=doctors_data)




# Assuming 'app' is your Flask app
@views.route('/doc_queue')
def doc_queue():
    # Assuming you have a session variable 'current_doctor_id' to store the ID of the logged-in doctor
    current_doctor_id = session.get('current_doctor_id')
    doctors_data=load_doctor_data()
    # Assuming 'doctors_data' is a list of doctors with their respective queues
    for doctor in doctors_data:
        if doctor.doctor_id == current_doctor_id:
            # Filter appointments for the current doctor
            doctor_queue = doctor.queue
            return render_template('doc_queue.html', doctor=doctor, doctor_queue=doctor_queue)

    # Redirect to login if the doctor is not found or not logged in
    return redirect(url_for('auth.login'))



def get_patient_by_id(patient_id):
    # Replace this with your actual implementation to retrieve a patient by ID
    patients = load_patient_data()  # You need to implement a function like load_patient_data() to load patient data
    return next((patient for patient in patients if patient.patient_id == patient_id), None)

# ... (Your existing code)
# ... (Your existing code)







# ... (Your existing code)

@views.route('/out_patient', methods=['GET', 'POST'])
def out_patient():
    # Retrieve the current doctor from the session
    doctors = load_doctor_data()
    doctor_id = session.get('current_doctor_id')
    doctor = next((d for d in doctors if d.doctor_id == doctor_id), None)

    if doctor is None:
        return "Doctor not found"

    
    if request.method == 'POST':
        # Doctor clicked "End Appointment" button
        if doctor.queue:
            appointment = doctor.queue[0]
            diagnosis = request.form.get('diagnosis')
            prescription = request.form.get('prescription')
            current_patient_id = appointment.patient_id
            
            # Use the AppointmentHandler facade
            AppointmentHandler.handle_end_appointment(doctor, appointment, diagnosis, prescription, doctors)

            # Reload the updated doctor data
            doctors = load_doctor_data()
            doctor = next((d for d in doctors if d.doctor_id == doctor_id), None)

    # Retrieve the patient's visit history

    if doctor.queue:
        current_appointment = doctor.queue[0]
        patient= get_patient_by_id(current_appointment.patient_id)
        all_visits = patient.visits if patient else []

    else:
        current_appointment = None
        all_visits=None
    # Retrieve all visits for the patient
    
    return render_template('out_patient.html', doctor=doctor, current_appointment=current_appointment, doctors=doctors, all_visits=all_visits)




def filter_invoices_by_status(patient, status):
    filtered_invoices = []
    for invoice in patient.invoices:
        print(f"Invoice State: {invoice.state.display_state()}")
        if invoice.state.display_state() == status:
            filtered_invoices.append(invoice)
    return filtered_invoices



@views.route('/recep_invoice')
def recep_invoice():
    # Load patient data
    patients = load_patient_data()
    print(patients)
    # Filter pending and paid invoices
    pending_invoices = []
    paid_invoices = []

    for patient in patients:
        pending_invoices.extend(filter_invoices_by_status(patient,"Pending"))
        paid_invoices.extend(filter_invoices_by_status(patient,"Paid"))
    print(pending_invoices,paid_invoices)

    return render_template('recep_invoice.html', pending_invoices=pending_invoices, paid_invoices=paid_invoices)



@views.route('/process_payment', methods=['POST'])
def process_payment():
    if request.method == 'POST':
        # Get payment details from the form
        invoice_number = request.form.get('invoice_number')
        patient_name = request.form.get('patient_name')
        doctor_name = request.form.get('doctor_name')
        total_amount = request.form.get('total_amount')
        payment_status = request.form.get('payment_status')
        
        patients=load_patient_data()
        for patient in patients:
            for invoice in patient.invoices:
                print("sana")
        
                if str(invoice.invoice_number) == str(invoice_number):
                    print("NJFRNJFJRF")
                    invoice.mark_as_paid()
        
        with open("patients_data.pkl", "wb") as pickle_file:
                pickle.dump(patients, pickle_file)


        # Determine the selected payment method
        payment_method = request.form.get('payment_method')

        if payment_method == 'cash':
            print(payment_status)

            # Redirect to cashpayment.html
            return redirect('/cashpayment?invoice_number={}&patient_name={}&doctor_name={}&total_amount={}&payment_status={}'.format(
                invoice_number, patient_name, doctor_name, total_amount, payment_status
            ))
        elif payment_method == 'card':
            # Redirect to cardpayment.html
            return redirect('/cardpayment?invoice_number={}&patient_name={}&doctor_name={}&total_amount={}&payment_status={}'.format(
                invoice_number, patient_name, doctor_name, total_amount, payment_status
            ))

    # Handle invalid requests or unexpected situations
    return render_template('error.html', message='Invalid request')

@views.route('/cashpayment')
def cash_payment():
    # Your logic for rendering the cashpayment.html page
    # ...

    return render_template('cashpayment.html')

@views.route('/cardpayment')
def card_payment():
    # Your logic for rendering the cardpayment.html page
    # ...

    return render_template('cardpayment.html')


@views.route('/success',methods=['GET','POST'])
def success():
    if request.method=="POST":
            
        invoice_number = request.form.get('invoice_number')
        print(invoice_number)
        patient_name = request.form.get('patient_name')
        doctor_name = request.form.get('doctor_name')
        total_amount = request.form.get('total_amount')
        payment_status = request.form.get('payment_status')
        
    return  render_template("success.html")



