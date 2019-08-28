from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from core.config import Config
 

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
admin = Admin()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from core.users.routes import users
    from core.posts.routes import posts
    from core.main.routes import main
    from core.finance.routes import finance
    from core.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(finance)
    app.register_blueprint(errors)

    # flask admin setup
    from core.models import User, Post, Transaction, MyAdminIndexView, MyModelView, WebsiteReturn
    admin.init_app(app, index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(WebsiteReturn(name='Website', endpoint='website'))

    # whoosh search function
    import flask_whooshalchemy
    flask_whooshalchemy.whoosh_index(app, Post)

    return app