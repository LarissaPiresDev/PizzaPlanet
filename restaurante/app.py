from flask_sqlalchemy import SQLAlchemy
from routes.cliente_routes import cliente_bp
from config import app, db

from routes.cliente_routes import cliente_bp
from routes.funcionario_routes import funcionario_bp
from routes.itemcardapio_routes import itemcardapio_bp
from routes.itempedido_routes import itempedido_bp
from routes.pedido_routes import pedido_bp



app.register_blueprint(cliente_bp)
app.register_blueprint(funcionario_bp)
app.register_blueprint(itemcardapio_bp)
app.register_blueprint(itempedido_bp)
app.register_blueprint(pedido_bp)

from schemas import ma  
ma.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG']) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
