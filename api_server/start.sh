#!/bin/bash

piccolo migrations new home --auto --auto_input='y'
piccolo migrations forwards session_auth
piccolo migrations forwards user
piccolo migrations forward all
piccolo user create --username="admin" --email="admin@admin.com" --password="${ADMIN_PASSWORD}" --is_admin=True --is_superuser=True --is_active=True
piccolo migrations check
# start app
exec uvicorn "app.main:app" --host "0.0.0.0" --port "8000"
