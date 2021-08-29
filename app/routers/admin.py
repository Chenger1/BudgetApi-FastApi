from fastapi import APIRouter, Depends, BackgroundTasks
from starlette.responses import FileResponse

from utils.authentication import get_current_user
from dependencies import check_is_admin

from utils.send_mail import send_email_background
from config import MAIL_FROM, MAIL_FROM_NAME
from db.crud import update_instance
from db.schema import UserAdmin, User_Schema
from logger import log


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


@router.patch('/change_admin_status', response_model=User_Schema)
async def change_user_admin_status(data: UserAdmin):
    log.info(f'User #{data.user_id} status has been changed')
    return await update_instance(data, data.user_id, 'User')


@router.get('/get_log_file')
async def get_log_file():
    return FileResponse('app.log', filename='app.log', media_type='text/plain')
