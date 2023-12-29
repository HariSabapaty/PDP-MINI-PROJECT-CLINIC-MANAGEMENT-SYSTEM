from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,flash
import pickle
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from .models import ClinicAdminSingleton,Receptionist
import json
from flask import render_template, request, redirect, url_for, flash

auth=Blueprint('auth',__name__)


@auth.route('/login')
def login():
    return render_template("login.html")




# Modify the load_admin_data function
def load_admin_data():
    try:
        # Read the JSON file and load the data back
        with open("admin_credentials.json", "r") as json_file:
            loaded_admin_list = json.load(json_file)

        # Retrieve the singleton instance of ClinicAdminSingleton
        admin_singleton_instance = ClinicAdminSingleton.get_instance(None, None)

        # Update the singleton instance with the loaded data
        admin_singleton_instance.username = loaded_admin_list[0]['username']
        admin_singleton_instance.password = loaded_admin_list[0]['password']

        # Now you can work with the admin_singleton_instance

        return [admin_singleton_instance]
    except FileNotFoundError:
        return None  # Return None or handle the absence of the file accordingly




@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    global adminlist
    adminlist = load_admin_data()
    print(adminlist)

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        for admin in adminlist:
            if admin.username == username:
                if admin.password == password:
                    flash("Login successful.")
                    session['admin_username'] = admin.username
                    session['admin_password'] = admin.password
                    return redirect(url_for('auth.admin_dashboard'))
                else:
                    flash("Invalid credentials. Please try again.")
                    # Show the pop-up and stay on the same page
                    return render_template("admin_login.html", boolean=True, show_popup=True)

        flash('You are not a recognized admin user')
        return redirect(url_for('auth.login'))

    else:
        # Check if the show_popup variable is set and pass it to the template
        show_popup = request.args.get('show_popup')
        # Check if the show_popup is not set (or set to False) when rendering the template
        return render_template("admin_login.html", boolean=True, show_popup= False)



@auth.route('/admin_dashboard')
def admin_dashboard():
    admin_username = session.get('admin_username')
    admin_password = session.get('admin_password')

    return render_template("admin_dashboard.html", admin_username=admin_username, admin_password=admin_password)
   



# Load receptionist data from pickle file
def load_receptionist_data():
    try:
        with open("receptionists_data.pkl", "rb") as pickle_file:
            loaded_receptionist_objects = pickle.load(pickle_file)

        return loaded_receptionist_objects
    except :
        return []


# Assuming you have a Flask Blueprint named 'auth'
@auth.route('/recep_login', methods=['GET', 'POST'])
def recep_login():
    
    global receptionist_list
    receptionist_list = load_receptionist_data()

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        for receptionist in receptionist_list:
            if receptionist.email == email:
                if receptionist.password== password:
                    session['recep_email'] = receptionist.email
                    session['recep_password'] = receptionist.password
                    flash("Login successful.")
                    return redirect(url_for('auth.recep_dashboard'))
                else:
                    flash("Invalid credentials. Please try again.")
                    # Show the pop-up and stay on the same page
                    return render_template("recep_login.html", boolean=True, show_popup=True)

        flash('You are not a recognized receptionist user')
        return redirect(url_for('auth.login'))

    else:
        # Check if the show_popup variable is set and pass it to the template
        show_popup = request.args.get('show_popup')
        # Check if the show_popup is not set (or set to False) when rendering the template
        return render_template("recep_login.html", boolean=True, show_popup=False)
    
def get_recep_by_email(recep_email):
    # Replace this with your actual implementation to retrieve a doctor by ID
    receps = load_receptionist_data()  # You need to implement a function like load_doctor_data() to load doctor data
    return next((receptionist for receptionist in receps if receptionist.email == recep_email), None)

@auth.route('/recep_dashboard')
def recep_dashboard():
    recep_email=session.get('recep_email')
    current_receptionist=get_recep_by_email(recep_email)
    return render_template("recep_dashboard.html", current_receptionist=current_receptionist)



@auth.route('/admin_signout')
def admin_signout():
    
    return render_template("login.html")



# Load doctor data from pickle file
def load_doctor_data():
    try:
        with open("doctors_data.pkl", "rb") as pickle_file:
            loaded_doctor_objects = pickle.load(pickle_file)

        return loaded_doctor_objects
    except :
        return []

# Assuming you have a Flask Blueprint named 'auth'
@auth.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    
    global doctor_list
    doctor_list = load_doctor_data()

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        for doctor in doctor_list:
            if doctor.email == email:
                if doctor.password == password:
                    session['current_doctor_id'] = doctor.doctor_id
                    flash("Login successful.")
                    return redirect(url_for('auth.doctor_dashboard'))
                else:
                    flash("Invalid credentials. Please try again.")
                    # Show the pop-up and stay on the same page
                    return render_template("doctor_login.html", boolean=True, show_popup=True)

        flash('You are not a recognized doctor user')
        return redirect(url_for('auth.login'))

    else:
        # Check if the show_popup variable is set and pass it to the template
        show_popup = request.args.get('show_popup')
        # Check if the show_popup is not set (or set to False) when rendering the template
        return render_template("doctor_login.html", boolean=True, show_popup=False)

def get_doctor_by_id(doctor_id):
    # Replace this with your actual implementation to retrieve a doctor by ID
    doctors = load_doctor_data()  # You need to implement a function like load_doctor_data() to load doctor data
    return next((doctor for doctor in doctors if doctor.doctor_id == doctor_id), None)

@auth.route('/doctor_dashboard')
def doctor_dashboard():
    # Retrieve doctor details from the session
    doctor_id = session.get('current_doctor_id')
    current_doctor = get_doctor_by_id(doctor_id)  # Implement a function to get doctor details by ID

    # Pass the doctor details to the template
    return render_template("doctor_dashboard.html", current_doctor=current_doctor)


# Load receptionist data from pickle file
def load_patient_data():
    try:
        with open("patients_data.pkl", "rb") as pickle_file:
            loaded_patient_objects = pickle.load(pickle_file)

        return loaded_patient_objects
    except :
        return []


# Assuming you have a Flask Blueprint named 'auth'
@auth.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    
    global patient_list
    patient_list = load_patient_data()

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        for patient in patient_list:
            if patient.email == email:
                if patient.password== password:
                    session['recep_email'] = patient.email
                    session['recep_password'] = patient.password
                    flash("Login successful.")
                    return redirect(url_for('auth.patient_dashboard'))
                else:
                    flash("Invalid credentials. Please try again.")
                    # Show the pop-up and stay on the same page
                    return render_template("patient_login.html", boolean=True, show_popup=True)

        flash('You are not a recognized patient user')
        return redirect(url_for('auth.login'))

    else:
        # Check if the show_popup variable is set and pass it to the template
        show_popup = request.args.get('show_popup')
        # Check if the show_popup is not set (or set to False) when rendering the template
        return render_template("patient_login.html", boolean=True, show_popup=False)
    

def get_patient_by_email(patient_email):
    # Replace this with your actual implementation to retrieve a patient by email
    patients = load_patient_data()  # You need to implement a function like load_patient_data() to load patient data
    return next((patient for patient in patients if patient.email == patient_email), None)


@auth.route('/patient_dashboard')
def patient_dashboard():
    # Retrieve patient details from the session
    patient_email = session.get('recep_email')
    current_patient = get_patient_by_email(patient_email)  # Implement a function to get patient details by email

    # Pass the patient details to the template
    return render_template("patient_dashboard.html", current_patient=current_patient)
