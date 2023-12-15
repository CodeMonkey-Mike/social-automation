# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from api import app
from flask_sqlalchemy import SQLAlchemy

# Disable modification tracking, as it can be resource-intensive
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.shell_context_processor
def make_shell_context():
    return {"app": app}


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0")
