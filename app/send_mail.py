from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

import config

from db.models import User, Message


html = """
    <h1>Hello</h1>
    <p>You have reached your balance</p>
"""

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        html=html,
        subtype='html',
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_background(background_tasks: BackgroundTasks,
                          subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        html=html,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message
    )


async def send_message(user_id: int, text: str, background_tasks: BackgroundTasks):
    receiver = await User.get(id=user_id)

    async def create_message():
        await Message.create(receiver=receiver, text=text)

    background_tasks.add_task(
        create_message
    )
