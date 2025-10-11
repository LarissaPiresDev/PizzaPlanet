from flask_restx import Namespace, Resource, fields
from flask import request
from models import ItemCardapio
from config import db
from schemas import ItemCardapioSchema

itens_ns = Namespace("itemcardapio", description="Operações relacionadas aos itens do cardápio")

item_schema = ItemCardapioSchema()
itens_schema = ItemCardapioSchema(many=True)

# Modelos para documentação
item_model = itens_ns.model("ItemCardapio", {
    "nome": fields.String(required=True, description="Nome do item do cardápio"),
    "preco": fields.Float(required=True, description="Preço do item"),
    "descricao": fields.String(required=True, description="Descrição do item"),
})

item_output_model = itens_ns.inherit("ItemCardapioOutput", item_model, {
    "id": fields.Integer(description="ID do item do cardápio"),
})

# Rotas do namespace
@itens_ns.route("/")
class ItensResource(Resource):
    @itens_ns.marshal_list_with(item_output_model)
    def get(self):
        """Lista todos os itens do cardápio"""
        itens = ItemCardapio.query.all()
        return itens_schema.dump(itens)

    @itens_ns.expect(item_model)
    @itens_ns.marshal_with(item_output_model, code=201)
    def post(self):
        """Cria um novo item do cardápio"""
        dados = request.get_json()
        try:
            item = item_schema.load(dados, session=db.session)
            db.session.add(item)
            db.session.commit()
            return item, 201
        except Exception as e:
            db.session.rollback()
            itens_ns.abort(400, f"Erro ao criar item: {e}")

@itens_ns.route("/<int:id>")
@itens_ns.response(404, "Item não encontrado")
class ItemIdResource(Resource):
    @itens_ns.marshal_with(item_output_model)
    def get(self, id):
        """Obtém um item pelo ID"""
        item = ItemCardapio.query.get(id)
        if not item:
            itens_ns.abort(404, "Item não encontrado")
        return item_schema.dump(item)

    @itens_ns.expect(item_model)
    def put(self, id):
        """Atualiza um item do cardápio pelo ID"""
        item = ItemCardapio.query.get(id)
        if not item:
            itens_ns.abort(404, "Item não encontrado")

        dados = request.get_json()
        for campo, valor in dados.items():
            setattr(item, campo, valor)
        db.session.commit()
        return item_schema.dump(item), 200

    @itens_ns.response(204, "Item deletado com sucesso")
    def delete(self, id):
        """Deleta um item pelo ID"""
        item = ItemCardapio.query.get(id)
        if not item:
            itens_ns.abort(404, "Item não encontrado")

        db.session.delete(item)
        db.session.commit()
        return "", 204
