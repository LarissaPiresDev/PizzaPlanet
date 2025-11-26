from flask_marshmallow import Marshmallow
from config import db
from models import ItemCardapio, Pedido, ItemPedido

ma = Marshmallow()

class ItemCardapioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemCardapio
        sqla_session = db.session
        load_instance = True

    nome = ma.Str(required=True)
    preco = ma.Float(required=True)
    descricao = ma.Str(required=True)
    imagem = ma.Str(required=False)


class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        sqla_session = db.session
        load_instance = True

    nome = ma.Str(required=True)
    data = ma.Date(required=True)
    valor_total = ma.Float(dump_only=True)
    status = ma.Str(required=True)


class ItemPedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemPedido
        sqla_session = db.session
        load_instance = True

    pedido_id = ma.Int(required=True)
    item_cardapio_id = ma.Int(required=True)
    quantidade = ma.Int(required=True)
    subtotal = ma.Float(dump_only=True)
