from flask import Blueprint, request, jsonify
from models import Pedido, ItemPedido, ItemCardapio
from config import db
from datetime import datetime

itempedido_bp = Blueprint('itempedido_bp', __name__)

# -------------------------
# LISTAR TODOS OS ITENS
# -------------------------
@itempedido_bp.route('/itempedido', methods=['GET'])
def listar_itens():
    itens = ItemPedido.query.all()
    return jsonify([
        {
            "id": i.id,
            "pedido_id": i.pedido_id,
            "item_cardapio_id": i.item_cardapio_id,
            "quantidade": i.quantidade,
            "subtotal": i.subtotal
        } for i in itens
    ]), 200

# -------------------------
# LISTAR ITEM POR ID
# -------------------------
@itempedido_bp.route('/itempedido/<int:id>', methods=['GET'])
def listar_item_por_id(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({"erro": "Item do pedido não encontrado"}), 404
    return jsonify({
        "id": item.id,
        "pedido_id": item.pedido_id,
        "item_cardapio_id": item.item_cardapio_id,
        "quantidade": item.quantidade,
        "subtotal": item.subtotal
    }), 200

# -------------------------
# CRIAR UM OU MAIS ITENS DE PEDIDO
# -------------------------
@itempedido_bp.route('/itempedido', methods=['POST'])
def criar_item():
    dados = request.json

    pedido_id = dados.get("pedido_id")
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    itens = dados.get("itens", [])
    if not itens:
        return jsonify({"erro": "Nenhum item fornecido"}), 400

    criados = []
    valor_total = pedido.valor_total or 0

    for i in itens:
        item_cardapio_id = i.get("item_cardapio_id")
        quantidade = i.get("quantidade", 1)

        cardapio = ItemCardapio.query.get(item_cardapio_id)
        if not cardapio:
            return jsonify({"erro": f"ItemCardapio {item_cardapio_id} não encontrado"}), 404

        subtotal = quantidade * cardapio.preco
        novo_item = ItemPedido(
            pedido_id=pedido_id,
            item_cardapio_id=item_cardapio_id,
            quantidade=quantidade,
            subtotal=subtotal
        )
        db.session.add(novo_item)
        db.session.flush()  
        criados.append({
            "id": novo_item.id,
            "item_cardapio_id": item_cardapio_id,
            "quantidade": quantidade,
            "subtotal": subtotal
        })
        valor_total += subtotal

    pedido.valor_total = valor_total
    db.session.commit()

    return jsonify({
        "mensagem": "Itens do pedido criados com sucesso",
        "itens": criados,
        "valor_total": valor_total
    }), 201

# -------------------------
# ATUALIZAR ITEM DE PEDIDO
# -------------------------
@itempedido_bp.route('/itempedido/<int:id>', methods=['PUT'])
def atualizar_item(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({"erro": "Item do pedido não encontrado"}), 404

    dados = request.json

    if "quantidade" in dados:
        item.quantidade = dados["quantidade"]

    if "item_cardapio_id" in dados:
        cardapio = ItemCardapio.query.get(dados["item_cardapio_id"])
        if not cardapio:
            return jsonify({"erro": "Item do cardápio não encontrado"}), 404
        item.item_cardapio_id = dados["item_cardapio_id"]

    cardapio = ItemCardapio.query.get(item.item_cardapio_id)
    item.subtotal = item.quantidade * cardapio.preco

    db.session.commit()

    pedido = Pedido.query.get(item.pedido_id)
    pedido.valor_total = sum(i.subtotal for i in pedido.itens)
    db.session.commit()

    return jsonify({
        "mensagem": "Item do pedido atualizado",
        "id": item.id,
        "quantidade": item.quantidade,
        "subtotal": item.subtotal,
        "valor_total_pedido": pedido.valor_total
    }), 200

# -------------------------
# DELETAR ITEM
# -------------------------
@itempedido_bp.route('/itempedido/<int:id>', methods=['DELETE'])
def deletar_item(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({"erro": "Item do pedido não encontrado"}), 404

    pedido = Pedido.query.get(item.pedido_id)
    db.session.delete(item)
    db.session.commit()

    pedido.valor_total = sum(i.subtotal for i in pedido.itens)
    db.session.commit()

    return jsonify({"mensagem": "Item do pedido deletado", "valor_total_pedido": pedido.valor_total}), 200
