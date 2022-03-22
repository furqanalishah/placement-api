import os

from flask_migrate import Migrate

from placement.web import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
from placement.models import *  # noqa

if __name__ == '__main__':
    app.run()
