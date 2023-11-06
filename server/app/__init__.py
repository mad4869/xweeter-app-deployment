from flask import Flask
from flask_admin.contrib.sqla import ModelView
import schedule
import time
import threading

from .extensions import *
from .models import *
from .routes import routes
from .config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(routes)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    jwt_manager.init_app(app)
    socket.init_app(app)
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session, name="Users"))
    admin.add_view(ModelView(Xweet, db.session, name="Xweets"))
    admin.add_view(ModelView(Rexweet, db.session, name="Rexweets"))
    admin.add_view(ModelView(Like, db.session, name="Likes"))
    admin.add_view(ModelView(Reply, db.session, name="Replies"))
    admin.add_view(ModelView(Hashtag, db.session, name="Hashtags"))

    def scheduled_task():
        with app.app_context():
            from .utils.update_file import update_file_url

            update_file_url()

    schedule.every(60).seconds.do(scheduled_task)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(2)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    return app


app = create_app()
