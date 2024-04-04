from collections import deque
from datetime import datetime, timedelta
from file1 import Patient, Doctor, Appointment, Prescription
from file2 import HospitalSystem


class UserAuth:
    '''A class to authenticate users before accessing the system'''
    def __init__(self):
        '''A private dictionary to store username and password (in real life this must be encrypted)'''
        self.__users = {"receptionist": "pass123",
                        "nurse": "nurse456"}

    def login(self, username, password):
        '''Check if the username and password match stored credentials'''
        if username in self.__users and self.__users[username] == password:
            print("Successful Login.\n")
            return True
        else:
            print("Invalid username or password. Please try again.\n")
            return False

auth = UserAuth()
print("Welcome to the Hospital Management System.")
# keep asking for credentials until successful login
while True:
    username = input("Username: ")
    password = input("Password: ")
    if auth.login(username, password):
        break

def main_menu(system):
    '''This is the main part of the software. It is a menu for actions users can take in a hospital'''
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Add patient record")
        print("2. Verify and remove patient record")
        print("3. Update patient record")
        print("4. Book an appointment")
        print("5. Cancel an appointment")
        print("6. Manage Queue")
        print("7. Issue a prescription")
        print("8. View recent prescriptions")
        print("9. Search for a patient and display a summary")
        print("10. Exit")

        choice = input("Enter your choice: ")         #user input of what they want to do

        # if 1 is entered
        if choice == "1":
            patient_id = input("Enter patient ID: ")        #ask for the patient ID
            #if the ID exists in the system
            if patient_id in system._HospitalSystem__patients:
                print("A patient with this ID already exists.")

                # fetch the existing patient record based on the ID
                patient = system._HospitalSystem__patients[patient_id]
                # confirm name and proceed accordingly
                confirmed_name = input(f"Is the patient's name {patient.get_details()[1]}? (Yes/No): ")
                if confirmed_name.lower() == 'yes':
                    print("Patient record already exists. No need to add again.")
                else:
                    print("Please double-check the patient ID and try again.")

            # if the patient ID does not exist, proceed to collect the patient's details
            else:
                name = input("Enter patient's name: ")
                dob = input("Enter patient's date of birth (YYYY-MM-DD): ")
                medical_history = input("Enter patient's medical history: ")
                phone = input("Enter patient's phone number: ")
                allergies = input("Enter patient's allergies (comma separated, leave blank if none): ")
                allergies_list = allergies.split(",") if allergies else []
                current_medications = input("Enter patient's current medications (comma separated, leave blank if none): ")
                medications_list = current_medications.split(",") if current_medications else []
                # register new patient in the Patient class
                new_patient = Patient(patient_id, name, dob, medical_history, phone, allergies_list, medications_list)
                #call the funtion to add the record
                system.add_patient_record(new_patient)

        # if 2 is chosen, verify the patient first and then remove it
        elif choice == "2":
            patient_id = input("Enter patient ID to remove: ")
            name = input("Enter patient's name for verification: ")
            phone = input("Enter patient's phone number for verification: ")
            system.verify_and_remove_patient_record(patient_id, name, phone)

        # if 3 is chosen ask for patient ID and check if the patient exits to update the record
        elif choice == "3":
            patient_id = input("Enter patient ID to update: ")
            if patient_id in system._HospitalSystem__patients:
                patient = system._HospitalSystem__patients[patient_id]

                # another menu for the user to choose what attribute they want to update
                print("\nSelect the patient detail to update:")
                print("1. Name")
                print("2. Phone Number")
                print("3. Medical History")
                print("4. Allergies")
                print("5. Current Medications")
                print("6. Exit Update")
                update_options = {
                    "1": "name",
                    "2": "phone",
                    "3": "medical_history",
                    "4": "allergies",
                    "5": "current_medications"
                }
                update_choice = input("Enter your choice: ")     # take user input

                # depending on the entered number, let the user update the corresponding attribute
                if update_choice in update_options:
                    new_value = input(f"Enter the new {update_options[update_choice]}: ")
                    system.update_patient_record(patient_id, update_options[update_choice], new_value)
                # if the entered number is not from 1 to 6
                else:
                    print("Invalid choice. Please enter a valid number or press '6' to exit update mode.")
            # if patient ID not found
            else:
                print("Patient ID does not exist in the system.")

        # if 4 is entered (main_menu) first check if there is a patient record
        # if there is a record allow booking. If not, ask the user to add the patient first
        elif choice == "4":
            phone = input("Enter patient's phone number: ")
            matching_patients = [patient for patient_id, patient in system._HospitalSystem__patients.items() if
                                 patient._Patient__phone == phone]
            if not matching_patients:
                print("No patient record found for that phone number. Please add the patient first.")
                continue

            patient = matching_patients[0]
            patient_id = patient._Patient__patient_id
            patient_name = patient._Patient__name

            # name confirmation
            patient_name_confirmation = input(f"Is the patient's name {patient_name}? (Yes/No): ")
            if patient_name_confirmation.lower() != 'yes':
                print("Patient name does not match. Please try again.")
                continue
            # choose specialization depending on patient need
            print("\nAvailable Specializations:")
            for specialization in system._HospitalSystem__doctors:
                print(f"{specialization}")
            chosen_specialization = input("Choose a specialization: ")
            if chosen_specialization not in system._HospitalSystem__doctors:
                print("Specialization not found. Please try again.")
                continue
            # choose doctor
            print("\nAvailable Doctors:")
            for idx, doctor in enumerate(system._HospitalSystem__doctors[chosen_specialization], start=1):
                print(f"{idx}. {doctor._Doctor__name}")

            chosen_doctor_index = int(input("Choose a doctor by number: ")) - 1
            if not (0 <= chosen_doctor_index < len(system._HospitalSystem__doctors[chosen_specialization])):
                print("Invalid doctor choice. Please try again.")
                continue
            chosen_doctor = system._HospitalSystem__doctors[chosen_specialization][chosen_doctor_index]
            doctor_id = chosen_doctor._Doctor__doctor_id
            # printing available appointment dates and times
            time_slots = system.generate_time_slots()
            print("\nAvailable Appointment Slots:")
            for idx, slot in enumerate(time_slots, start=1):
                print(f"{idx}. Date: {slot[0]}, Time: {slot[1]}")

            # choose appointment slot
            chosen_slot_index = int(input("Choose a slot number: ")) - 1
            if not (0 <= chosen_slot_index < len(time_slots)):
                print("Invalid slot choice. Please try again.")
                continue
            chosen_date, chosen_time = time_slots[chosen_slot_index]

            # booking the appointment by calling book_appointment function
            system.book_appointment(patient_id, doctor_id, chosen_date, chosen_time)

        # if 5 is entered, cancel the appointment by appointment ID
        elif choice == "5":
            appointment_id = input("Enter appointment ID: ")
            system.cancel_appointment(appointment_id)

        # if 6 is entered, show the user how the queue is managed. Once a consultation is completed, show the next patient
        # queue is managed by time. The earliest first
        elif choice == "6":
            print("Managing Queue...")
            system.manage_queue()

        # if 7 is entered, issue a prescription by taking user input
        elif choice == "7":
            patient_id = input("Enter patient ID: ")
            doctor_id = input("Enter doctor ID: ")
            medication = input("Enter medication details: ")
            system.issue_prescription(patient_id, doctor_id, medication)
        # if 8 is entered, ask the user how many latest prescriptions they want to see and print it
        elif choice == "8":
            count = input("How many recent prescriptions do you want to see? ")
            try:
                count = int(count)
            except ValueError:
                print("Please enter a valid number.")
                continue
            recent_prescriptions = system.get_recent_prescriptions(count)
            print("\nRecent Prescriptions:")
            for prescription in recent_prescriptions:
                prescription_id, patient_id, doctor_id, date, medication = prescription.get_details()
                print(f"Prescription ID: {prescription_id}, Patient ID: {patient_id}, Doctor ID: {doctor_id}, Date: {date}, Medication: {medication}")

        # if the choice is 9, find the patient by their ID and print their summary
        elif choice == "9":
            patient_id = input("Enter patient ID to search: ")
            system.search_patient_summary(patient_id)
        # exit the system if the choice is 10
        elif choice == "10":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


# creating an instance to get the program to run
if __name__ == "__main__":
    hospital_system = HospitalSystem()
    main_menu(hospital_system)