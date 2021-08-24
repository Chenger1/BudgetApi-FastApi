from .models import Transaction

from sqlalchemy.orm import Session


async def get_next_transaction_number(db: Session, user_id: int) -> int:
    last_instance = db.query(Transaction).filter(Transaction.user_id == user_id).first()
    if not last_instance:
        return 1
    return last_instance.number + 1
