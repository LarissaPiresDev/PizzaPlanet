from flask import Blueprint, jsonify
from models import Pedido

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    resultado = []

    for p in pedidos:
        resultado.append({
            "id": p.id_pedido,
            "data": p.data.strftime("%Y-%m-%d") if p.data else None,
            "valor_total": p.valor_total,
            "cliente": {
                "id": p.cliente.id,
                "nome": p.cliente.nome,
                "cpf": p.cliente.cpf
            } if p.cliente else None,
            "funcionario": {
                "id": p.funcionario.id,
                "nome": p.funcionario.nome,
                "cpf": p.funcionario.cpf
            } if p.funcionario else None,
            "itens": [
                {
                    "id": i.id,
                    "quantidade": i.quantidade,
                    "subtotal": i.subtotal
                } for i in p.itens
            ]
        })

    return jsonify(resultado)


