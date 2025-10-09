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
    data = request.get_json()
    try:
        cliente = cliente_schema.load(data)
        db.session.add(cliente)
        db.session.commit()
        return cliente_schema.jsonify(cliente), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400



