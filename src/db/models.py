import email
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean

from db import base


class ContactUs(base):
    __tablename__ = 'contactus'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    subject = Column(String)
    message = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(String)
    modified_by = Column(String)
    created_date = Column(DateTime(timezone=False), server_default=func.now())
    modified_date = Column(DateTime(timezone=False), onupdate=func.now())

    def __repr__(self):
        return (
            f"<ContactUs(id = {self.id},name = {self.name}, "
            f"email = {self.email},phone = {self.phone},"
            f"subject = {self.subject},message = {self.message},is_active = {self.is_active},"
            f"created_by = {self.created_by},modified_by = {self.modified_by},"
            f"created_date = {self.created_date},modified_date = {self.modified_date})>")