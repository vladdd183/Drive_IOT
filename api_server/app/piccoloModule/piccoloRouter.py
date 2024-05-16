from blacksheep import Application
from piccolo_admin.endpoints import create_admin
from app.piccoloModule.tables import Users, EventLog



def configure_routes(app: Application, docs):
    admin = create_admin([Users, EventLog])
    app.mount("/admin/", admin)


