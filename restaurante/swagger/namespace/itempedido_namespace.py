from flask_restx import Namespace, Resource, fields
from flask import request
from models import ItemPedido, ItemCardapio
from config import db
from schemas import ItemPedidoSchema

itempedido_ns = Namespace("itempedido", description="Operações relacionadas aos itens do pedido")

item_schema = ItemPedidoSchema()
itens_schema = ItemPedidoSchema(many=True)

# Modelos para documentação
item_model = itempedido_ns.model("ItemPedido", {
    "pedido_id": fields.Integer(required=True, description="ID do pedido"),
    "item_cardapio_id": fields.Integer(required=True, description="ID do item do cardápio"),
    "quantidade": fields.Integer(required=True, description="Quantidade do item no pedido"),
})

item_output_model = itempedido_ns.inherit("ItemPedidoOutput", item_model, {
    "id": fields.Integer(description="ID do item do pedido"),
    "subtotal": fields.Float(description="Subtotal calculado automaticamente"),
})

# Rotas do namespace
@itempedido_ns.route("/")
class ItensPedidoResource(Resource):
    @itempedido_ns.marshal_list_with(item_output_model)
    def get(self):
        """Lista todos os itens do pedido"""
        itens = ItemPedido.query.all()
        return itens_schema.dump(itens)

    @itempedido_ns.expect(item_model)
    @itempedido_ns.marshal_with(item_output_model, code=201)
    def post(self):
        """Cria um novo item do pedido"""
        dados = request.get_json()
        try:
            item = item_schema.load(dados, session=db.session)
        except Exception as e:
            itempedido_ns.abort(400, f"Erro ao criar item do pedido: {e}")

        cardapio = ItemCardapio.query.get(item.item_cardapio_id)
        if not cardapio:
            itempedido_ns.abort(404, "Item do cardápio não encontrado")

        item.subtotal = item.quantidade * cardapio.preco
        db.session.add(item)
        db.session.commit()
        return item, 201

@itempedido_ns.route("/<int:id>")
@itempedido_ns.response(404, "Item do pedido não encontrado")
class ItemPedidoIdResource(Resource):
    @itempedido_ns.marshal_with(item_output_model)
    def get(self, id):
        """Obtém um item do pedido pelo ID"""
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")
        return item_schema.dump(item)

    @itempedido_ns.expect(item_model)
    def put(self, id):
        """Atualiza um item do pedido pelo ID"""
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")

        dados = request.get_json()
        for campo, valor in dados.items():
            setattr(item, campo, valor)

        cardapio = ItemCardapio.query.get(item.item_cardapio_id)
        if cardapio:
            item.subtotal = item.quantidade * cardapio.preco

        db.session.commit()
        return item_schema.dump(item), 200

    @itempedido_ns.response(204, "Item do pedido deletado com sucesso")
    def delete(self, id):
        """Deleta um item do pedido pelo ID"""
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")

        db.session.delete(item)
        db.session.commit()
        return "", 204
