from flask_marshmallow import Marshmallow
from config import db
from models import Cliente, Funcionario, ItemCardapio, Pedido, ItemPedido

ma = Marshmallow()

# -------------------
# Schema Cliente
# -------------------
class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        sqla_session = db.session
        load_instance = True

    nome = ma.Str(required=True)
    cpf = ma.Str(required=True)
    numero_telefone = ma.Str(required=True)
    endereco = ma.Str(required=True)


# -------------------
# Schema Funcionario
# -------------------
class FuncionarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Funcionario
        sqla_session = db.session
        load_instance = True

    nome = ma.Str(required=True)
    cpf = ma.Str(required=True)
    senha = ma.Str(required=True)


# -------------------
# Schema ItemCardapio
# -------------------
class ItemCardapioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemCardapio
        sqla_session = db.session
        load_instance = True

    nome = ma.Str(required=True)
    preco = ma.Float(required=True)
    descricao = ma.Str(required=True)


# -------------------
# Schema Pedido
# -------------------
class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        sqla_session = db.session
        load_instance = True

    cliente_id = ma.Int(required=True)
    funcionario_id = ma.Int(required=True)
    valor_total = ma.Float(required=True)
    data = ma.Date(required=True)


# -------------------
# Schema ItemPedido
# -------------------
class ItemPedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemPedido
        sqla_session = db.session
        load_instance = True

    pedido_id = ma.Int(required=True)
    quantidade = ma.Int(required=True)
    subtotal = ma.Float(required=True)
