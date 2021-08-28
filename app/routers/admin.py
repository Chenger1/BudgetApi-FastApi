from fastapi import APIRouter, Depends, BackgroundTasks

from authentication import get_current_user
from dependencies import check_is_admin

from send_mail import send_email_background
from config import MAIL_FROM, MAIL_FROM_NAME


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_current_user),
                  Depends(check_is_admin)]
)


@router.get('/panel')
async def admin_panel():
    return {'admin-panel': 'You have access to this page'}


@router.get('/broadcast')
async def broadcast_mailing(text: str, background_task: BackgroundTasks):
    await send_email_background(background_task, MAIL_FROM, MAIL_FROM_NAME, text)
