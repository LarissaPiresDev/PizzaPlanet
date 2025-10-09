from flask import Blueprint, request, jsonify
from models import ItemCardapio
from config import db
from schemas import ItemCardapioSchema

itemcardapio_bp = Blueprint('itemcardapio_bp', __name__)

@itemcardapio_bp.route('/itemcardapio', methods=['GET'])
def listar_itens():
    itens = ItemCardapio.query.all()
    schema = ItemCardapioSchema(many=True)
    return jsonify(schema.dump(itens))

@itemcardapio_bp.route('/itemcardapio/<int:id>', methods=['GET'])
def listar_item_por_id(id):
    item = ItemCardapio.query.get(id)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    schema = ItemCardapioSchema()
    return jsonify(schema.dump(item))
