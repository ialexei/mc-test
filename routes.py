import datetime

from flask import request
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from dto_converters import appointment_to_json, patient_to_json, practitioner_to_json
from error import InvalidParameter, RecordNotFound
from model import Appointment
from repository import create_appointment_repository, create_patient_repository, create_practitioner_repository

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mc-test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = None


def get_db_session():
  global db
  if db is None:
    db = SQLAlchemy(app)
  return db.session


@app.route('/api/patients/<int:patient_id>/appointments', methods=['GET'])
def get_patient_appointments(patient_id: int):
  appointment_repository = create_appointment_repository(get_db_session())
  query_results = appointment_repository.get_appointments_for_patient(
    patient_id=patient_id)
  output = [appointment_to_json(row) for row in query_results]
  return output, status.HTTP_200_OK


@app.route('/api/patients/<int:patient_id>/appointment', methods=['POST'])
def create_appointments(patient_id: int):
  payload = request.data
  # basic validation
  validate_appointment_request(payload)
  start_time = parse_datetime(payload['start_time'])
  if start_time.minute % 30 != 0:
    raise InvalidParameter('Specified appointment must '
                           'start and end on the hour or half hour')
  # Get patient
  patient_repository = create_patient_repository(get_db_session())
  patient = patient_repository.find_by_id(patient_id)
  if patient is None:
    raise RecordNotFound('Invalid patient id ' + str(patient_id))

  # Get practitioner
  practitioner_repository = create_practitioner_repository(get_db_session())
  practitioner = practitioner_repository.find_by_id(payload['practitioner_id'])
  if practitioner is None:
    raise RecordNotFound(
      'Invalid practitioner id ' + str(payload['practitioner_id']))

  # Check if patient already an appointment on the day
  appointment_repository = create_appointment_repository(get_db_session())
  if appointment_repository.is_patient_having_multiple_appointments(
    start_time, patient.id):
    raise InvalidParameter(
      'Patient with id ' + str(patient_id) +
      ' has an existing appointment on the same day')

  # Check if practitioner is busy
  end_time = start_time + datetime.timedelta(minutes=30)
  if appointment_repository.is_practitioner_busy(
    start_time, end_time, practitioner.id):
    raise InvalidParameter(
      'Practitioner with id ' + str(practitioner.id) +
      ' is booked for the specified time')

  new_appointment = Appointment(
    patient=patient,
    practitioner=practitioner,
    start_time=start_time,
    end_time=end_time)
  appointment_repository.create(new_appointment)
  appointment_repository.commit()

  return appointment_to_json(new_appointment), status.HTTP_201_CREATED


@app.route('/api/patients', methods=['GET'])
def get_all_patients():
  patient_repository = create_patient_repository(get_db_session())
  query_results = patient_repository.find_all()
  output = [patient_to_json(row) for row in query_results]
  return output, status.HTTP_200_OK


@app.route('/api/practitioners', methods=['GET'])
def get_all_practitioners():
  practitioner_repository = create_practitioner_repository(get_db_session())
  query_results = practitioner_repository.find_all()
  output = [practitioner_to_json(row) for row in query_results]
  return output, status.HTTP_200_OK


def parse_datetime(date_time_str):
  try:
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
  except:
    raise InvalidParameter('Specified appointment must be in '
                           'the format %Y-%m-%d %H:%M:%S')


def validate_appointment_request(payload_json):
  if payload_json is None:
    raise InvalidParameter('Missing input payload')
  if 'practitioner_id' not in payload_json:
    raise InvalidParameter('Missing key in payload practitioner_id')
  if 'start_time' not in payload_json:
    raise InvalidParameter('Missing key in payload start_time')

