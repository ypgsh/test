
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.extension import db
from app.main import create_app

app=create_app('product')
manager = Manager(app)
migrate = Migrate(app, db, directory='data/migrations', compare_type=True)


manager.add_command('db', MigrateCommand)



if __name__=='__main__':
    manager.run()
