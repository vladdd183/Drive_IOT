from piccolo.columns import Varchar, Secret, Timestamp, Boolean, Float
from piccolo.columns.defaults import TimestampNow
from piccolo.table import Table
import datetime


class Users(Table):
    username = Varchar(unique=True, required=True)
    password = Secret()

    @classmethod
    async def login(cls, username: str, password: str) -> bool:
        user = await cls.objects().where(cls.username == username).first()
        if user is None:
            return False

        if password == user.password:
            return user
        else:
            return False


class EventLog(Table):
    username = Varchar(length=255, null=False)
    drive = Varchar(length=255, null=False)
    event_type = Varchar(length=255, null=False)
    timestamp = Timestamp(default=TimestampNow())
    is_running = Boolean()
    speed = Float()
