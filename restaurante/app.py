from flask_sqlalchemy import SQLAlchemy
from config import app, db
from flask_cors import CORS   

from routes.itemcardapio_routes import itemcardapio_bp
from routes.itempedido_routes import itempedido_bp
from routes.pedido_routes import pedido_bp

# Habilitar CORS para toda a API
CORS(app, resources={r"/*": {"origins": "*"}}) 

app.register_blueprint(itemcardapio_bp)
app.register_blueprint(itempedido_bp)
app.register_blueprint(pedido_bp)

from schemas import ma  
ma.init_app(app)

from swagger.swagger_config import configure_swagger
configure_swagger(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])
