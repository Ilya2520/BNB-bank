from fastapi_users import FastAPIUsers

from src.configs.base_config import auth_backend
from src.controllers.manager import get_user_manager
from src.models.auth_models import user

fastapi_users = FastAPIUsers[user, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
