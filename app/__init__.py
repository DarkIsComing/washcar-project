from flask import Flask 
from flask_apscheduler import APScheduler

scheduler=APScheduler()

def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    scheduler.init_app(app)
    scheduler.start()
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint)
    return app