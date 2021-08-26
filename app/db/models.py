from tortoise import Model, fields


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

    created = fields.DatetimeField(auto_now_add=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                   related_name='transactions')
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField('models.Category',
                                                                           related_name='transactions')

    @classmethod
    async def get_next_transaction_number(cls, user_id: int) -> int:
        last_instance = await cls.filter(user__id=user_id).order_by().limit(1).first()
        if not last_instance:
            return 1
        return last_instance.number + 1
