from notifico.models.bot import BotEvent
from notifico.models.user import User, Role, user_roles
from notifico.models.hook import Hook
from notifico.models.channel import Channel
from notifico.models.project import Project
from notifico.models.token import AuthToken

ALL_CORE_TABLES = [
    User.__table__,
    Role.__table__,
    user_roles,
    Hook.__table__,
    Channel.__table__,
    Project.__table__,
    BotEvent.__table__,
    AuthToken.__table__
]
