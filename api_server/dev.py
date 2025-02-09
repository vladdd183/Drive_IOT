"""
Runs the application for local development. This file should not be used to start the
application for production.

Refer to https://www.uvicorn.org/deployment/ for production deployments.
"""
import os

import uvicorn
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
try:
    import uvloop
except ModuleNotFoundError:
    pass
else:
    uvloop.install()

if __name__ == "__main__":
    os.environ["APP_ENV"] = "dev"
    port = int(os.environ.get("APP_PORT", 44777))

    os.environ['POSTGRES_DB'] = 'ai_db'
    os.environ['POSTGRES_USER'] = 'postgres'
    os.environ['POSTGRES_PASSWORD'] = 'postgres'
    os.environ['POSTGRES_HOST'] = 'localhost'
    os.environ['POSTGRES_PORT'] = '5432'
    os.environ['ADMIN_PASSWORD'] = 'admin123'

    os.environ['BROKER_HOST'] = 'localhost'
    os.environ['BROKER_PORT'] = '1883'

    console = Console()
    console.rule("[bold yellow]Running for local development", align="left")
    console.print(f"[bold yellow]Visit http://localhost:{port}/docs")

    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=port,
        lifespan="on",
        log_level="info",
        reload=True,
    )
