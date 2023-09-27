from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.encoders import jsonable_encoder
import models
from database import engine
from datetime import datetime
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/assets",StaticFiles(directory="D:/healthcareIoT/templates/assets"))

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
# Routes
@app.get('/')
def home(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse('home.html',context={"request":request})

@app.get('/doctor_register')
def docregister(request:Request):
    return templates.TemplateResponse('docregister.html',context={"request":request})

@app.get('/nurse_register')
def nurregister(request:Request):
    return templates.TemplateResponse('nurregister.html',context={"request":request})

@app.get('/login')
def login(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse('login.html',context={"request":request})

@app.post('/doc_register')
def docregister(request:Request,db:Session=Depends(get_db),user_id:str=Form(...),name:str=Form(...),specialization:str=Form(...),email:str=Form(...),phone:str=Form(...),password:str=Form(...)):
    find = db.query(models.Doctor).filter(models.Doctor.doctor_id == id).first()
    if find is None:
        new_user = models.Doctor(doctor_id=user_id,doctor_name=name,doctor_specialization=specialization,doctor_email=email,doctor_phone=phone,doctor_password=password,status="Active",created_on=date)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return templates.TemplateResponse('login.html',context={"request":request,"message":"User created successfully"})
    else:
        return templates.TemplateResponse('docregister.html',context={"request":request,"message":"User already exists"})

@app.post('/nur_register')
def docregister(request:Request,db:Session=Depends(get_db),user_id:str=Form(...),name:str=Form(...),email:str=Form(...),phone:str=Form(...),password:str=Form(...)):
    find = db.query(models.Nurse).filter(models.Nurse.nurse_id == user_id).first()
    if find is None:
        new_user = models.Nurse(nurse_id=user_id,nurse_name=name,nurse_email=email,nurse_phone=phone,nurse_password=password,status="Active",created_on=date)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return templates.TemplateResponse('login.html',context={"request":request,"message":"User created successfully"})
    else:
        return templates.TemplateResponse('nurregister.html',context={"request":request,"message":"User already exists"})

@app.post('/authlogin')
def authlogin(request:Request,db:Session=Depends(get_db),id:str=Form(...),password:str=Form(...)):
    find = db.query(models.Doctor).filter(models.Doctor.doctor_id == id,models.Doctor.doctor_password==password).first()  
    if find:
        patientList = db.query(models.Patient).filter(models.Patient.status=="Active").all()
        return templates.TemplateResponse('dashboard.html',context={"request":request,"message":"Login Successful!","patientsData":patientList})   
    else:
        return templates.TemplateResponse('login.html',context={"request":request,"message":"Wrong ID or Password!"})    

@app.get('/dashboard')
def dashboard(request:Request,db:Session=Depends(get_db)):
    patientList = db.query(models.Patient).filter(models.Patient.status=="Active").all()
    print(patientList)
    return templates.TemplateResponse('dashboard.html',context={"request":request,"patientsData":patientList})   

@app.get('/addpatient')
def patient(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse('patient.html',context={"request":request})

@app.get('/settings')
def settings(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse('setting.html',context={"request":request})

@app.get('/about')
def about(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse('about.html',context={"request":request})

@app.post('/add_patient')
def addpatient(request:Request,db:Session=Depends(get_db),id:str=Form(...),name:str=Form(...),doc_id:str=Form(...),doc_name:str=Form(...),email:str=Form(...),phone:str=Form(...),address:str=Form(...),disease:str=Form(...),gender:str=Form(...),age:str=Form(...),cause:str=Form(...)):
    find = db.query(models.Patient).filter(models.Patient.patient_id == id,models.Patient.status=="Active").first()

    if find is None:
        new_user = models.Patient(patient_id=id,patient_name=name,patient_email=email,patient_phone=phone,patient_address=address,patient_disease=disease,patient_gender=gender,patient_age=age,patient_cause=cause,doctor_id=doc_id,doctor_name=doc_name,status="Active",created_on=date)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse("/dashboard",status_code=303)
    else:
        return templates.TemplateResponse('patient.html',context={"request":request,"message":"Patient already exists"})
    
@app.post('/editpatient')
def edit_patient(request:Request,db:Session=Depends(get_db),id:str=Form(...),name:str=Form(...),doc_id=Form(...),doc_name=Form(...),email:str=Form(...),phone:str=Form(...),address:str=Form(...),disease:str=Form(...),gender:str=Form(...),age:str=Form(...),cause:str=Form(...)):
    db.query(models.Patient).filter(models.Patient.patient_id==id).update({"patient_name":name,"doctor_id":doc_id,"doctor_name":doc_name,"patient_email":email,"patient_phone":phone,"patient_address":address,"patient_disease":disease,"patient_gender":gender,"patient_age":age,"patient_cause":cause})
    db.commit()
    return RedirectResponse("/dashboard",status_code=303)

@app.get('/delete_patient/{id}')
def deletepatient(id:str,request:Request,db:Session=Depends(get_db)):
    
    find = db.query(models.Patient).filter(models.Patient.patient_id == id).first()
    if find is not None:
        db.delete(find)
        db.commit()
        return templates.TemplateResponse('patient.html',context={"request":request})

@app.put('/put_data/{id}')
def update_form(id:str,request:Request,db:Session=Depends(get_db)):
    find = db.query(models.Patient).filter(models.Patient.patient_id == id,models.Patient.status=="Active").first()
    json_compatible_item_data = jsonable_encoder(find)
    return JSONResponse(content=json_compatible_item_data)

@app.get('/edit_patient/{id}')
def editpatient(id:str,request:Request,db:Session=Depends(get_db)):
    find = db.query(models.Patient).filter(models.Patient.patient_id == id,models.Patient.status=="Active").first()
    return templates.TemplateResponse('edit_patient.html',context={"request":request,"i":find})

@app.get('/view_patient/{id}')
def viewpatient(id:str,request:Request,db:Session=Depends(get_db)):
    find = db.query(models.Patient).filter(models.Patient.patient_id == id,models.Patient.status=="Active").first()
    return templates.TemplateResponse('view.html',context={"request":request,"i":find})