from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    numero_telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    senha = db.Column(db.String(100))

    pedidos = db.relationship("Pedido", backref="funcionario", lazy=True)

class ItemCardapio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    preco = db.Column(db.Float)
    descricao = db.Column(db.String(200))

class Pedido(db.Model):
    id_pedido = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    valor_total = db.Column(db.Float)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'))

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
