from typing import Optional
import uuid

import uvicorn
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from requests import RequestException
from starlette.requests import Request
from starlette.responses import JSONResponse

import request_body_mapping as req_mapping
from db import Session, models
from const import PREFIX_URL

import create_tables
create_tables.create() #This will create the tables automatically, first create database(create the schema within db if exists.)

app = FastAPI(debug=True)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# contactus
@app.post(PREFIX_URL + "/contactus")
async def create_contactus(request_context: Request, contactus: req_mapping.ContactUs, response: Response):
    session = None
    try:
        session = Session()
        name = contactus.name
        email = contactus.email
        phone = contactus.phone
        subject = contactus.subject
        message = contactus.message
        contact = models.ContactUs(name=name, email=email, phone=phone, subject=subject, message=message)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        response.status_code = status.HTTP_201_CREATED
        return {"Success"}
    except Exception as err:
        print("Exception:",err)
        return JSONResponse({"error_code": "ContactUsFailed",
                             "message": "Technical Error occurred while storing the contact us info"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/contactus/{id}")
async def get_contactus(request_context: Request, id):
    session = None
    try:
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id)
        result_set_count = result_set.count()
        result_set = result_set.all()
        if result_set_count > 0:
            return result_set
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:",err)
        return JSONResponse({"error_code": "ContactUsRetrievingApiFailure",
                             "message": "Technical Error occurred while retrieving the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/contactus")
async def get_contactus_all(request_context: Request, page: Optional[int] = 0, size: Optional[int] = 20):
    session = None
    try:
        if page != 0:
            # index starts from zero,req page is 1 means index 0.
            page = page - 1
        session = Session()
        result_set = session.query(models.ContactUs).order_by(models.ContactUs.id).offset(
            page * size).limit(size).all()
        return {"contactus": result_set}
    except Exception as err:
        print("Exception:",err)
        return JSONResponse({"error_code": "contactusRetrievingAllApiFailure",
                             "message": "Technical Error occurred while retrieving the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.put(PREFIX_URL + "/contactus/{id}")
async def update_contactus(request_context: Request, id, contact_update: req_mapping.UpdateStatus):
    session = None
    try:
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id)
        result_set_count = result_set.count()
        result_set = result_set.all()
        if result_set_count > 0:
            for contact in result_set:
                contact.is_active = contact_update.status
                session.commit()
                session.refresh(contact)
            return result_set
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:",err)
        return JSONResponse({"error_code": "ContactUsUpdationApiFailure",
                             "message": "Technical Error occurred while updating the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.delete(PREFIX_URL + "/contactus/{id}")
async def delete_contact(request_context: Request, id):
    session = None
    try:
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id)
        if result_set.count() > 0:
            result_set.delete()
            session.commit()
            return JSONResponse({"detail": "success"})
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        print("Exception:",err)
        return JSONResponse({"error_code": "ContactUsDeletionApiFailure",
                             "message": "Technical Error occurred while deleting the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200, log_level="debug")