
from app.core.config import settings
from fastapi_mail import MessageSchema


async def send_pw_reset_email(email: str, pw_reset_token: str, fm):
    template_body = {
        'email': email,
        'pw_reset_token': pw_reset_token,
        'frontend_url': settings.FRONTEND_URL
    }

    message = MessageSchema(
        subject="Autograder Bundler - Reset Password",
        recipients=[email],
        template_body=template_body,
    )

    await fm.send_message(message, template_name="pw_reset_template.html")
    return {"message": "email has been sent"}
