from src.server import app
from src.config import APP_HOST, APP_PORT
import uvicorn


def main():
    uvicorn.run(app, port=APP_PORT, host=APP_HOST)


main()
