from blacksheep import Application, Response, json, auth, file, StreamedContent, WebSocket, ws, WebSocketDisconnectError
from blacksheep.exceptions import HTTPException
from app.auth import Authenticated
from blacksheep.server.openapi.common import SecurityInfo
from app.piccoloModule.tables import Users as UserTB, EventLog as EventLogTable
from guardpost.authentication import User
from app.auth import Authenticated
import jwt
import os
from datetime import datetime, timedelta
from app.driverModule.driverService import DriveManager
import paho.mqtt.client as paho
import anyio

active_connections = []

async def send_message_to_all(message: str):
    for connection in active_connections:
        await connection.send_text(message)

def on_mqtt_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")
    message = msg.payload.decode()
    anyio.run(send_message_to_all, message)

# MQTT Settings
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = int(os.getenv('BROKER_PORT'))
TOPIC_PREFIX = "electrical_drive"


async def log_event(usr: str, drive: str, event_type: str, is_running: bool = False, speed: float = 0):
    await EventLogTable(
        username=usr,
        drive=drive,
        event_type=event_type,
        is_running=is_running,
        speed=speed,
    ).save()


def configure_routes(app: Application, docs):
    mqtt_client = paho.Client()
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.connect(BROKER_HOST, BROKER_PORT)
    mqtt_client.loop_start()
    mqtt_client.subscribe(f"{TOPIC_PREFIX}/#")



    @ws("/api/info")
    async def f21(ws: WebSocket):
        await ws.accept()
        active_connections.append(ws)
        try:
            while True:
                msg = await ws.receive_text()
                await ws.send_text(msg)
        except:
            pass
        finally:
            active_connections.remove(ws)
            return Response(200)

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.get("/api/drives")
    async def list_drives(user: User, drive_manager: DriveManager):
        uid = user.claims.get('uid')
        usr = await UserTB.select().where(UserTB.id == uid).first()
        return json(drive_manager.list_drives())

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.get("/api/drives/{drive_name}")
    async def get_drive(user: User, drive_manager: DriveManager, drive_name: str):
        uid = user.claims.get('uid')
        usr = await UserTB.select().where(UserTB.id == uid).first()
        drive = drive_manager.get_drive(drive_name)
        return json({
            "name": drive.name,
            "is_running": drive.is_running,
            "speed": drive.speed,
        })

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.post("/api/drives")
    async def create_drive(user: User, drive_manager: DriveManager, drive_name: str):
        uid = user.claims.get('uid')
        usr = await UserTB.select(UserTB.username).where(UserTB.id == uid).first()
        usr = usr['username']
        drive = drive_manager.create_drive(drive_name)
        await log_event(usr, drive_name, "CREATE")
        return json({
            "name": drive.name,
            "is_running": drive.is_running,
            "speed": drive.speed,
        }, status=201)

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.delete("/api/drives/{drive_name}")
    async def delete_drive(user: User, drive_manager: DriveManager, drive_name: str):
        uid = user.claims.get('uid')
        usr = await UserTB.select(UserTB.username).where(UserTB.id == uid).first()
        usr = usr['username']
        drive_manager.delete_drive(drive_name)
        await log_event(usr, drive_name, "DELETE")
        return json({"result": "Drive deleted"}, status=200)

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.post("/api/drives/{drive_name}/start")
    async def start_drive(user: User, drive_manager: DriveManager, drive_name: str, speed: float):
        uid = user.claims.get('uid')
        usr = await UserTB.select(UserTB.username).where(UserTB.id == uid).first()
        usr = usr['username']
        drive = await drive_manager.change_drive_state(drive_name, True, speed)
        await log_event(usr, drive_name, "START", True, speed)
        return json({
            "name": drive.name,
            "is_running": drive.is_running,
            "speed": drive.speed,
        })

    @docs(tags=['drivers'],
        security=[
            SecurityInfo("BearerAuth", []),
        ])
    @app.router.post("/api/drives/{drive_name}/stop")
    async def stop_drive(user: User, drive_manager: DriveManager, drive_name: str):
        uid = user.claims.get('uid')
        usr = await UserTB.select(UserTB.username).where(UserTB.id == uid).first()
        usr = usr['username']
        drive = await drive_manager.change_drive_state(drive_name, False)
        await log_event(usr, drive_name, "STOP", False)
        return json({
            "name": drive.name,
            "is_running": drive.is_running,
            "speed": drive.speed,
        })
