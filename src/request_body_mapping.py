from typing import Any
from typing import Optional

from pydantic import BaseModel

class ContactUs(BaseModel):
    name: str
    email: str
    phone: str
    subject: str
    message: str

class UpdateStatus(BaseModel):
    status: bool
