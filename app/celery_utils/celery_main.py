from celery import Celery
from celery.schedules import crontab

from db.models import Transaction, Message
from utils.send_mail import send_email
from config import MAIL_FROM

from datetime import date


app = Celery('budget')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour='1', minute=0),
        check_transaction_planned_date
    )


@app.task
async def check_transaction_planned_date():
    today = date.today()
    instances = await Transaction.filter(planned=today)
    for instance in instances:
        await instance.fetch_related('user')
        user = instance.user
        if instance.type:
            user.balance += instance.sum
        else:
            user.balance -= instance.sum
        await user.save()

        if user.fixed_balance and user.balance >= user.fixed_balance:
            await Message.create(receiver=user,
                                 text='You have reached your balance')

        if user.email:
            await send_email('BudgetApi', MAIL_FROM)
        else:
            text = f'Your transaction №{instance.number} has been added to balance'
            await Message.create(receiver=user,
                                 text=text)
