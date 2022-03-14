#!/bin/sh
echo "Mongo not yet run..."
while ! nc -z $MONGODB_HOST $MONGO_PORT; do
  sleep 0.1
done
echo "Mongo did run."
python main.py
exec "$@"