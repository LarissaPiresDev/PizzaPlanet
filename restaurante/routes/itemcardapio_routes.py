from flask import Blueprint, request, jsonify
from models import ItemCardapio


itemcardapio_bp = Blueprint('itemcardapio_bp', __name__)

@itemcardapio_bp.route('/itemcardapio', methods=['GET'])
def listar_itens():
    itens = ItemCardapio.query.all()
    return jsonify([{"id": i.id, "nome": i.nome, "preco": i.preco} for i in itens])
