from flask import Blueprint, request, jsonify
from models import Pedido, ItemPedido, ItemCardapio
from config import db
from datetime import datetime

pedido_bp = Blueprint('pedido_bp', __name__)

# ---------------------------
# LISTAR TODOS OS PEDIDOS
# ---------------------------
@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    resultado = []
    for p in pedidos:
        resultado.append({
            "id": p.id_pedido,
            "nome": p.nome,
            "data": p.data.strftime("%Y-%m-%d") if p.data else None,
            "status": p.status,
            "valor_total": p.valor_total,
            "itens": [
                {
                    "id": item.id,
                    "item_cardapio_id": item.item_cardapio_id,
                    "quantidade": item.quantidade,
                    "subtotal": item.subtotal
                } for item in p.itens
            ]
        })
    return jsonify(resultado), 200


# ---------------------------
# LISTAR PEDIDO POR ID
# ---------------------------
@pedido_bp.route('/pedidos/<int:id>', methods=['GET'])
def listar_pedido_por_id(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    resultado = {
        "id": pedido.id_pedido,
        "nome": pedido.nome,
        "data": pedido.data.strftime("%Y-%m-%d") if pedido.data else None,
        "status": pedido.status,
        "valor_total": pedido.valor_total,
        "itens": [
            {
                "id": item.id,
                "item_cardapio_id": item.item_cardapio_id,
                "quantidade": item.quantidade,
                "subtotal": item.subtotal
            } for item in pedido.itens
        ]
    }
    return jsonify(resultado), 200


# ---------------------------
# CRIAR PEDIDO
# ---------------------------
@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.json
    nome = dados.get("nome")
    data_str = dados.get("data")
    itens = dados.get("itens", [])
    
    if not nome:
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    try:
        data_formatada = datetime.strptime(data_str, "%Y-%m-%d").date() if data_str else datetime.utcnow().date()
    except:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    pedido = Pedido(nome=nome, data=data_formatada)
    db.session.add(pedido)
    db.session.commit()  # gera id_pedido

    valor_total = 0
    for item in itens:
        item_cardapio_id = item.get("item_cardapio_id")
        quantidade = item.get("quantidade", 1)

        cardapio = ItemCardapio.query.get(item_cardapio_id)
        if not cardapio:
            return jsonify({"erro": f"ItemCardapio {item_cardapio_id} não encontrado"}), 404

        novo_item = ItemPedido(
            pedido_id=pedido.id_pedido,
            item_cardapio_id=item_cardapio_id,
            quantidade=quantidade
        )
        novo_item.calcular_subtotal()
        valor_total += novo_item.subtotal
        db.session.add(novo_item)

    pedido.valor_total = valor_total
    db.session.commit()

    return jsonify({"mensagem": "Pedido criado com sucesso", "id": pedido.id_pedido}), 201


# ---------------------------
# ATUALIZAR PEDIDO
# ---------------------------
@pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    dados = request.json

    # Atualiza campos do pedido
    if "nome" in dados:
        pedido.nome = dados["nome"]

    if "data" in dados:
        try:
            pedido.data = datetime.strptime(dados["data"], "%Y-%m-%d").date()
        except:
            return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    if "status" in dados:
        pedido.status = dados["status"]

    # Atualiza itens do pedido se enviados
    itens_enviados = dados.get("itens")
    if itens_enviados is not None:
        ids_enviados = []
        for i in itens_enviados:
            item_id = i.get("id")
            item_cardapio_id = i.get("item_cardapio_id")
            quantidade = i.get("quantidade", 1)

            # Verifica se item_cardapio existe
            cardapio = ItemCardapio.query.get(item_cardapio_id)
            if not cardapio:
                return jsonify({"erro": f"ItemCardapio {item_cardapio_id} não encontrado"}), 404

            if item_id:
                # Atualiza item existente
                item = ItemPedido.query.get(item_id)
                if not item:
                    return jsonify({"erro": f"ItemPedido {item_id} não encontrado"}), 404
                item.item_cardapio_id = item_cardapio_id
                item.quantidade = quantidade
                item.subtotal = quantidade * cardapio.preco
            else:
                # Cria novo item
                item = ItemPedido(
                    pedido_id=pedido.id_pedido,
                    item_cardapio_id=item_cardapio_id,
                    quantidade=quantidade,
                    subtotal=quantidade * cardapio.preco
                )
                db.session.add(item)
            db.session.flush()  # Gera id do item antes de commit
            ids_enviados.append(item.id)

        # Remove itens que não foram enviados
        for item in pedido.itens:
            if item.id not in ids_enviados:
                db.session.delete(item)

    # Recalcula valor total do pedido
    db.session.commit()  # salva alterações dos itens
    pedido.valor_total = sum(item.subtotal for item in pedido.itens)
    db.session.commit()

    return jsonify({"mensagem": "Pedido atualizado com sucesso", "id": pedido.id_pedido, "valor_total": pedido.valor_total}), 200


# ---------------------------
# DELETAR PEDIDO
# ---------------------------
@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"mensagem": "Pedido deletado com sucesso", "id": id}), 200
