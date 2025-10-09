from flask import Blueprint, request, jsonify
from models import Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{"id": c.id, "nome": c.nome, "cpf": c.cpf} for c in clientes])


