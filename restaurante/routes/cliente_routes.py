from flask import Blueprint, request, jsonify
from models import Cliente
from config import db
from schemas import ClienteSchema

cliente_bp = Blueprint('cliente_bp', __name__)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return clientes_schema.jsonify(clientes)

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    dados = request.get_json()
    try:
        cliente = cliente_schema.load(dados)
        db.session.add(cliente)
        db.session.commit()
        return cliente_schema.jsonify(cliente), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400
    

@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def listar_cliente_por_id(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "numero_telefone": cliente.numero_telefone,
        "endereco": cliente.endereco
    })


@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    dados = request.json

    if "nome" in dados:
        cliente.nome = dados["nome"]
    if "cpf" in dados:
        cliente.cpf = dados["cpf"]
    if "numero_telefone" in dados:
        cliente.numero_telefone = dados["numero_telefone"]
    if "endereco" in dados:
        cliente.endereco = dados["endereco"]

    db.session.commit()
    return jsonify({"mensagem": "Cliente atualizado"})


@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente deletado com sucesso"}), 204