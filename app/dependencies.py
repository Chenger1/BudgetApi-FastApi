from typing import Optional
from fastapi import Request, HTTPException


def get_user_fixed_balance(request: Request) -> Optional[float]:
    user = request.state.user
    if user.use_fixed_balance:
        return user.fixed_balance


def check_is_admin(request: Request):
    if not request.state.user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='User is not an admin'
        )
