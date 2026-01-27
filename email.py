from fastapi import(BackgroundTasks, UploadFile, File, Form, HTTPException, Depends, status)
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from typing import List
config_credentials = dotenv_values(".env")
from .models import User
import jwt


conf = ConnectionConfig(
    MAIL_USERNAME= config_credentials["EMAIL"],
    MAIL_PASSWORD= config_credentials["PASS"],
    MAIL_FROM= config_credentials["EMAIL"],
    MAIL_PORT= 587,
    MAIL_SERVER= "smpt.gmail.com",
    MAIL_SSL_TLS=True,
    MAIL_SSL =False,
    USE_CREDENTIALS= True
)


class EmailSchema(BaseModel):
    email: List[EmailStr]
    
async def send_email(email: EmailSchema, instance: User):
    token_data = {
        "id" : instance.id,
        "username" : instance.username
    }
    
    token = jwt.encode(token_data, config_credentials["SECRET"])
    
    templete = f"""
            <!DOCTYPE html>
            <html>
                <head>
                
                </head>
                <body>
                    <div style = "display: flex; align-items: center; justify-content:
                    center; flex-direction: column">
                    
                    <h3> Account Verification </h3>
                    <br>
                    <p Thanks for choossing our shop</p>
                    <a style = "margin-top: lrem; padding: lrem; border-radius: 0.5rem;
                    font-size: lrem; text-decorations: none;
                    background; #0275d8; color: white;" href = "http://127.0.0.1:8000/verification/?token={token}">
                    </a>
                    
                    <p> Please Ignore if you are did not register MirzaShop. Thanks</p>
                    </div>
                </body>
            </html>
    """
