# from app.piccolo.tables import User, OneTimeCode
import string
import random
from blacksheep.exceptions import HTTPException



class AuthService:
    pass
    # async def get_users(self):
    #     users = await User.select()
    #     return users
    #
    # async def get_codes(self):
    #     sms_codes = await OneTimeCode.select()
    #     return sms_codes
    #
    # async def create_code(self):
    #     # Админский метод
    #     def generate_code(length=8):
    #         allchars = string.ascii_letters + string.digits
    #         password = "".join(random.choice(allchars) for _ in range(length))
    #         return password
    #
    #     code = generate_code()
    #     await OneTimeCode(code=code).save()
    #     return code
    #
    # async def register_with_code(self, tg_id, code):
    #     # Проверка, что пользователь ещё не зарегистрирован
    #     if await self.check_user(tg_id):
    #         raise HTTPException(301, "User already exists")
    #
    #     code = await OneTimeCode.objects().where(OneTimeCode.code == code).first()
    #     if not code:
    #         raise HTTPException(401, "Code is invalid")
    #
    #     # Сохраняем пользователя и удаляем код, чтобы им не воспользовался другой
    #     await User(tg_id=tg_id, custom_settings={'ban': [], 'amount': {}}).save()
    #     await OneTimeCode.delete().where(OneTimeCode.code == code)
    #     return True
    #
    # async def check_user(self, tg_id):
    #     existing_user = await User.objects().where(User.tg_id == tg_id).first()
    #     return True if existing_user else False
