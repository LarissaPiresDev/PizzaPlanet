from flask_restx import Namespace, Resource, fields
from flask import request
from models import ItemPedido, ItemCardapio
from config import db
from schemas import ItemPedidoSchema

itempedido_ns = Namespace("itempedido", description="Operações relacionadas aos itens do pedido")

item_schema = ItemPedidoSchema()
itens_schema = ItemPedidoSchema(many=True)

# Modelo de entrada
item_model = itempedido_ns.model("ItemPedido", {
    "pedido_id": fields.Integer(required=True, description="ID do pedido"),
    "item_cardapio_id": fields.Integer(required=True, description="ID do item do cardápio"),
    "quantidade": fields.Integer(required=True, description="Quantidade"),
})

# Modelo de saída
item_output_model = itempedido_ns.inherit("ItemPedidoOutput", item_model, {
    "id": fields.Integer(description="ID"),
    "subtotal": fields.Float(description="Subtotal"),
})


# =====================================
# LISTAR / CRIAR
# =====================================
@itempedido_ns.route("/")
class ItensPedidoResource(Resource):

    @itempedido_ns.marshal_list_with(item_output_model)
    def get(self):
        itens = ItemPedido.query.all()
        return itens_schema.dump(itens)

    @itempedido_ns.expect(item_model)
    @itempedido_ns.marshal_with(item_output_model, code=201)
    def post(self):
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
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")

        return item_schema.dump(item)

    @itempedido_ns.expect(item_model)
    @itempedido_ns.marshal_with(item_output_model)
    def put(self, id):
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")

        dados = request.get_json()

        if "pedido_id" in dados:
            item.pedido_id = dados["pedido_id"]

        if "item_cardapio_id" in dados:
            cardapio = ItemCardapio.query.get(dados["item_cardapio_id"])
            if not cardapio:
                itempedido_ns.abort(404, "Item do cardápio não encontrado")
            item.item_cardapio_id = dados["item_cardapio_id"]

        if "quantidade" in dados:
            item.quantidade = dados["quantidade"]

        cardapio = ItemCardapio.query.get(item.item_cardapio_id)
        item.subtotal = item.quantidade * cardapio.preco

        db.session.commit()
        return item

    @itempedido_ns.response(204, "Item do pedido deletado")
    def delete(self, id):
        item = ItemPedido.query.get(id)
        if not item:
            itempedido_ns.abort(404, "Item do pedido não encontrado")

        db.session.delete(item)
        db.session.commit()
        return "", 204
