# -*- coding: utf-8 -*-
from apps import app
from flask_script import Manager, Command

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    manager = Manager(app)
    print app.url_map
    manager.run()


#  vim: set ts=8 sw=4 tw=0 fdm=manual et :
