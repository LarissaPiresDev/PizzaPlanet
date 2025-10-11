from flask_restx import Namespace, Resource, fields
from flask import request
from models import Funcionario
from config import db
from schemas import FuncionarioSchema

funcionarios_ns = Namespace("funcionarios", description="Operações relacionadas aos funcionários")

funcionario_schema = FuncionarioSchema()
funcionarios_schema = FuncionarioSchema(many=True)

# Modelos para documentação
funcionario_model = funcionarios_ns.model("Funcionario", {
    "nome": fields.String(required=True, description="Nome do funcionário"),
    "cpf": fields.String(required=True, description="CPF do funcionário"),
    "senha": fields.String(required=True, description="Senha do funcionário"),
})

funcionario_output_model = funcionarios_ns.inherit("FuncionarioOutput", funcionario_model, {
    "id": fields.Integer(description="ID do funcionário"),
})

# Rotas do namespace
@funcionarios_ns.route("/")
class FuncionariosResource(Resource):
    @funcionarios_ns.marshal_list_with(funcionario_output_model)
    def get(self):
        """Lista todos os funcionários"""
        funcionarios = Funcionario.query.all()
        return funcionarios_schema.dump(funcionarios)

    @funcionarios_ns.expect(funcionario_model)
    @funcionarios_ns.marshal_with(funcionario_output_model, code=201)
    def post(self):
        """Cria um novo funcionário"""
        dados = request.get_json()
        try:
            funcionario = funcionario_schema.load(dados, session=db.session)
            db.session.add(funcionario)
            db.session.commit()
            return funcionario, 201
        except Exception as e:
            db.session.rollback()
            funcionarios_ns.abort(400, f"Erro ao criar funcionário: {e}")

@funcionarios_ns.route("/<int:id>")
@funcionarios_ns.response(404, "Funcionário não encontrado")
class FuncionarioIdResource(Resource):
    @funcionarios_ns.marshal_with(funcionario_output_model)
    def get(self, id):
        """Obtém um funcionário pelo ID"""
        funcionario = Funcionario.query.get(id)
        if not funcionario:
            funcionarios_ns.abort(404, "Funcionário não encontrado")
        return funcionario_schema.dump(funcionario)

    @funcionarios_ns.expect(funcionario_model)
    def put(self, id):
        """Atualiza um funcionário pelo ID"""
        funcionario = Funcionario.query.get(id)
        if not funcionario:
            funcionarios_ns.abort(404, "Funcionário não encontrado")

        dados = request.get_json()
        for campo, valor in dados.items():
            setattr(funcionario, campo, valor)
        db.session.commit()
        return funcionario_schema.dump(funcionario), 200

    @funcionarios_ns.response(204, "Funcionário deletado com sucesso")
    def delete(self, id):
        """Deleta um funcionário pelo ID"""
        funcionario = Funcionario.query.get(id)
        if not funcionario:
            funcionarios_ns.abort(404, "Funcionário não encontrado")

        db.session.delete(funcionario)
        db.session.commit()
        return "", 204
