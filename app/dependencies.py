from typing import Optional
from fastapi import Request


def get_user_fixed_balance(request: Request) -> Optional[float]:
    user = request.state.user
    if user.use_fixed_balance:
        return user.fixed_balance
