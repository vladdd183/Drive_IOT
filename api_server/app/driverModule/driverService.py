import string
import json
import random
from typing import Dict, List

import anyio
from blacksheep.exceptions import HTTPException
import paho.mqtt.client as paho
from rich.traceback import install
from rich.pretty import pprint as print
import os

install(show_locals=True)

# MQTT Settings
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = int(os.getenv('BROKER_PORT'))
TOPIC_PREFIX = "electrical_drive"


class ElectricalDrive:
    def __init__(self, drive_name):
        self.name = drive_name
        self.topic = f"{TOPIC_PREFIX}/{drive_name}"
        self.is_running = False
        self.speed = 0.0

        self.client = paho.Client()
        self.client.connect(BROKER_HOST, BROKER_PORT)
        self.client.loop_start()

        self.publish_state(initial=True)

    async def update_speed(self, target_speed, duration=1.0):
        steps = int(duration / 0.1)
        speed_step = (target_speed - self.speed) / steps
        current_speed = self.speed
        for _ in range(steps):
            current_speed += speed_step
            self.speed = round(current_speed, 6)
            self.publish_state()
            await anyio.sleep(0.1)
        self.speed = target_speed
        self.publish_state()

    def publish_state(self, initial=False, deleted=False):
        payload = {
            "name": self.name,
            "is_running": self.is_running,
            "speed": self.speed,
        }
        if initial:
            payload['message'] = 'Drive created'
        elif deleted:
            payload['message'] = 'Drive deleted'
        else:
            if not self.is_running and self.speed == 0.0:
                payload['message'] = 'Drive stopped and switched off'
            elif self.is_running:
                payload['message'] = 'Drive running'

        payload_b = json.dumps(payload, indent=2).encode('utf-8')
        self.client.publish(self.topic, payload_b, qos=1)

    async def stop(self):
        await self.update_speed(0.0)
        self.is_running = False
        self.publish_state()


class DriveManager:
    def __init__(self):
        self.drives: Dict[str, ElectricalDrive] = {}

    def create_drive(self, drive_name: str) -> ElectricalDrive:
        if drive_name in self.drives:
            raise HTTPException(400, f"Drive {drive_name} already exists")
        drive = ElectricalDrive(drive_name)
        self.drives[drive_name] = drive
        return drive

    def delete_drive(self, drive_name: str) -> bool:
        if drive_name not in self.drives:
            raise HTTPException(404, f"Drive {drive_name} not found")
        drive = self.drives[drive_name]
        drive.publish_state(deleted=True)
        del self.drives[drive_name]
        return True

    async def change_drive_state(self, drive_name: str, is_running: bool, speed: float = None):
        if drive_name not in self.drives:
            raise HTTPException(404, f"Drive {drive_name} not found")
        drive = self.drives[drive_name]
        if is_running:
            drive.is_running = True
            drive.publish_state()
            if speed is not None:
                await drive.update_speed(speed if is_running else 0.0)
        else:
            await drive.stop()

        return drive

    def get_drive(self, drive_name: str) -> ElectricalDrive:
        if drive_name not in self.drives:
            raise HTTPException(404, f"Drive {drive_name} not found")
        return self.drives[drive_name]

    def list_drives(self) -> List[str]:
        return list(self.drives.keys())
