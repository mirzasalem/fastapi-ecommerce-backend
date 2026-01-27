from fastapi import(BackgroundTasks, UploadFile, File, Form, HTTPException, Depends, status)
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from typing import List
config_credentials = dotenv_values(".env")
from models import User
import jwt


conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",

    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,

    USE_CREDENTIALS=True
)


class EmailSchema(BaseModel):
    email: List[EmailStr]
    
async def send_email(email: EmailSchema, instance: User):
    token_data = {
        "id" : instance.id,
        "username" : instance.username
    }
    
    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm='HS256')
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <div style="display:flex;align-items:center;justify-content:center;flex-direction:column">
    
    <h3>Account Verification</h3>
    
    <p>Thanks for choosing our shop.</p>
    
    <a href="http://127.0.0.1:8000/verification/?token={token}"
       style="margin-top:1rem;padding:1rem;border-radius:0.5rem;
       font-size:1rem;text-decoration:none;
       background:#0275d8;color:white;">
       Verify Account
    </a>
    
    <p>If you did not register at MirzaShop, please ignore this email.</p>
    
    </div>
    </body>
    </html>
    """
    

    message = MessageSchema(
        subject = "MirzaShop Account Verification",
        recipients = email,
        body = template,
        subtype = "html")
    fm = FastMail(conf)
    await fm.send_message(message=message)