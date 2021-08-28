from typing import Optional

from tortoise import Model, fields

from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(unique=True, max_length=155)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, null=True)

    balance = fields.FloatField(default=0)

    use_fixed_balance = fields.BooleanField(default=False)
    fixed_balance = fields.FloatField(default=0)

    class PydanticMeta:
        exclude = ['password']


class Message(Model):
    id = fields.IntField(pk=True, index=True)
    receiver: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='messages',
                                                                       on_delete=fields.CASCADE)
    text = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def get_messages(cls, user_id: int) -> list['Message']:
        return await cls.filter(receiver__id=user_id)


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
    async def get_transaction_by_type(cls, user_id: int, type: bool) -> list['Transaction']:
        return await cls.filter(user__id=user_id, type=type)

    @classmethod
    async def get_transactions_by_category(cls, user_id: int, category_id: int,
                                           type: Optional[bool] = None) -> list['Transaction']:
        if isinstance(type, bool):
            return await cls.filter(user__id=user_id, category__id=category_id, type=type)
        return await cls.filter(user__id=user_id, category__id=category_id)

    @classmethod
    async def get_next_transaction_number(cls, user_id: int) -> int:
        last_instance = await cls.filter(user__id=user_id).order_by('-id').limit(1).first()
        if not last_instance:
            return 1
        return last_instance.number + 1

    def category_id(self) -> int:
        return self.category.id

    class PydanticMeta:
        computed = ('category_id', )
