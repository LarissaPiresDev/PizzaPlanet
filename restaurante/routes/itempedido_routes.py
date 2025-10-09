from flask import Blueprint, request, jsonify
from models import ItemPedido

itempedido_bp = Blueprint('itempedido_bp', __name__)

@itempedido_bp.route('/itempedido', methods=['GET'])
def listar():
    itens = ItemPedido.query.all()
    return jsonify([{"id": i.id, "quantidade": i.quantidade, "subtotal": i.subtotal} for i in itens])
