import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, content):
    """
    Gửi email text qua Gmail SMTP
    """

    # THAY BẰNG EMAIL & APP PASSWORD CỦA BẠN
    SMTP_EMAIL = "tuyen01632647361@gmail.com"
    SMTP_PASSWORD = "xdpzlplsopxzjyyd"

    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Lỗi gửi email:", e)
        raise
