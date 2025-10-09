from flask import Blueprint, request, jsonify
from models import ItemPedido, ItemCardapio
from config import db
from schemas import ItemPedidoSchema

itempedido_bp = Blueprint('itempedido_bp', __name__)

@itempedido_bp.route('/itempedido', methods=['GET'])
def listar():
    itens = ItemPedido.query.all()
    return jsonify([{"id": i.id, "quantidade": i.quantidade, "subtotal": i.subtotal} for i in itens])


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
    })

@itempedido_bp.route('/itempedido', methods=['POST'])
def criar_item():
    dados = request.json
    schema = ItemPedidoSchema()
    
    try:
        item = schema.load(dados, session=db.session)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


    cardapio = ItemCardapio.query.get(item.item_cardapio_id)
    if not cardapio:
        return jsonify({"erro": "Item do cardápio não encontrado"}), 404
    item.subtotal = item.quantidade * cardapio.preco

    db.session.add(item)
    db.session.commit()
    return jsonify({"mensagem": "Item do pedido criado", "id": item.id, "subtotal": item.subtotal}), 201

@itempedido_bp.route('/itempedido/<int:id>', methods=['PUT'])
def atualizar_item(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({"erro": "Item do pedido não encontrado"}), 404

    dados = request.json
    if "pedido_id" in dados:
        item.pedido_id = dados["pedido_id"]
    if "item_cardapio_id" in dados:
        item.item_cardapio_id = dados["item_cardapio_id"]
    if "quantidade" in dados:
        item.quantidade = dados["quantidade"]

    cardapio = ItemCardapio.query.get(item.item_cardapio_id)
    if cardapio:
        item.subtotal = item.quantidade * cardapio.preco

    db.session.commit()
    return jsonify({"mensagem": "Item do pedido atualizado", "id": item.id, "subtotal": item.subtotal})



