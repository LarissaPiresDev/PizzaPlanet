from flask_restx import Namespace, Resource, fields
from flask import request
from models import Pedido, ItemPedido, ItemCardapio
from config import db
from datetime import datetime

pedido_ns = Namespace("pedidos", description="Operações relacionadas aos pedidos")

# -------------------------------
# MODELOS SWAGGER
# -------------------------------

item_pedido_model = pedido_ns.model("ItemPedidoInput", {
    "item_cardapio_id": fields.Integer(required=True, description="ID do item do cardápio"),
    "quantidade": fields.Integer(required=True, description="Quantidade do item")
})

pedido_model = pedido_ns.model("PedidoInput", {
    "data": fields.String(required=False, description="Data do pedido (YYYY-MM-DD)"),
    "valor_total": fields.Float(required=False, description="Valor total (opcional)"),
    "itens": fields.List(fields.Nested(item_pedido_model), required=False)
})

item_pedido_output = pedido_ns.model("ItemPedidoOutput", {
    "id": fields.Integer(description="ID do item"),
    "item_cardapio_id": fields.Integer(),
    "quantidade": fields.Integer(),
    "subtotal": fields.Float()
})

pedido_output = pedido_ns.model("PedidoOutput", {
    "id": fields.Integer(description="ID do pedido"),
    "data": fields.String(),
    "valor_total": fields.Float(),
    "itens": fields.List(fields.Nested(item_pedido_output))
})

pedido_created = pedido_ns.model("PedidoCreated", {
    "mensagem": fields.String(),
    "id": fields.Integer()
})


# ============================================
# GET /pedidos  — Listar todos
# ============================================
@pedido_ns.route("/")
class PedidosResource(Resource):

    @pedido_ns.marshal_list_with(pedido_output)
    def get(self):
        pedidos = Pedido.query.all()
        resultado = []

        for p in pedidos:
            resultado.append({
                "id": p.id_pedido,
                "data": p.data.strftime("%Y-%m-%d") if p.data else None,
                "valor_total": p.valor_total,
                "itens": [
                    {
                        "id": item.id,
                        "item_cardapio_id": item.item_cardapio_id,
                        "quantidade": item.quantidade,
                        "subtotal": item.subtotal
                    }
                    for item in p.itens
                ]
            })

        return resultado, 200

    # ============================================
    # POST /pedidos — Criar pedido
    # ============================================
    @pedido_ns.expect(pedido_model)
    @pedido_ns.marshal_with(pedido_created, code=201)
    def post(self):
        dados = request.get_json()

        data_str = dados.get("data")
        valor_total = dados.get("valor_total", 0)
        itens = dados.get("itens", [])

        # valida data
        try:
            data_formatada = (
                datetime.strptime(data_str, "%Y-%m-%d").date()
                if data_str else None
            )
        except:
            pedido_ns.abort(400, "Formato de data inválido. Use YYYY-MM-DD")

        pedido = Pedido(
            data=data_formatada,
            valor_total=valor_total
        )

        db.session.add(pedido)
        db.session.commit()  # gera ID

        # cria itens do pedido
        for item in itens:
            item_cardapio_id = item.get("item_cardapio_id")
            quantidade = item.get("quantidade")

            cardapio_item = ItemCardapio.query.get(item_cardapio_id)
            if not cardapio_item:
                pedido_ns.abort(404, f"ItemCardapio {item_cardapio_id} não encontrado")

            novo_item = ItemPedido(
                pedido_id=pedido.id_pedido,
                item_cardapio_id=item_cardapio_id,
                quantidade=quantidade,
                subtotal=cardapio_item.preco * quantidade
            )
            db.session.add(novo_item)

        db.session.commit()

        return {"mensagem": "Pedido criado com sucesso", "id": pedido.id_pedido}, 201


# ============================================
# GET /pedidos/<id> | PUT | DELETE
# ============================================
@pedido_ns.route("/<int:id>")
@pedido_ns.response(404, "Pedido não encontrado")
class PedidoIdResource(Resource):

    @pedido_ns.marshal_with(pedido_output)
    def get(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            pedido_ns.abort(404, "Pedido não encontrado")

        return {
            "id": pedido.id_pedido,
            "data": pedido.data.strftime("%Y-%m-%d") if pedido.data else None,
            "valor_total": pedido.valor_total,
            "itens": [
                {
                    "id": item.id,
                    "item_cardapio_id": item.item_cardapio_id,
                    "quantidade": item.quantidade,
                    "subtotal": item.subtotal
                }
                for item in pedido.itens
            ]
        }

    # ---------------------------------------
    # Atualizar somente dados do pedido
    # ---------------------------------------
    @pedido_ns.expect(pedido_model)
    def put(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            pedido_ns.abort(404, "Pedido não encontrado")

        dados = request.get_json()

        if "data" in dados:
            try:
                pedido.data = datetime.strptime(dados["data"], "%Y-%m-%d").date()
            except:
                pedido_ns.abort(400, "Formato de data inválido")

        if "valor_total" in dados:
            pedido.valor_total = dados["valor_total"]

        db.session.commit()

        return {"mensagem": "Pedido atualizado com sucesso"}, 200

    # ---------------------------------------
    # DELETE /pedidos/<id>
    # ---------------------------------------
    @pedido_ns.response(200, "Pedido deletado com sucesso")
    def delete(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            pedido_ns.abort(404, "Pedido não encontrado")

        # deletar itens primeiro
        for item in pedido.itens:
            db.session.delete(item)

        db.session.delete(pedido)
        db.session.commit()

        return {
            "mensagem": "Pedido deletado com sucesso",
            "id": id
        }, 200
