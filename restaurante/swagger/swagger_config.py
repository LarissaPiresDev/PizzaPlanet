from . import api

from swagger.namespace.itemcardapio_namespace import itens_ns
from swagger.namespace.itempedido_namespace import itempedido_ns
from swagger.namespace.pedido_namespace import pedido_ns

def configure_swagger(app):
    """Configura a documentação Swagger e registra os namespaces"""
    api.init_app(app)
    api.add_namespace(itens_ns, path="/itemcardapio")
    api.add_namespace(itempedido_ns, "/itempedido")
    api.add_namespace(pedido_ns, "/pedido")
    api.mask_swagger = False