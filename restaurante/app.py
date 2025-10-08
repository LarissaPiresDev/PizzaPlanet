from flask_sqlalchemy import SQLAlchemy
from routes.cliente_routes import cliente_bp
from config import app,db



db = SQLAlchemy(app)




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG']) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
