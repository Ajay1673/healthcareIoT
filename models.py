from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer,String
from sqlalchemy.orm import relationship
from database import Base,engine

class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, autoincrement=True,index=True)
    doctor_id = Column(String(25),primary_key=True)
    doctor_name = Column(String(50))
    doctor_specialization = Column(String(50))
    doctor_email = Column(String(50))
    doctor_phone = Column(String(50))
    doctor_password = Column(String(50))
    status = Column(String(50))
    created_on = Column(String(50), nullable=False)


class Nurse(Base):
    __tablename__ = "nurse"

    id = Column(Integer, autoincrement=True,index=True)
    nurse_id = Column(String(25),primary_key=True)
    nurse_name = Column(String(50))
    nurse_email = Column(String(50))
    nurse_phone = Column(String(50))
    nurse_password = Column(String(50))
    status = Column(String(50))
    created_on = Column(String(50), nullable=False)

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, autoincrement=True)
    patient_id = Column(String(25),primary_key=True)
    patient_name = Column(String(50))
    patient_email = Column(String(50))
    patient_phone = Column(String(50))
    patient_address = Column(String(50))
    patient_disease = Column(String(100))
    patient_gender = Column(String(50))
    patient_age = Column(String(50))
    patient_cause = Column(String(200))
    doctor_id = Column(String(50),ForeignKey("doctor.doctor_id"))
    doctor_name = Column(String(50))
    status = Column(String(50))
    created_on = Column(String(50), nullable=False)


Base.metadata.create_all(bind=engine)