import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Patient, Practitioner, Appointment
from repository import AppointmentRepository


class TestAppointmentRepository(unittest.TestCase):

  # Create db
  def setUp(self):
    db = create_engine('sqlite://', echo=True)
    Base.metadata.bind = db
    Base.metadata.create_all(db)

    DBSession = sessionmaker(bind=db)
    self.session = DBSession()

  def test_get_appointments(self):
    patient_alexei = Patient(first_name='alexei', last_name='isac')
    self.session.add(patient_alexei)

    patient_mathew = Patient(first_name='mathew', last_name='isac')
    self.session.add(patient_mathew)

    practitioner_bob = Practitioner(first_name='Bob', last_name='Dr', npi='1')
    self.session.add(practitioner_bob)

    appointment1 = Appointment(
      patient=patient_alexei, practitioner=practitioner_bob,
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=0, second=0))
    self.session.add(appointment1)

    appointment2 = Appointment(
      patient=patient_mathew, practitioner=practitioner_bob,
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=2, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=3, minute=0, second=0))
    self.session.add(appointment2)

    self.session.commit()
    appointment_repository = AppointmentRepository(session=self.session)

    result = appointment_repository.get_appointments_for_patient(
      patient_id=patient_alexei.id)
    count = 0
    for row in result:
      count += 1
      assert row.patient.id == patient_alexei.id
      assert row.practitioner.id == practitioner_bob.id
    assert count == 1

  def test_is_patient_having_multiple_appointments(self):
    patient_alexei = Patient(first_name='alexei', last_name='isac')
    self.session.add(patient_alexei)

    patient_mathew = Patient(first_name='mathew', last_name='isac')
    self.session.add(patient_mathew)

    practitioner_bob = Practitioner(first_name='Bob', last_name='Dr', npi='1')
    self.session.add(practitioner_bob)

    appointment1 = Appointment(
      patient=patient_alexei, practitioner=practitioner_bob,
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=0, second=0))
    self.session.add(appointment1)

    self.session.commit()

    appointment_repository = AppointmentRepository(session=self.session)
    assert appointment_repository.is_patient_having_multiple_appointments(
      patient_id=patient_alexei.id,
      appointment_date=datetime.datetime(year=2021, month=1, day=1)) == True

    assert appointment_repository.is_patient_having_multiple_appointments(
      patient_id=patient_alexei.id,
      appointment_date=datetime.datetime(year=2021, month=1, day=2)) == False

    assert appointment_repository.is_patient_having_multiple_appointments(
      patient_id=patient_mathew.id,
      appointment_date=datetime.datetime(year=2021, month=1, day=1)) == False

  def test_is_appointment_clashing(self):
    patient = Patient(first_name='alexei', last_name='isac')
    self.session.add(patient)

    practitioner_bob = Practitioner(first_name='Bob', last_name='Dr', npi='1')
    self.session.add(practitioner_bob)

    practitioner_alice = Practitioner(first_name='Alice', last_name='Dr', npi='2')
    self.session.add(practitioner_alice)

    appointment1 = Appointment(
      patient=patient, practitioner=practitioner_bob,
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=0, second=0))
    self.session.add(appointment1)

    appointment2 = Appointment(
      patient=patient, practitioner=practitioner_bob,
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=2, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=3, minute=0, second=0))
    self.session.add(appointment2)

    self.session.commit()

    appointment_repository = AppointmentRepository(self.session)

    # Should clash with 2nd appointment
    assert appointment_repository.is_practitioner_busy(
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=30, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=2, minute=30, second=0),
      practitioner_id=practitioner_bob.id) == True

    # Should not clash as its perfectly in the middle of 1 and 2
    assert appointment_repository.is_practitioner_busy(
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=30, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=2, minute=00, second=0),
      practitioner_id=practitioner_bob.id) == False

    # Appointment immidetely after last appt
    assert appointment_repository.is_practitioner_busy(
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=3, minute=0, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=3, minute=30, second=0),
      practitioner_id=practitioner_bob.id) == False

    # should not clash because this is for Alice
    assert appointment_repository.is_practitioner_busy(
      start_time=datetime.datetime(year=2021, month=1, day=1, hour=1, minute=30, second=0),
      end_time=datetime.datetime(year=2021, month=1, day=1, hour=2, minute=30, second=0),
      practitioner_id=practitioner_alice.id) == False


if __name__ == '__main__':
  unittest.main()
