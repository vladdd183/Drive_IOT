from blacksheep import Application, Response, json, auth, file, StreamedContent
from blacksheep.exceptions import HTTPException
from app.auth import Authenticated
from blacksheep.server.openapi.common import SecurityInfo
from app.piccoloModule.tables import Users as UserTB
from guardpost.authentication import User
from app.auth import Authenticated
import jwt
import os
from datetime import datetime, timedelta


def get_jwt_token(user_id):
    jwt_token = jwt.encode(
        {
            "uid": user_id,
            "exp": datetime.utcnow() + timedelta(days=30), # Время действия токена, после которого происходит разлогин
        },
        os.environ.get('jwt-secret', 'secret'),
        algorithm="HS256",
    )
    return jwt_token

def configure_routes(app: Application, docs):
    @docs(tags=['auth'])
    @app.router.post("/api/auth/login")
    async def login(username: str, password: str):
        user = await UserTB.login(username, password)
        if not user:
            raise HTTPException(404, 'Не верный логин или пароль')
        token = get_jwt_token(user.id)
        return token

    @docs(tags=['auth'],
          security=[
            SecurityInfo("apiKeyAuth", []),
        ])
    @app.router.post("/api/auth/register")
    async def register(username: str, password: str):
        if await UserTB.select().where(UserTB.username == username):
            raise HTTPException(401, 'Пользователь с таким именем уже существует')
        user = UserTB(username=username, password=password)
        await user.save()
        token = get_jwt_token(user.id)

        return token

    @docs(tags=['auth'],
        security=[
            SecurityInfo("BearerAuth", []),
        ]
    )
    @app.router.get("/api/auth/test")
    @auth(Authenticated)
    async def test_auth(user: User):
        uid = user.claims.get('uid')
        usr = await UserTB.select().where(UserTB.id == uid).first()
        del usr['id'], usr['password']
        return json(usr)




