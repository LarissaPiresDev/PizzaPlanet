from flask import Blueprint, request, jsonify
from models import ItemCardapio
from config import db
from schemas import ItemCardapioSchema

itemcardapio_bp = Blueprint('itemcardapio_bp', __name__)


@itemcardapio_bp.route('/itemcardapio', methods=['GET'])
def listar_itens():
    itens = ItemCardapio.query.all()
    schema = ItemCardapioSchema(many=True)
    return jsonify(schema.dump(itens)), 200


@itemcardapio_bp.route('/itemcardapio/<int:id>', methods=['GET'])
def listar_item_por_id(id):
    item = ItemCardapio.query.get(id)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404

    schema = ItemCardapioSchema()
    return jsonify(schema.dump(item)), 200


@itemcardapio_bp.route('/itemcardapio', methods=['POST'])
def criar_item():
    dados = request.json
    schema = ItemCardapioSchema()

    try:
        item = schema.load(dados, session=db.session)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "mensagem": "Item criado com sucesso",
        "id": item.id
    }), 201


@itemcardapio_bp.route('/itemcardapio/<int:id>', methods=['PUT'])
def atualizar_item(id):
    item = ItemCardapio.query.get(id)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404

    dados = request.json

    item.nome = dados.get("nome", item.nome)
    item.preco = dados.get("preco", item.preco)
    item.descricao = dados.get("descricao", item.descricao)
    item.imagem = dados.get("imagem", item.imagem)

    db.session.commit()

    return jsonify({
        "mensagem": "Item atualizado com sucesso",
        "id": item.id
    }), 200


@itemcardapio_bp.route('/itemcardapio/<int:id>', methods=['DELETE'])
def deletar_item(id):
    item = ItemCardapio.query.get(id)
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "mensagem": "Item deletado com sucesso",
        "id": id
    }), 200
