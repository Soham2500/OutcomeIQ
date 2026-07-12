"""SMTP email helpers for transactional auth messages."""

from email.message import EmailMessage
import smtplib

from app.core.config import get_settings


def send_registration_otp_email(email: str, otp: str) -> None:
    """Send a registration OTP through configured SMTP settings."""

    settings = get_settings()
    missing = [
        name
        for name, value in {
            "SMTP_HOST": settings.SMTP_HOST,
            "SMTP_USER": settings.SMTP_USER,
            "SMTP_PASSWORD": settings.SMTP_PASSWORD,
            "MAIL_FROM": settings.MAIL_FROM,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(
            "SMTP settings are not configured: " + ", ".join(missing)
        )

    message = EmailMessage()
    from_name = settings.MAIL_FROM_NAME or "OutcomeIQ"
    message["From"] = f"{from_name} <{settings.MAIL_FROM}>"
    message["To"] = email
    message["Subject"] = "Your OutcomeIQ registration OTP"
    message.set_content(
        "\n".join(
            [
                "Welcome to OutcomeIQ.",
                "",
                f"Your registration OTP is: {otp}",
                f"This OTP expires in {settings.OTP_EXPIRE_MINUTES} minutes.",
                "",
                "If you did not request this, you can ignore this email.",
            ]
        )
    )

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as exc:
        raise RuntimeError("Could not send OTP email.") from exc
