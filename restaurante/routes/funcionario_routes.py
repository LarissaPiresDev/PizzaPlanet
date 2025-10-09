from flask import Blueprint, request, jsonify
from models import Funcionario
from config import db
from schemas import FuncionarioSchema

funcionario_bp = Blueprint('funcionario_bp', __name__)

@funcionario_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return jsonify([{"id": f.id, "nome": f.nome} for f in funcionarios])

@funcionario_bp.route('/funcionarios/<int:id>', methods=['GET'])
def listar_funcionario_por_id(id):
    funcionario = Funcionario.query.get(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não foi encontrado"}), 404
    return jsonify({"id": funcionario.id, "nome": funcionario.nome, "cpf": funcionario.cpf})

