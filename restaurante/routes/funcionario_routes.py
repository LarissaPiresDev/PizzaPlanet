from flask import Blueprint, request, jsonify
from models import Funcionario

funcionario_bp = Blueprint('funcionario_bp', __name__)

@funcionario_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return jsonify([{"id": f.id, "nome": f.nome} for f in funcionarios])

