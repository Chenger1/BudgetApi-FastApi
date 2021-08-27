from tortoise import Model, fields

from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(unique=True, max_length=155)
    password = fields.CharField(max_length=255)

    class PydanticMeta:
        exclude = ['password']


class Category(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                   related_name='categories')


class Transaction(Model):
    id = fields.IntField(pk=True, index=True)
    number = fields.IntField()
    sum = fields.FloatField()
    type = fields.BooleanField(default=True)  #: True is "Income", False is "Outcome"

    created = fields.DatetimeField(auto_now_add=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                   related_name='transactions')
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField('models.Category',
                                                                           related_name='transactions')

    @classmethod
    async def get_transactions_by_period(cls, user_id: int, period: str, number: int = None,
                                         type: bool = None) -> list['Transaction']:
        current_data = datetime.now()
        instances = cls.filter(user__id=user_id)
        if type:
            instances = instances.filter(type=type)
        if period == 'day':
            if not number:
                number = current_data.day
            instances = instances.filter(created__day=number)
        elif period == 'month':
            if not number:
                number = current_data.month
            instances = instances.filter(created__month=number)
        else:
            if not number:
                number = current_data.year
            instances = instances.filter(created__year=number)
        return await instances

    @classmethod
    async def get_next_transaction_number(cls, user_id: int) -> int:
        last_instance = await cls.filter(user__id=user_id).order_by().limit(1).first()
        if not last_instance:
            return 1
        return last_instance.number + 1
