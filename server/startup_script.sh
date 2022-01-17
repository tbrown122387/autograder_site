#!/bin/bash

RETRIES=5
until psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_ADDRESS:5432/$POSTGRES_DB -c "SELECT 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

python3 -m alembic upgrade head
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
