from .app.app import create_app
from .config import ApplicationConfig
from functools import wraps

app = create_app(ApplicationConfig)
if __name__ == '__main__':
    app.run()
