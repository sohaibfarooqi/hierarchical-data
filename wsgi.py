from app import create_app
from config import ApplicationConfig

application = create_app(ApplicationConfig)
if __name__ == '__main__':
    app.run()
