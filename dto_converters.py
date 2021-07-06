from model import Appointment, Patient, Practitioner


def appointment_to_json(appointment: Appointment):
  return {
    'appointment_id': appointment.id,
    'patient_id': appointment.patient_id,
    'patient_first_name': appointment.patient.first_name,
    'patient_last_name': appointment.patient.last_name,
    'practitioner_id': appointment.practitioner_id,
    'practitioner_first_name': appointment.practitioner.first_name,
    'practitioner_last_name': appointment.practitioner.last_name,
    'practitioner_npi': appointment.practitioner.npi,
    'start_time': appointment.start_time.strftime("%Y-%m-%d %H:%M:%S"),
    'end_time': appointment.end_time.strftime("%Y-%m-%d %H:%M:%S"),
  }


def patient_to_json(patient: Patient):
  return {
    'id': patient.id,
    'first_name': patient.first_name,
    'last_name': patient.last_name,
  }


def practitioner_to_json(practitioner: Practitioner):
  return {
    'id': practitioner.id,
    'first_name': practitioner.first_name,
    'last_name': practitioner.last_name,
    'npi': practitioner.npi,
  }
