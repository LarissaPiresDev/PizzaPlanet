from flask_restx import Namespace, Resource, fields
from flask import request
from models import Cliente
from config import db
from schemas import ClienteSchema

clientes_ns = Namespace("clientes", description="Operações relacionadas aos clientes")

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

# MODELOS PARA A DOCUMENTAÇÃO DA ENTIDADE DE CLIENTE
cliente_model = clientes_ns.model("Cliente", {
    "nome": fields.String(required=True, description="Nome do cliente"),
    "cpf": fields.String(required=True, description="CPF do cliente"),
    "numero_telefone": fields.String(required=True, description="Número de telefone do cliente"),
    "endereco": fields.String(required=True, description="Endereço completo do cliente"),
})

cliente_output_model = clientes_ns.inherit("ClienteOutput", cliente_model, {
    "id": fields.Integer(description="ID do cliente"),
})

# ROTAS DA NOSSA APLICAÇÃO PIZZA PLANET
@clientes_ns.route("/")
class ClientesResource(Resource):
    @clientes_ns.marshal_list_with(cliente_output_model)
    def get(self):
        """Lista todos os clientes cadastrados"""
        clientes = Cliente.query.all()
        return clientes_schema.dump(clientes)

    @clientes_ns.expect(cliente_model)
    @clientes_ns.marshal_with(cliente_output_model, code=201)
    def post(self):
        """Cria um novo cliente"""
        dados = request.get_json()
        try:
            cliente = cliente_schema.load(dados)
            db.session.add(cliente)
            db.session.commit()
            return cliente, 201
        except Exception as e:
            db.session.rollback()
            clientes_ns.abort(400, f"Erro ao criar cliente: {e}")


@clientes_ns.route("/<int:id>")
@clientes_ns.response(404, "Cliente não encontrado")
class ClienteIdResource(Resource):
    @clientes_ns.marshal_with(cliente_output_model)
    def get(self, id):
        """Obtém um cliente pelo seu ID"""
        cliente = Cliente.query.get(id)
        if not cliente:
            clientes_ns.abort(404, "Cliente não encontrado")
        return cliente_schema.dump(cliente)

    @clientes_ns.expect(cliente_model)
    def put(self, id):
        """Atualiza os dados de um cliente"""
        cliente = Cliente.query.get(id)
        if not cliente:
            clientes_ns.abort(404, "Cliente não encontrado")

        dados = request.get_json()
        for campo, valor in dados.items():
            setattr(cliente, campo, valor)
        db.session.commit()
        return cliente_schema.dump(cliente), 200

    @clientes_ns.response(204, "Cliente deletado com sucesso")
    def delete(self, id):
        """Deleta um cliente pelo ID"""
        cliente = Cliente.query.get(id)
        if not cliente:
            clientes_ns.abort(404, "Cliente não encontrado")

        db.session.delete(cliente)
        db.session.commit()
        return "", 204
