from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='hhhh123'

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix=str('/'))
    app.register_blueprint(auth,url_prefix=str('/'))
    return app

