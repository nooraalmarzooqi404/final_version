from collections import deque
from datetime import datetime

class Patient:
    '''A class to represent a patient'''

    # initalizing private attributes
    def __init__(self, patient_id, name, dob, medical_history, phone, allergies=None, current_medications=None):
        self.__patient_id = patient_id
        self.__name = name
        self.__dob = datetime.strptime(dob, "%Y-%m-%d")    # date of birth and its format
        self.__medical_history = medical_history
        self.__phone = phone       # phone number
        self.__allergies = allergies if allergies else []             # if ... else [] is a concise way to ensure these attributes are always lists,
                                                                      # which is good to avoid NoneType errors
        self.__current_medications = current_medications if current_medications else []
        self.__appointments = deque()  # queue of appointments waiting for consultation

    # setter and getter methods required for other methods introduced later in the code
    def get_details(self):
        return self.__patient_id, self.__name, self.__phone

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_medical_history(self, medical_history):
        self.__medical_history = medical_history

    def set_allergies(self, allergies):
        self.__allergies = allergies

    def set_current_medications(self, current_medications):
        self.__current_medications = current_medications

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)  #add the appointment to the end of the queue

    def get_appointments(self):
        return self.__appointments

    def remove_appointment(self):
        if self.__appointments:  #hheck if deque is not empty
            return self.__appointments.popleft()  #remove the first appointment from the queue
        return None  #return None if there are no appointments to remove


class Doctor:
    '''A class to represent doctors'''

    #initialize private attributes
    def __init__(self, doctor_id, name, specialization):
        self.__doctor_id = doctor_id
        self.__name = name
        self.__specialization = specialization

class Appointment:
    '''A class to represent appointments'''
    def __init__(self, appointment_id, patient_id, doctor_id, date, time):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__time = time

    # getter methods will be required latter on
    def get_details(self):
        return self.__appointment_id, self.__patient_id, self.__doctor_id, self.__date, self.__time

    def get_id(self):
        return self.__appointment_id


class Prescription:
    '''A class to represent prescriptions'''
    def __init__(self, prescription_id, patient_id, doctor_id, date, medication):
        self.__prescription_id = prescription_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__medication = medication

    # getter method required later on
    def get_details(self):
        return self.__prescription_id, self.__patient_id, self.__doctor_id, self.__date, self.__medication