from collections import deque
from datetime import datetime, timedelta
from file1 import Patient, Doctor, Appointment, Prescription

class HospitalSystem:
    '''A class to represent a hospital system to manage different operations'''
    def __init__(self):
        # predefined patients (like a database) in which we gather all registered patients' records
        self.__patients = {
            "P001": Patient("P001", "Noora Almarzooqi", "2005-02-03", "diabetes", "0551234567", ["Penicillin"], ["Aspirin"]),
            "P002": Patient("P002", "Mohammad Ahmed", "1985-05-05", "None", "0526789012"),
            "P003": Patient("P003", "John Brown", "2000-08-12", "None", "0501234567"),
            "P004": Patient("P004", "Reem Albloushi", "2007-04-23", "Hypertension", "05555555555"),
            "P005": Patient("P005", "Chloe smith", "1995-07-30", "None", "0500000000")
        }

        # predefined doctors grouped by specialization (in real life, there will be many doctor)
        self.__doctors = {
            "Cardiology": [Doctor("D001", "Dr. Muna Omar", "Cardiology")],
            "Neurology": [Doctor("D002", "Dr. Mohammad Ahmed", "Neurology")],
            "General Practice": [Doctor("D003", "Dr. Micheal Baker", "General Practice")]
        }

        self.__appointments = deque()  # queue of appointments for all patients
        self.__prescriptions = []  # a list to represent a stack of prescriptions

    def add_patient_record(self, patient):
        '''A function to add a patient record'''

        #if the patient ID not found in self.__patients dictionary
        if patient.get_details()[0] not in self.__patients:
            # create an instance of Patient class which will be added to self.__patients
            self.__patients[patient.get_details()[0]] = patient
            print("Patient record added successfully.")
        else:
            print("Patient already exists in the system.")


    def verify_and_remove_patient_record(self, patient_id, name, phone):
        '''A function to remove patient record and verifying it'''

        # if the provided 'patient_id' exists as a key in the self__patients dictionary (if the record exists)
        if patient_id in self.__patients:
            # retrieve the details of the patient using the 'get_details' method of the patient object
            stored_id, stored_name, stored_phone = self.__patients[patient_id].get_details()

            # check if both the provided 'name' and 'phone' match the stored values for the patient
            # this serves as a verification step before removal
            if name == stored_name and phone == stored_phone:
                del self.__patients[patient_id]     # if confirmed, delete record
                print("Patient record removed successfully.")
            else:
                print("Patient details do not match. Removal canceled.")  # details are wrong
        else:
            print("Patient not found in the system.")       # patient ID not found

    def update_patient_record(self, patient_id, update_choice, new_value):
        '''A function to update an existing record'''
        # first check if the record exits
        if patient_id in self.__patients:
            # retrieve the patient object associated with 'patient_id' from the self.__patients dictionary
            # and assign it to the variable 'patient'
            patient = self.__patients[patient_id]

            # user chooses what attribute to update
            if update_choice == "name":
                patient.set_name(new_value)
            elif update_choice == "phone":
                patient.set_phone(new_value)
            elif update_choice == "medical_history":
                patient.set_medical_history(new_value)
            elif update_choice == "allergies":
                patient.set_allergies(new_value.split(","))
            elif update_choice == "current_medications":
                patient.set_current_medications(new_value.split(","))
            print("Patient record updated successfully.")
        else:
            print("Patient not found in the system.")

    def add_doctor(self, doctor):
        '''Extra function in case of a new employeed doctor'''
        self.__doctors.setdefault(doctor.specialization, []).append(doctor)  # append new doctor according to specialization

    def generate_time_slots(self):
        '''A function to generate appointment slots'''
        booked_slots = [(appointment._Appointment__date, appointment._Appointment__time) for appointment in self.__appointments]
        slots = []
        for day in range(5):  #next 5 days
            date = (datetime.now() + timedelta(days=day)).date()
            for hour in [9, 14]:  #9 AM for morning and 2 PM for afternoon slots
                time = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0).time()
                if (date, time) not in booked_slots:
                    slots.append((date, time))
            if len(slots) >= 10:
                break
        return slots

    def book_appointment(self, patient_id, doctor_id, date, time):
        '''A funciton to book an appointment and add to the queue. The queue is then sorted from earliest appointment to latest'''
        if patient_id in self.__patients:
            patient = self.__patients[patient_id]
        else:
            print("Patient not found in the system.")
            return

        appointment_id = f"A{len(self.__appointments) + 1}"
        new_appointment = Appointment(appointment_id, patient.get_details()[0], doctor_id, date, time)
        self.__appointments.append(new_appointment)  #add to the end of the queue
        self.__appointments = deque(sorted(self.__appointments, key=lambda x: (x._Appointment__date, x._Appointment__time)))
        patient.add_appointment(new_appointment)
        print(f"Appointment {appointment_id} booked successfully for {date} at {time}.")

    def cancel_appointment(self, appointment_id):
        '''A funciton to cancel appointments from the queue and them remove the appointment from the individual patient record'''
        found = False
        for appointment in list(self.__appointments):  # iterate over a shallow copy to safely remove from the original deque
            if appointment.get_id() == appointment_id:
                self.__appointments.remove(appointment)  # remove the appointment from the system's queue
                found = True
                break

        if found:
            for patient in self.__patients.values():  # ensure to remove the appointment from the correct patient
                patient_appointments = patient.get_appointments()
                for patient_appointment in list(patient_appointments):  # Iterate over a shallow copy to safely modify
                    if patient_appointment.get_id() == appointment_id:  # check ID
                        patient.remove_appointment()
                        print(f"Appointment {appointment_id} cancelled successfully.")
                        return
        else:
            print("Appointment not found in the system.")


    def manage_queue(self):
        '''A fucntion to manage the queue of patients'''
        # if the appointment queue is empty
        if not self.__appointments:
            print("There are no appointments in the queue.")
            return

        while self.__appointments:
            appointment = self.__appointments.popleft()  #pop the earliest appointment
            patient_id = appointment._Appointment__patient_id  # access the patient ID associated with the appointment
            patient = self.__patients.get(patient_id) #retrieve the patient object using the patient_id

            # if the patient is found in the system
            if patient:
                print(f"\nConsulting Patient: {patient._Patient__name} (ID: {patient_id})")
                print(
                    f"Appointment Date: {appointment._Appointment__date}, Time: {appointment._Appointment__time.strftime('%H:%M')}")
                print(f"Appointment {appointment._Appointment__appointment_id} is now being consulted.")

                # simulate the consultation and remove the appointment from the patient's queue
                patient_appointment = patient.remove_appointment()
                if patient_appointment:
                    print(f"Appointment {patient_appointment.get_id()} completed successfully.")

                # after consulting the current patient, check if there are more appointments
                if self.__appointments:
                    next_appointment = self.__appointments[0]
                    next_patient_id = next_appointment._Appointment__patient_id
                    next_patient = self.__patients.get(next_patient_id)
                    if next_patient:
                        print(
                            f"Next Patient: {next_patient._Patient__name} (ID: {next_patient_id}), Appointment Date: {next_appointment._Appointment__date}, Time: {next_appointment._Appointment__time.strftime('%H:%M')}")
                else:
                    print("There are no more patients in the queue.")


    def issue_prescription(self, patient_id, doctor_id, medication):
        '''Issue a new prescription to a patient'''
        prescription_id = f"P{len(self.__prescriptions) + 1}"
        date = datetime.now().date()
        new_prescription = Prescription(prescription_id, patient_id, doctor_id, date, medication)
        self.__prescriptions.append(new_prescription)  # add the prescription to the stack
        print(f"Prescription {prescription_id} issued successfully.")

    def get_recent_prescriptions(self, count=5):
        '''Retrieve the most recent prescriptions issued'''
        return list(reversed(self.__prescriptions[-count:]))

    def search_patient_summary(self, patient_id):
        '''Search for a patient by their ID and print their summary'''
        if patient_id not in self.__patients:
            print("Patient not found in the system.")
            return

        patient = self.__patients[patient_id]
        patient_details = patient.get_details()
        patient_appointments = patient.get_appointments()
        print(f"\nPatient Summary for {patient_details[1]} (ID: {patient_details[0]})")
        print(f"Phone: {patient_details[2]}")
        print(f"Allergies: {', '.join(patient._Patient__allergies) if patient._Patient__allergies else 'None'}")
        print(
            f"Current Medications: {', '.join(patient._Patient__current_medications) if patient._Patient__current_medications else 'None'}")

        if patient_appointments:
            next_appointment = patient_appointments[0]
            doctor_id = next_appointment._Appointment__doctor_id
            doctor = next(filter(lambda d: any(doctor._Doctor__doctor_id == doctor_id for doctor in d), self.__doctors.values()))
            if doctor:
                doctor = doctor[0]
                print(f"Next Appointment with Dr. {doctor._Doctor__name} (Specialization: {doctor._Doctor__specialization}) on {next_appointment._Appointment__date} at {next_appointment._Appointment__time}.")
            else:
                print("Doctor details not found.")
        else:
            print("No upcoming appointments.")