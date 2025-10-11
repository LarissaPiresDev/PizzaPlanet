from . import api
from swagger.namespace.cliente_namespace import clientes_ns
from swagger.namespace.funcionario_namespace import funcionarios_ns

def configure_swagger(app):
    """Configura a documentação Swagger e registra os namespaces"""
    api.init_app(app)
    api.add_namespace(clientes_ns, path="/clientes")
    api.add_namespace(funcionarios_ns, path="/funcionarios")
    api.mask_swagger = False