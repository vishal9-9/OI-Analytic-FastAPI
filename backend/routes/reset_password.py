from fastapi import APIRouter, Depends
from database.schema import reset_pass
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import Users
from fastapi_mail import MessageSchema,ConnectionConfig,FastMail
from routes.password import password

router = APIRouter(
    tags = ["Reset Password"]
)

@router.post('/resetpassword')
async def reset_password(request: reset_pass, db: Session = Depends(get_db)):
    if request.email:
        exist = db.query(Users).filter(Users.email == request.email).first()
        if exist:
            email = request.email
            conf = ConnectionConfig(
                MAIL_USERNAME = "alexmercerazon@gmail.com",
                MAIL_PASSWORD = password,
                MAIL_FROM = "alexmercerazon@gmail.com",
                MAIL_PORT = 587,
                MAIL_SERVER = "smtp.gmail.com",
                MAIL_FROM_NAME="OI-Analytics",
                MAIL_TLS = True,
                MAIL_SSL = False,
                USE_CREDENTIALS = True,
                VALIDATE_CERTS = True
            )
            message = MessageSchema(
                subject = "Reset Password",
                recipients = email,
                body = 'New Password = 123456789', 
            )
            fm = FastMail(conf)
            await fm.send_message(message)
            return 'Mail Sent'
        else:
            return 'User Does Not Exist'
    else:
        return 'Please Enter Email'