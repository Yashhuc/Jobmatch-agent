import os
import base64
from typing import Tuple, Any, Optional
from src.config import settings

try:
    from postmarker.core import PostmarkClient
except Exception as e:
    PostmarkClient = None

POSTMARK_API_TOKEN = settings.POSTMARK_API_TOKEN.get_secret_value() if settings.POSTMARK_API_TOKEN else None
POSTMARK_SENDER_EMAIL = settings.POSTMARK_SENDER_EMAIL if settings.POSTMARK_SENDER_EMAIL else None

def send_application_email(
    to_email: str,
    subject: str,
    body_html: str,
    resume_path: Optional[str] = None
) -> Tuple[int, Any]:
    if PostmarkClient is None:
        raise RuntimeError("postmarker is not installed. pip install postmarker")
    if not POSTMARK_API_TOKEN or not POSTMARK_SENDER_EMAIL:
        raise RuntimeError("Missing Postmark config. Set POSTMARK_API_TOKEN and POSTMARK_SENDER_EMAIL in .env")

    client = PostmarkClient(server_token=POSTMARK_API_TOKEN)
    attachments = None
    if resume_path:
        with open(resume_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode("utf-8")
        attachments = [
            {
                "Name": os.path.basename(resume_path),
                "Content": encoded,
                "ContentType": "application/pdf"
            }
        ]
    response = client.emails.send(
        From=POSTMARK_SENDER_EMAIL,
        To=to_email,
        Subject=subject,
        HtmlBody=body_html,
        Attachments=attachments
    )
    return 200, response
