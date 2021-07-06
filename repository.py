import datetime

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

from model import Appointment, Patient, Practitioner


class AbstractRepository:

  def __init__(self, session, model_class):
    self.session = session
    self.model_class = model_class

  def find_all(self):
    return self.session.query(self.model_class).all()

  def find_by_id(self, id):
    return self.session.query(self.model_class) \
      .filter(self.model_class.id == id).first()

  def create(self, model):
    self.session.add(model)
    return model

  def delete(self, model):
    self.session.remove(model)

  def commit(self):
    self.session.commit()

# Repository to encapsulate all queries for Appointment model
# so they could be unit tested
class AppointmentRepository(AbstractRepository):

  def __init__(self, session):
    AbstractRepository.__init__(self, session, Appointment)

  # Get all appointments for patient
  # (patient and practitioner eager loaded to keep this to 1 query)
  def get_appointments_for_patient(self, patient_id):
    result = self.session.query(Appointment) \
      .join(Patient) \
      .filter(Patient.id == patient_id) \
      .options(joinedload(Appointment.patient), joinedload(Appointment.practitioner))
    return result

  # Function checks to see if there is a clash in appointment for a practitioner
  def is_practitioner_busy(self, start_time, end_time, practitioner_id):
    result = self.session.query(Appointment).filter(
      and_(practitioner_id == Appointment.practitioner_id,
           or_(
             and_(start_time >= Appointment.start_time, start_time < Appointment.end_time),
             and_(end_time > Appointment.start_time, end_time < Appointment.end_time)
           ))).first()
    return result is not None

  # Function checks to see if patient already has an appoint for the day
  def is_patient_having_multiple_appointments(self, appointment_date:datetime, patient_id:int):
    start_of_day = datetime.datetime(
      year=appointment_date.year,
      month=appointment_date.month,
      day=appointment_date.day)
    end_of_day = appointment_date + datetime.timedelta(seconds=86400)
    result = self.session.query(Appointment).filter(
      and_(Appointment.patient_id == patient_id,
           Appointment.start_time >= start_of_day,
           Appointment.end_time <= end_of_day)).first()
    return result is not None


class PatientRepository(AbstractRepository):

  def __init__(self, session):
    AbstractRepository.__init__(self, session, Patient)


class PractitionerRepository(AbstractRepository):

  def __init__(self, session):
    AbstractRepository.__init__(self, session, Practitioner)


def create_appointment_repository(db_session):
  return AppointmentRepository(db_session)


def create_patient_repository(db_session):
  return PatientRepository(db_session)


def create_practitioner_repository(db_session):
  return PractitionerRepository(db_session)
