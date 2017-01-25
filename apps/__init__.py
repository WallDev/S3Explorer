 # -*- coding: utf-8 -*-
from flask import Flask
import config


app = Flask(__name__)
app.config.from_object('config')

def enable_ext(app):
    from apps.utils.session import sess
    sess.init_app(app)

def enable_blueprints(app):
    from apps.frontend.views import front
    app.register_blueprint(front)

def enable_dev(app):
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)


enable_ext(app)
enable_blueprints(app)

if app.debug:
    enable_dev(app)

#  vim: set ts=8 sw=4 tw=0 fdm=manual et :
