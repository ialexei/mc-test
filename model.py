# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Practitioner(Base):
    __tablename__ = 'practitioner'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    npi = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    practitioner_id = Column(ForeignKey('practitioner.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    patient = relationship('Patient')
    practitioner = relationship('Practitioner')
