
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import smtplib
import random
from email.mime.text import MIMEText
from email_verification import SENDER_EMAIL, APP_PASSWORD

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
verification_codes = {}
class EmailRequest(BaseModel):
    email: EmailStr

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str


@app.post("/send-code")
def send_code(data: EmailRequest):
    code = str(random.randint(100000, 999999))
    verification_codes[data.email] = code

    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = data.email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, data.email, msg.as_string())
        server.quit()
        return {"message": "Verification code sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")


@app.post("/verify-code")
def verify_code(data: VerifyRequest):
    saved_code = verification_codes.get(data.email)

    if not saved_code:
        raise HTTPException(status_code=404, detail="No code found for this email")

    if saved_code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    del verification_codes[data.email]
    return {"message": "Email verified successfully"}