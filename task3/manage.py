from flask_script import Manager

from .app import create_app


app = create_app("task3")
manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=app.debug, host=app.config.get('HOST'))


if __name__ == "__main__":
    manager.run()
