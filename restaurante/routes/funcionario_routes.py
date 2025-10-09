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

@funcionario_bp.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    dados = request.json

    schema = FuncionarioSchema()
    try:
        funcionario = schema.load(dados, session=db.session)  
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

    db.session.add(funcionario)
    db.session.commit()

    return jsonify({"mensagem": "Funcionário criado com sucesso", "id": funcionario.id}), 201


@funcionario_bp.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    funcionario = Funcionario.query.get(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    dados = request.json
    if "nome" in dados: funcionario.nome = dados["nome"]
    if "cpf" in dados: funcionario.cpf = dados["cpf"]
    if "senha" in dados: funcionario.senha = dados["senha"]

    db.session.commit()
    return jsonify({"mensagem": "Funcionário atualizado com sucesso", "id": funcionario.id})

@funcionario_bp.route('/funcionarios/<int:id>', methods=['DELETE'])
def deletar_funcionario(id):
    funcionario = Funcionario.query.get(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    db.session.delete(funcionario)
    db.session.commit()
    return jsonify({"mensagem": "Funcionário deletado com sucesso", "id": id}), 204

