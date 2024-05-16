from guardpost.common import AuthenticatedRequirement
from blacksheep.server.authorization import Policy
from blacksheep import Application, Request
import jwt
from guardpost.authentication import AuthenticationHandler, Identity
from jwt import ExpiredSignatureError
import os

Authenticated = "authenticated"


class AuthHandler(AuthenticationHandler):
    def __init__(self, app: Application) -> None:
        super().__init__()
        self.app: Application = app

    async def authenticate(self, context: Request) -> Identity | None:
        if not context:
            return None

        token = context.get_first_header(b"Authorization")

        if not token:
            return None

        try:
            token = token.decode().split()[-1]
            user = jwt.decode(
                token,
                os.environ.get('jwt-secret', 'secret'),
                algorithms=[
                    "HS256",
                ],
            )
        except ExpiredSignatureError:
            print("Token has expired")
            return None
        except Exception as e:
            print(e)
            return None

        context.identity = Identity(user, "MOCK")

        return context.identity


def configure_authentication(app: Application):
    app.use_authentication().add(AuthHandler(app))
    app.use_authorization().add(Policy(Authenticated, AuthenticatedRequirement()))
