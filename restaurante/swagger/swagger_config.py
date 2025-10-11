from . import api
from swagger.namespace.cliente_namespace import clientes_ns

def configure_swagger(app):
    """Configura a documentação Swagger e registra os namespaces"""
    api.init_app(app)
    api.add_namespace(clientes_ns, path="/cliente")
    api.mask_swagger = False