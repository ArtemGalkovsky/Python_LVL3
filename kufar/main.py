from tg import run_bot
from asyncio import run as asyncio_run
from flask_site import app
from threading import Thread

if __name__ == '__main__':
    Thread(target=app.run, daemon=True).start()

    asyncio_run(run_bot())
