"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""
from typing import Tuple
from rodi import Container
from app.settings import Settings
from app.driverModule.driverService import DriveManager
"""
Метод add_instance используется для регистрации экземпляра объекта в контейнере. Этот метод принимает один аргумент - экземпляр объекта, который нужно зарегистрировать.

Метод add_transient используется для регистрации сервиса как временного. Это означает, что каждый раз, когда сервис запрашивается, будет создаваться новый экземпляр. Этот метод принимает один аргумент - класс сервиса, который нужно зарегистрировать.

Кроме того, есть метод add_singleton, который используется для регистрации сервиса как одиночки. Это означает, что будет создан только один экземпляр сервиса, который будет использоваться повторно на протяжении всего времени жизни контейнера.
"""

def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    driver_manager = DriveManager()
    container.add_instance(driver_manager)

    return container, settings
