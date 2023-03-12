# ____________________________________________________
# That project was created by Denys Atamanchuk
# That project cannot copy anyone
# That project was created only for portfolio
# ____________________________________________________


import os
from app import crete_app, db
from app.models import User, load_user
from flask_migrate import Migrate

app = crete_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
