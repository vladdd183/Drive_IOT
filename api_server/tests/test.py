import pytest
import asyncio
from piccolo.engine.finder import engine_finder
from piccolo.table import create_db_tables, drop_db_tables

from app.piccoloModule.tables import Users, EventLog

@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='module', autouse=True)
async def setup_db():
    engine = engine_finder()
    # Create the tables in the database
    await create_db_tables(Users, EventLog, if_not_exists=True)
    yield
    # Drop the tables after testing is done
    await drop_db_tables(Users, EventLog)

@pytest.mark.asyncio
async def test_user_login_success():
    # Ensure the tables exist
    await Users.create_table(if_not_exists=True)

    # Create a sample user
    await Users(username="testuser", password="testpass").save()

    # Test successful login
    user = await Users.login(username="testuser", password="testpass")
    assert user is not False

@pytest.mark.asyncio
async def test_user_login_fail():
    # Test login with a non-existent user
    user = await Users.login(username="nonexistent", password="doesnotmatter")
    assert user is False

    # Create a sample user
    await Users(username="testuser", password="testpass").save()

    # Test login with incorrect password
    user = await Users.login(username="testuser", password="wrongpass")
    assert user is False
