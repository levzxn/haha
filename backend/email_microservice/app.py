from fastapi import FastAPI, BackgroundTasks, HTTPException
from email_microservice.schemas import EmailSchema
from email_microservice.templates import EmailTemplate
import aiosmtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()



app = FastAPI()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")


async def send_email(to_email: str, subject: str, body: str):
    try:
        message = EmailMessage()
        message["From"] = FROM_EMAIL
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body,subtype='HTML')
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=False,
            start_tls=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao enviar e-mail: {str(e)}")
    

@app.post('/email/send')
async def post_email(email:EmailSchema,background_tasks:BackgroundTasks):
    background_tasks.add_task(send_email,email.email,email.subject, EmailTemplate(email.keys))
    return {'message':'Email enviado com sucesso!!!'}

