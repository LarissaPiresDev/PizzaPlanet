from config import db
from datetime import datetime

class ItemCardapio(db.Model):
    __tablename__ = "item_cardapio"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.String(300), nullable=True)



class Pedido(db.Model):
    __tablename__ = "pedido"

    id_pedido = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    data = db.Column(db.Date, default=datetime.utcnow)
    valor_total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="em_execucao")

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, default=0)

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    item_cardapio_id = db.Column(db.Integer, db.ForeignKey('item_cardapio.id'), nullable=False)

    item_cardapio = db.relationship("ItemCardapio")

    def calcular_subtotal(self):
        if self.item_cardapio and self.quantidade:
            self.subtotal = self.quantidade * self.item_cardapio.preco
