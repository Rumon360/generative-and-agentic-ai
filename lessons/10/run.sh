#!/bin/bash

case "$1" in
  dev)    fastapi dev main.py --port 8000 ;;
  index)  python src/index.py ;;
  worker) python -c "from src.client.rq_client import start_worker; start_worker()" ;;
  *)      echo "Usage: ./run.sh [dev|index|worker]" ;;
esac
